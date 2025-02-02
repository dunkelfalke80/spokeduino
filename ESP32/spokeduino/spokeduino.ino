#include <BluetoothSerial.h>

BluetoothSerial SerialBT;

// Define gauge pins
#define PIN_GAUGE1_CLOCK 34
#define PIN_GAUGE1_DATA  35
#define PIN_GAUGE2_CLOCK 32
#define PIN_GAUGE2_DATA  39
#define PIN_GAUGE3_CLOCK 36
#define PIN_GAUGE3_DATA  27

// Define digital input pins
#define PIN_PEDAL        26
#define PIN_BTN_FUNC     25
#define PIN_BTN_FUNC2    33

// --- CONFIGURATION OPTIONS ---
#define USE_START_PULSE       // Uncomment to enable start pulse detection
#define USE_ANALOG_INPUTS     // Uncomment to use analog input instead of digital input
#define INVERTED_LOGIC        // Uncomment if using transistors (inverts signal logic)

// --- CONSTANTS ---
#define ADC_THRESHOLD_HIGH 1400  // Adjusted for HIGH signal
#define ADC_THRESHOLD_LOW  1000  // Adjusted for LOW signal
#define START_PULSE_MIN_DURATION 100000  // Min duration (µs) for start pulse (~100ms)
#define GAUGE_TIMEOUT 1000  // Timeout in microseconds for bit reading

float gauge1_deflection_old = 0.1f;
float gauge2_deflection_old = 0.1f;
float gauge3_deflection_old = 0.1f;

/**
 * @brief Reads the clock and data signals.
 * Handles both analog/digital inputs and optional logic inversion.
 * @param pin The pin to read.
 * @return 1 for HIGH, 0 for LOW.
 */
int read_signal(uint8_t pin) {
#ifdef USE_ANALOG_INPUTS
    int signal = analogRead(pin);
    if (signal > ADC_THRESHOLD_HIGH) return 1;
    if (signal < ADC_THRESHOLD_LOW) return 0;
    return -1;  // Undefined/mid-level
#else
    int signal = digitalRead(pin);
#endif

#ifdef INVERTED_LOGIC
    signal = !signal;
#endif

    return signal;
}

/**
 * @brief Detects the start pulse before reading data.
 * @param clock_pin The clock pin.
 * @return true if start pulse is detected, false otherwise.
 */
bool detect_start_pulse(uint8_t clock_pin) {
    unsigned long start_time = micros();

    while (read_signal(clock_pin) == 1) {  // Wait while clock is HIGH
        if ((micros() - start_time) > START_PULSE_MIN_DURATION) {
            Serial.println("Start pulse detected!");
            return true;
        }
    }
    Serial.println("Start pulse NOT detected!");
    return false;
}

/**
 * @brief Reads a single bit from the gauge.
 * @param clock_pin The clock pin to read.
 * @param data_pin The data pin to read.
 * @return The bit value (0 or 1) or -1 on timeout.
 */
int read_bit(uint8_t clock_pin, uint8_t data_pin) {
    unsigned long timeout = micros() + GAUGE_TIMEOUT;

    // Wait for clock to go LOW
    while (read_signal(clock_pin) == 1) {
        if (micros() > timeout) return -1;
    }

    // Wait for clock to go HIGH (bit ready to be read)
    while (read_signal(clock_pin) == 0) {
        if (micros() > timeout) return -1;
    }

    // Read the data bit
    return read_signal(data_pin);
}

/**
 * @brief Reads the gauge data packet (24 bits).
 * Supports optional start pulse detection.
 * @param clock_pin The clock pin to read.
 * @param data_pin The data pin to read.
 * @return The decoded gauge value or -1000.0 on timeout/error.
 */
float read_gauge(uint8_t clock_pin, uint8_t data_pin) {
#ifdef USE_START_PULSE
    if (!detect_start_pulse(clock_pin)) {
        Serial.println("No start pulse detected, skipping...");
        return -1000.0f;
    }
#endif

    int outputval = 0;
    for (int shift = 0; shift < 24; shift++) {
        int bit = read_bit(clock_pin, data_pin);
        if (bit < 0) {
            Serial.println("Bit read timeout!");
            return -1000.0f;
        }
        outputval |= (bit << shift);
    }

    // Decode measurement
    bool inches = (outputval & 0x800000) != 0;
    bool negative = (outputval & 0x400000) != 0;
    outputval &= 0x3FFFFF;

    float measurement = static_cast<float>(outputval) / 20480.0f;
    if (inches) measurement *= 25.4;
    if (negative) measurement = -measurement;

    return measurement;
}

/**
 * @brief Sends the gauge value to the serial output and Bluetooth.
 */
void send_gauge_value(uint8_t gauge_number, float deflection_value) {
    Serial.printf("%d:%.2f\r\n", gauge_number, deflection_value);
    SerialBT.printf("%d:%.2f\r\n", gauge_number, deflection_value);
}

/**
 * @brief Processes a single gauge.
 */
void process_gauge(uint8_t clock_pin, uint8_t data_pin, uint8_t gauge_number, float &old_deflection_value) {
    float deflection_value = read_gauge(clock_pin, data_pin);

    // Skip timeouts and unchanged values
    if (deflection_value < -10.0f || deflection_value == old_deflection_value) return;

    old_deflection_value = deflection_value;
    send_gauge_value(gauge_number, deflection_value);
}

/**
 * @brief Initializes the ESP32.
 */
void setup() {
    Serial.begin(115200);   // Increased baud rate for faster debugging
    SerialBT.begin("Spokeduino-ESP32");

    // Optimize ADC settings
    analogReadResolution(12);     
    analogSetWidth(12);           
    analogSetAttenuation(ADC_11db); 

    // Configure gauge ports as inputs
    pinMode(PIN_GAUGE1_CLOCK, INPUT);
    pinMode(PIN_GAUGE1_DATA, INPUT);
    pinMode(PIN_GAUGE2_CLOCK, INPUT);
    pinMode(PIN_GAUGE2_DATA, INPUT);
    pinMode(PIN_GAUGE3_CLOCK, INPUT);
    pinMode(PIN_GAUGE3_DATA, INPUT);

    // Enable internal pull-up for other inputs
    pinMode(PIN_PEDAL, INPUT_PULLUP);
    pinMode(PIN_BTN_FUNC, INPUT_PULLUP);
    pinMode(PIN_BTN_FUNC2, INPUT_PULLUP);
}

/**
 * @brief Main loop.
 */
void loop() {
    process_gauge(PIN_GAUGE1_CLOCK, PIN_GAUGE1_DATA, 1, gauge1_deflection_old);
    delay(50);  // Adjust delay if needed for proper signal processing
}
