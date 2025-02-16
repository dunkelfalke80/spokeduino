// MIT License
//
// Copyright (c) 2025 Roman Galperin
// Original code Copyright (c) David Pilling (https://www.davidpilling.com/wiki/index.php/DialGauge)
// and used with explicid permission.
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

#include <Arduino.h>
#include <BluetoothSerial.h>
#include <math.h>
#include <BLEDevice.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>

// ------------------------------------------------------------------
// Uncomment the following line to use the stable digital (inverted)
// gauge signals (if using a transistor circuit on data and clock)
// ------------------------------------------------------------------
// #define USE_TRANSISTOR

// Configuration constants
#define ADC_THRESHOLD       1100         // Only used in analog mode
#define BIT_READ_TIMEOUT    100          // Timeout for a single bit (ms)
#define PACKET_READ_TIMEOUT 250          // Overall timeout for a 24-bit packet (ms)

// Digital input pins for pedals
#define PIN_PEDAL      13
#define PIN_BTN_FUNC   12
#define PIN_BTN_FUNC2  14

// Gauge clock and data pins
// For gauges with a MicroUSB connector the pinout is white (D-) = clock, green (D+) = data
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

// Global Objects and Types

// Global BLEScan pointer
BLEScan* pBLEScan = nullptr;

// Bluetooth Serial (SPP) instance for dual serial output
BluetoothSerial SerialBT;

// Message structure for sending updates
typedef struct
{
	char message[64];
} Message;

// FreeRTOS queue handle for outgoing messages
QueueHandle_t sendQueue = NULL;

// Structure to pass parameters to each gauge task
struct GaugeTaskParams
{
	int gauge_number;  // Gauge identifier (1, 2, or 3)
	int clock_pin;     // Input pin for the clock signal
	int data_pin;      // Input pin for the data signal
};


// BLE Advertisement Callback
class WHC06AdvertisedDeviceCallbacks : public BLEAdvertisedDeviceCallbacks
{
	void onResult(BLEAdvertisedDevice advertisedDevice)
	{
		if (advertisedDevice.haveManufacturerData())
		{
			std::string  manufacturerData = advertisedDevice.getManufacturerData();
			if (manufacturerData.size() < WEIGHT_OFFSET + 2) return;
			uint16_t companyId = (uint8_t)manufacturerData[0] | ((uint8_t)manufacturerData[1] << 8);
			if (companyId == WHC06_MANUFACTURER_ID)
			{
				// Extract two bytes from offset WEIGHT_OFFSET to form a raw weight value.
				uint16_t weightRaw = ((uint8_t)manufacturerData[WEIGHT_OFFSET] << 8) |
									 (uint8_t)manufacturerData[WEIGHT_OFFSET + 1];
				// Convert raw weight to kilograms (assuming the sensor sends weight in grams).
				float weightKg = weightRaw / 100.0;
				Message msg;
				snprintf(msg.message, sizeof(msg.message), "weight,%.2f", weightKg);
				xQueueSend(sendQueue, &msg, portMAX_DELAY);
			}
		}
	}
};


/**
 * @brief Reads one bit from a gauge’s clock and data lines.
 *      In analog mode, it uses analogRead() with a threshold.
 *      In digital mode (when USE_TRANSISTOR is defined), it uses digitalRead() and inverts the logic.
 *
 * @param clock_pin   The pin for the gauge clock signal
 * @param data_pin    The pin for the gauge data signal
 *
 * @return int Bit value (0 or 1) if a valid value could be read, otherwise -1
 */
int get_gauge_bit(int clock_pin, int data_pin)
{
    unsigned long timeout = millis() + BIT_READ_TIMEOUT;
#ifdef USE_TRANSISTOR
	// Wait for clock to go HIGH (which is the inverted equivalent of a falling edge).
	while (digitalRead(clock_pin) == LOW)
#else
	// Analog mode: use analogRead() with a threshold.
	while (analogRead(clock_pin) > ADC_THRESHOLD)
#endif
	{
		if (millis() > timeout)
			return -1;
	}
#ifdef USE_TRANSISTOR
	// Then wait for clock to go LOW.
	while (digitalRead(clock_pin) == HIGH)
#else
    while (analogRead(clock_pin) < ADC_THRESHOLD)
#endif
	{
		if (millis() > timeout)
			return -1;
	}
#ifdef USE_TRANSISTOR
	// Read the data pin and invert the result: HIGH becomes 0, LOW becomes 1.
	int data = digitalRead(data_pin);
	return (data == HIGH) ? 0 : 1;
#else
	// Analog mode: use analogRead() with a threshold.
	int data = (analogRead(data_pin) > ADC_THRESHOLD) ? 1 : 0;
	return data;
#endif
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
void gauge_task(void *param)
{
	GaugeTaskParams *p = (GaugeTaskParams*) param;
    float last_value = 0.0f;      // Stores the last accepted value
#ifdef USE_TRANSISTOR
	pinMode(p->clock_pin, INPUT);
	pinMode(p->data_pin, INPUT);
#endif
	while (true)
	{
        vTaskDelay(50 / portTICK_PERIOD_MS);
        long packet = get_gauge_packet(p->clock_pin, p->data_pin);
		float value = parse_gauge_packet(packet);

        // Timeout or garbage data
		if (value < MIN_VAL)
        {
            last_value = 0;
            continue;
        }

        // Hysteresis filter: if the change is too large or too small, assume noise and discard update.
        float delta_value = (fabs(value - last_value));
        last_value = value;
        if ((delta_value < 0.01) || (delta_value > MAX_DELTA))
            continue;

        last_value = value;
        Message msg;
		snprintf(msg.message, sizeof(msg.message), "gauge,%d,%.2f", p->gauge_number, value);
		xQueueSend(sendQueue, &msg, portMAX_DELAY);
	}
}

// Digital inputs task: monitors three digital inputs (pedal and buttons) and sends an update when a full toggle occurs.
void digitalInputTask(void *param)
{
	const int pins[3] = {PIN_PEDAL, PIN_BTN_FUNC, PIN_BTN_FUNC2};
	int last_value[3];
	bool toggleFlags[3] = {false, false, false};
	for (int i = 0; i < 3; i++)
	{
		pinMode(pins[i], INPUT_PULLUP);
		last_value[i] = digitalRead(pins[i]);
	}
	while (true)
	{
		for (int i = 0; i < 3; i++)
		{
			int value = digitalRead(pins[i]);
			if (value != last_value[i])
			{
				last_value[i] = value;
				if (toggleFlags[i])
				{
					toggleFlags[i] = false;
					Message msg;
					snprintf(msg.message, sizeof(msg.message), "input,%d,%d", pins[i], value);
					xQueueSend(sendQueue, &msg, portMAX_DELAY);
				}
				else
				{
					toggleFlags[i] = true;
				}
			}
		}
		vTaskDelay(10 / portTICK_PERIOD_MS);
	}
}

// BLE scanner task: continuously scans for BLE advertisements from the WH-C06 scale,
// extracts weight data, and posts it to the send queue.
void bleScannerTask(void *param)
{
	// Initialize BLE and configure the scan.
	BLEDevice::init("");
	pBLEScan = BLEDevice::getScan();
	pBLEScan->setAdvertisedDeviceCallbacks(new WHC06AdvertisedDeviceCallbacks());
	pBLEScan->setActiveScan(true); // Request extra data from advertisers.
	while (true)
	{
		Serial.println("BLE: Scanning for WH-C06 scale...");
		pBLEScan->start(bleScanTime, false);
		pBLEScan->clearResults();
		vTaskDelay(2000 / portTICK_PERIOD_MS);
	}
}

// Sender task: waits for messages from the queue and sends them out via Serial and Bluetooth.
void senderTask(void *param)
{
	Message msg;
	while (true)
	{
		if (xQueueReceive(sendQueue, &msg, portMAX_DELAY) == pdTRUE)
		{
			Serial.println(msg.message);
			SerialBT.println(msg.message);
		}
	}
}

// -----------------------
// Setup and Main Loop
// -----------------------
void setup()
{
	Serial.begin(115200);
	SerialBT.begin("Spokeduino");
#ifndef USE_TRANSISTOR
	// Only used in analog mode.
	analogReadResolution(11);
	analogSetAttenuation(ADC_6db);
#endif

	// Create a FreeRTOS queue for outgoing messages (holds up to 20 messages).
	sendQueue = xQueueCreate(20, sizeof(Message));

	// Set up gauge tasks for three gauges.
	static GaugeTaskParams gauge1Params = { 1, GAUGE1_CLOCK, GAUGE1_DATA };
	static GaugeTaskParams gauge2Params = { 2, GAUGE2_CLOCK, GAUGE2_DATA };
	static GaugeTaskParams gauge3Params = { 3, GAUGE3_CLOCK, GAUGE3_DATA };
	xTaskCreatePinnedToCore(gauge_task, "Gauge1Task", 2048, &gauge1Params, 1, NULL, 1);
	//xTaskCreatePinnedToCore(gauge_task, "Gauge2Task", 2048, &gauge2Params, 1, NULL, 1);
	//xTaskCreatePinnedToCore(gauge_task, "Gauge3Task", 2048, &gauge3Params, 1, NULL, 1);

	// Set up the digital inputs task.
	xTaskCreatePinnedToCore(digitalInputTask, "DigitalInputTask", 2048, NULL, 1, NULL, 1);

	// Set up the sender task (runs on core 0).
	xTaskCreatePinnedToCore(senderTask, "SenderTask", 2048, NULL, 1, NULL, 0);

	// Set up the BLE scanner task (runs on core 0).
	//xTaskCreatePinnedToCore(bleScannerTask, "BLEScannerTask", 4096, NULL, 1, NULL, 0);
}

void loop()
{
	// Main loop is unused; all work is done in tasks.
	vTaskDelay(1000 / portTICK_PERIOD_MS);
}