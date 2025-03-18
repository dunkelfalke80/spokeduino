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

// Configuration constants
#define ADC_THRESHOLD       1100         // Only used in analog mode
#define BIT_READ_TIMEOUT    100          // Timeout for a single bit (ms)
#define PACKET_READ_TIMEOUT 250          // Overall timeout for a 24-bit packet (ms)

// Digital input pins for pedals
#define PIN_PEDAL      13

// Gauge clock and data pins
// For the gauges with a MicroUSB connector the pinout is white (D-) = clock, green (D+) = data
#define PIN_GAUGE1_CLOCK   14
#define PIN_GAUGE1_DATA    12
#define PIN_GAUGE2_CLOCK   32
#define PIN_GAUGE2_DATA    33
#define PIN_GAUGE3_CLOCK   25
#define PIN_GAUGE3_DATA    26

// Hysteresis filter: maximum allowed change (in mm) between successive filtered readings.
#define MAX_DELTA 1.0f

// Minimum value filter: discard data lower than this (gauge is not in use)
#define MIN_VAL 0.6f

// BLE-related Constants
#define WHC06_MANUFACTURER_ID 256
#define WEIGHT_OFFSET         32  // Offset in manufacturer data for weight

const int ble_scan_time = 5;         // BLE scan time in seconds

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
QueueHandle_t send_queue = NULL;

// BLE Advertisement Callback
class WHC06AdvertisedDeviceCallbacks : public BLEAdvertisedDeviceCallbacks
{
	void onResult(BLEAdvertisedDevice advertisedDevice)
	{
		if (advertisedDevice.haveManufacturerData())
		{
			String  manufacturerData = advertisedDevice.getManufacturerData();
			//if (manufacturerData.size() < WEIGHT_OFFSET + 2) return;
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
				xQueueSend(send_queue, &msg, portMAX_DELAY);
			}
		}
	}
};


/**
 * @brief Reads one bit from a gauge’s clock and data lines.
 *      In analog mode, it uses analogRead() with a threshold.
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
	while (analogRead(clock_pin) > ADC_THRESHOLD)
	{
		if (millis() > timeout)
			return -1;
	}
    while (analogRead(clock_pin) < ADC_THRESHOLD)
	{
		if (millis() > timeout)
			return -1;
	}
	// Analog mode: use analogRead() with a threshold.
	int data = (analogRead(data_pin) > ADC_THRESHOLD) ? 1 : 0;
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
void gauge_task(void *param)
{
    float last_value = 0.0f;      // Stores the last accepted value
	while (true)
	{
        vTaskDelay(50 / portTICK_PERIOD_MS);
        long packet = get_gauge_packet(PIN_GAUGE1_CLOCK, PIN_GAUGE1_DATA);
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
        if ((delta_value < 0.01) || ((delta_value > MAX_DELTA) && (value > 0.5)))
            continue;

        last_value = value;
        Message msg;
		snprintf(msg.message, sizeof(msg.message), "1:%.2f", value);
		xQueueSend(send_queue, &msg, portMAX_DELAY);
	}
}

/**
 * @brief Runs the full job for a single digital input.
 *
 * Reads the input value, compares it to the old value,
 * sends updated data to the send queue on a full toggle.
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
        Message msg;
		snprintf(msg.message, sizeof(msg.message), "6:%.2f", value);
		xQueueSend(send_queue, &msg, portMAX_DELAY);
    }
    else
    {
        toggle_value = true;
    }
}

/**
 * @brief Digital inputs task.
 *
 * Continuously reads from digital inputs (pedals, buttons) and posts updates if the value changes.
 *
 * @param *pvParameters  Standard FreeRTOS task parameters.
 */
void input_task(void *pvParameters)
{
    // Save the old values to reduce the data transfer over the serial port
    int pedal_value_old = 0;
    bool pedal_value_toggle = false;

    pinMode(PIN_PEDAL, INPUT_PULLUP);
    pedal_value_old = digitalRead(PIN_PEDAL);

    while (true)
    {
        process_pin(PIN_PEDAL, pedal_value_old, pedal_value_toggle);
        vTaskDelay(pdMS_TO_TICKS(10));
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
		pBLEScan->start(ble_scan_time, false);
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
		if (xQueueReceive(send_queue, &msg, portMAX_DELAY) == pdTRUE)
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
#ifndef USE_SCHMITT_TRIGGER
	// Only used in analog mode.
	analogReadResolution(11);
	analogSetAttenuation(ADC_6db);
#endif

	// Create a FreeRTOS queue for outgoing messages (holds up to 20 messages).
	send_queue = xQueueCreate(20, sizeof(Message));

	xTaskCreatePinnedToCore(gauge_task, "Gauge1Task", 2048, NULL, 1, NULL, 1);
	//xTaskCreatePinnedToCore(gauge_task, "Gauge2Task", 2048, &gauge2Params, 1, NULL, 1);
	//xTaskCreatePinnedToCore(gauge_task, "Gauge3Task", 2048, &gauge3Params, 1, NULL, 1);

	// Set up the digital inputs task.
	xTaskCreatePinnedToCore(input_task, "InputTask", 2048, NULL, 1, NULL, 1);

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