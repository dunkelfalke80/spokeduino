// MIT License
//
// Copyright (c) 2025 Roman Galperin
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

#include <BluetoothSerial.h>

BluetoothSerial SerialBT;

#define PIN_GAUGE1_CLOCK 23
#define PIN_GAUGE1_DATA  22
#define PIN_GAUGE2_CLOCK 32
#define PIN_GAUGE2_DATA  39
#define PIN_GAUGE3_CLOCK 36
#define PIN_GAUGE3_DATA  27

#define PIN_PEDAL        26
#define PIN_BTN_FUNC     25
#define PIN_BTN_FUNC2    33

#define GAUGE_TIMEOUT    1000

float gauge1_deflection_old = 0.1f;
float gauge2_deflection_old = 0.1f;
float gauge3_deflection_old = 0.1f;

int pedal_value_old = 0;
int btn_func_value_old = 0;
int btn_func2_value_old = 0;

bool pedal_value_toggle = false;
bool btn_func_value_toggle = false;
bool btn_func2_value_toggle = false;

/**
 * @brief Reads the gauge with the signal inverted by the transistor.
 *
 * @param clock_pin       The clock pin of the gauge
 * @param data_pin        The data pin of the gauge
 * @param timeout         The maximum time (ms) to wait for a falling edge on each bit
 *
 * @return float Gauge value in mm, two decimal places; -1000.0 on timeout
 */
float read_gauge(uint8_t clock_pin, uint8_t data_pin, unsigned long timeout)
{
    unsigned long looptime = millis();
    int shift = 0;
    int outputval = 0;
    bool inches = false;
    bool negative = false;
    
    unsigned long pulse_start = millis();
    while (!digitalRead(clock_pin));  // Wait for HIGH clock
    unsigned long high_duration = millis() - pulse_start;
    
    bool start_pulse_detected = (high_duration > 500);

    while (shift < 24) 
    {
        while (!digitalRead(clock_pin)); // Wait for LOW (actual HIGH from gauge)
        while (digitalRead(clock_pin));  // Wait for HIGH (actual LOW from gauge)

        if (!digitalRead(data_pin))  // Inverted logic
        {
            outputval |= (1 << shift);
        }
        shift++;
    }

    negative = (outputval & (1 << 20)) != 0;
    inches = (outputval & (1 << 23)) != 0;  
    outputval &= 0xFFFFF; 

    float measurement = static_cast<float>(negative ? -outputval : outputval) / 100.0f;
    
    if (inches) 
        measurement *= 25.4;

    // Store values instead of printing inside function
    static char debug_buffer[128];  // Create buffer to store formatted output
    snprintf(debug_buffer, sizeof(debug_buffer), "Start pulse: %d | Raw: %d | Measurement: %.2f %s", start_pulse_detected,
             outputval, measurement, inches ? "in" : "mm");
    Serial.println(debug_buffer);

    // Return measurement and save debug output
    // SerialBT.println(debug_buffer);  // Send over Bluetooth
    return measurement;
}

/**
 * @brief Sends the gauge value to the serial output and Bluetooth
 *
 * @param gauge_number      Identifier for the gauge (1, 2 or 3)
 * @param deflection_value  The gauge deflection value in mm.
 */
void send_gauge_value(const uint8_t gauge_number, float deflection_value)
{
    Serial.print(gauge_number);
    Serial.print(':');
    Serial.print(deflection_value);
    Serial.print("\r\n");

    SerialBT.print(gauge_number);
    SerialBT.print(':');
    SerialBT.print(deflection_value);
    SerialBT.print("\r\n");
}


/**
 * @brief Sends an input status value to the serial output and Bluetooth
 *
 * @param input_number      Identifier for the digital input
 * @param value             The gauge deflection value in mm.
 */
void send_input_value(const uint8_t pin_number, int value)
{
    Serial.print(pin_number);
    Serial.print(':');
    Serial.print(value);
    Serial.print("\r\n");

    SerialBT.print(pin_number);
    SerialBT.print(':');
    SerialBT.print(value);
    SerialBT.print("\r\n");
}

/**
 * @brief Runs the full job for a single gauge.
 *
 * Reads the gauge value, compares it to the old value, checks for a timeout,
 * sends updated data to the serial port.
 *
 * @param clock_pin            The clock pin of the gauge
 * @param data_pin             The data pin of the gauge
 * @param gauge_number         The number of the gauge (1, 2 or 3)
 * @param old_deflection_value The previous valid detection value reference
 */
void process_gauge(uint8_t clock_pin, uint8_t data_pin, const uint8_t gauge_number, float& old_deflection_value)
{
    float deflection_value = read_gauge(clock_pin, data_pin, GAUGE_TIMEOUT);

    // Skip timeouts and unchanged values
    if (deflection_value < -10.0f || deflection_value == old_deflection_value)
        return;

    old_deflection_value = deflection_value;
    send_gauge_value(gauge_number, deflection_value);
}

/**
 * @brief Runs the full job for a single digital input.
 *
 * Reads the input value, compares it to the old value,
 * sends updated data to the serial port on a full toggle.
 *
 * @param pin_number  The number of the pin
 * @param old_value   The previous valid detection value reference
 */
void process_pin(const uint8_t pin_number, int& old_value, bool& toggle_value)
{
    int value = digitalRead(pin_number);

    // Skip unchanged values
    if (value == old_value)
        return;

    old_value = value;
    if (toggle_value) // Only send a value on a full toggle (high-low-high)
    {
        toggle_value = false;
        send_input_value(pin_number, value);
    }
    else
    {
        toggle_value = true;
    }
}

void setup()
{
    Serial.begin(9600); // Debugging via USB Serial
    SerialBT.begin("Spokeduino-ESP32"); // Bluetooth Serial name

    // Configure gauge ports as analog inputs
    //pinMode(PIN_GAUGE1_CLOCK, INPUT);
    //pinMode(PIN_GAUGE1_DATA, INPUT);
    pinMode(PIN_GAUGE1_CLOCK, INPUT_PULLUP);
    pinMode(PIN_GAUGE1_DATA, INPUT_PULLUP);    
    pinMode(PIN_GAUGE2_CLOCK, INPUT);
    pinMode(PIN_GAUGE2_DATA, INPUT);
    pinMode(PIN_GAUGE3_CLOCK, INPUT);
    pinMode(PIN_GAUGE3_DATA, INPUT);

    // Enable the internal pullup resistor for all controller inputs
    pinMode(PIN_PEDAL, INPUT_PULLUP);
    pinMode(PIN_BTN_FUNC, INPUT_PULLUP);
    pinMode(PIN_BTN_FUNC2, INPUT_PULLUP);

    // Reset all checked digital input values
    pedal_value_old = digitalRead(PIN_PEDAL);
    btn_func_value_old = digitalRead(PIN_BTN_FUNC);
    btn_func2_value_old = digitalRead(PIN_BTN_FUNC2);

    Serial.print("Clock ADC: ");
    Serial.println(analogRead(PIN_GAUGE1_CLOCK));
    Serial.print("Data ADC: ");
    Serial.println(analogRead(PIN_GAUGE1_DATA));
}


static int lastClock = -1;
static int lastData = -1;
unsigned long lastTime = micros();

void loop() 
{

    //process_pin(PIN_PEDAL, pedal_value_old, pedal_value_toggle);
    //process_pin(PIN_BTN_FUNC, btn_func_value_old, btn_func_value_toggle);
    //process_pin(PIN_BTN_FUNC2, btn_func2_value_old, btn_func2_value_toggle);
    //process_gauge(PIN_GAUGE1_CLOCK, PIN_GAUGE1_DATA, 0, gauge1_deflection_old);
    //process_gauge(PIN_GAUGE2_CLOCK, PIN_GAUGE2_DATA, 1, gauge2_deflection_old);
    //process_gauge(PIN_GAUGE3_CLOCK, PIN_GAUGE3_DATA, 2, gauge3_deflection_old);
    //delay(50);
    //Serial.print("Clock Pin: ");
    //Serial.print(digitalRead(PIN_GAUGE1_CLOCK));
    //Serial.print(" | Data Pin: ");
    //Serial.println(digitalRead(PIN_GAUGE1_DATA));
    //delay(100);  // Slow down for readability
    
    int clockState = digitalRead(PIN_GAUGE1_CLOCK);
    int dataState = digitalRead(PIN_GAUGE1_DATA);

    // Detect clock edge
    if (clockState != lastClock) {
        unsigned long now = micros();
        Serial.print("Clock Edge Detected | Duration: ");
        Serial.print(now - lastTime);
        Serial.print(" µs | Clock: ");
        Serial.print(clockState);
        Serial.print(" | Data: ");
        Serial.println(dataState);
        lastTime = now;
        lastClock = clockState;
    }
}
