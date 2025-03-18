#include <Arduino.h>
#include <pins_arduino.h>
#include "Adafruit_TinyUSB.h"
#include "nrf.h"         // Provides register definitions for the nRF52840
#include "delay.h"
#include <math.h>

float MV_PER_LSB = 1200.0F/1024.0F; // 10-bit ADC with 3.6V input range

// Configuration constants
#define ADC_THRESHOLD       1100         // Only used in analog mode
#define BIT_READ_TIMEOUT    100          // Timeout for a single bit (ms)
#define PACKET_READ_TIMEOUT 250          // Overall timeout for a 24-bit packet (ms)

// Digital input pins for pedals
#define PIN_PEDAL      13
#define PIN_BTN_FUNC   12
#define PIN_BTN_FUNC2  14

// Gauge clock and data pins
// For the gauges with a MicroUSB connector the pinout is white (D-) = clock, green (D+) = data
#define GAUGE1_CLOCK   34
#define GAUGE1_DATA    35
#define GAUGE2_CLOCK   32
#define GAUGE2_DATA    33
#define GAUGE3_CLOCK   25
#define GAUGE3_DATA    26

// Hysteresis filter: maximum allowed change (in mm) between successive filtered readings.
#define MAX_DELTA 1.0f

// Minimum value filter: discard data lower than this (gauge is not in use)
#define MIN_VAL 0.6f

// BLE-related Constants
#define WHC06_MANUFACTURER_ID 256
#define WEIGHT_OFFSET         32  // Offset in manufacturer data for weight

const int bleScanTime = 5;         // BLE scan time in seconds

// Structure to pass parameters to each gauge task
struct GaugeTaskParams
{
	int gauge_number;  // Gauge identifier (1, 2, or 3)
	int clock_pin;     // Input pin for the clock signal
	int data_pin;      // Input pin for the data signal
};


/**
 * @brief Reads one bit from a gauge’s clock and data lines.
 *      In analog mode, it uses analogRead() with a threshold.
 *      In digital mode (when USE_SCHMITT_TRIGGER is defined),
 *      it uses digitalRead() and inverts the logic.
 *
 * @param clock_pin   The pin for the gauge clock signal
 * @param data_pin    The pin for the gauge data signal
 *
 * @return int Bit value (0 or 1) if a valid value could be read, otherwise -1
 */
int get_gauge_bit(int clock_pin, int data_pin)
{
    unsigned long timeout = millis() + BIT_READ_TIMEOUT;
	// Analog mode: use analogRead() with a threshold.
	while (float f = analogRead(clock_pin) > ADC_THRESHOLD)
	{
		Serial.println(f);
        if (millis() > timeout)
			return -1;
	}
    while (float f = analogRead(clock_pin) < ADC_THRESHOLD)
	{
		Serial.println(f);
        if (millis() > timeout)
			return -1;
	}
	// Analog mode: use analogRead() with a threshold.
    float f = analogRead(data_pin);
    Serial.println(f);
	int data = (f > ADC_THRESHOLD) ? 1 : 0;
	return data;
}

/**
 * @brief Reads a complete 24-bit packet from the gauge lines.
 *
 * @param clock_pin   The pin for the gauge clock signal
 * @param data_pin    The pin for the gauge data signal
 *
 * @return long The whole 24 bit packet, or -1 if unable to read gauge
 */
long get_gauge_packet(int clock_pin, int data_pin)
{
	long packet = 0;
	unsigned long timeout = millis() + PACKET_READ_TIMEOUT;
	int bit_index = 0;
	while (bit_index < 24)
	{
		int bit = get_gauge_bit(clock_pin, data_pin);
		if (bit < 0)
		{
			if (millis() > timeout)
				return -1;
			// Restart packet if a bit times out before overall timeout.
			bit_index = 0;
			packet = 0;
			continue;
		}
		packet |= ((long)(bit & 1)) << bit_index;
		bit_index++;
	}
	return packet;
}

/**
 * @brief Parses a 24-bit packet into a gauge reading (deflection in mm).
 *        The conversion uses only the lower 12 bits for the gauge value,
 *        interprets bit 20 as the negative flag and bit 23 as the "inches" flag.
 *
 * @param packet   The 24-bit packet of gauge data
 *
 * @return float The gauge deflection value in mm
 */
float parse_gauge_packet(long packet)
{
	if (packet < 0)
		return -1000.0f;  // Error value indicating timeout
	int gauge_val = packet & 0x0FFF;  // Lower 12 bits
	bool negative = (packet & (1 << 20)) != 0;
	bool inches   = (packet & (1 << 23)) != 0;
	int value = negative ? -gauge_val : gauge_val;
	if (inches)
		value = static_cast<int>((value / 2.0) * 2.54); // Strictly metric

	return static_cast<float>(value) / 100.0f;
}

// Gauge reading task: continuously reads from one gauge and posts updates if the value changes.
float last_value = 0.0f;      // Stores the last accepted value

void setup() {
    Serial.begin(115200);
    analogReadResolution(10);  // Can be 8, 10, 12 or 14
    analogReference(AR_INTERNAL_1_2);
}

void loop()
{
    long packet = get_gauge_packet(PIN_031, PIN_029);
    float value = parse_gauge_packet(packet);

    // Timeout or garbage data
    if (value < MIN_VAL)
    {
        last_value = 0;
        return;
    }

    // Hysteresis filter: if the change is too large or too small, assume noise and discard update.
    float delta_value = (fabs(value - last_value));
    last_value = value;
    if ((delta_value < 0.01) || (delta_value > MAX_DELTA))
        return;

    last_value = value;
    char msg[100];
    snprintf(msg, sizeof(msg), "gauge,%d,%.2f", 0, value);
    Serial.println(msg);
}
