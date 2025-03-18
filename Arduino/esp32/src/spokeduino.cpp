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
			String manufacturer_data = advertisedDevice.getManufacturerData();
            uint16_t company_id = ((uint8_t)manufacturer_data[1] << 8) | (uint8_t)manufacturer_data[0];
            if (manufacturer_data.length() >= 2 && company_id == WHC06_MANUFACTURER_ID)
            {
                // Big-endian bytes [12] and [13] absolute value
                uint16_t weight_raw = ((uint8_t)manufacturer_data[12] << 8) | (uint8_t)manufacturer_data[13];
                float weightKg = weight_raw / 100.0f;

                Message msg;
                snprintf(msg.message, sizeof(msg.message), "9:%.2f", weight_raw);
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
	// Waiting for the clock falling edge
	while (analogRead(clock_pin) > ADC_THRESHOLD)
	{
		if (millis() > timeout)
			return -1;
	}
    // Waiting for the clock rising edge
    while (analogRead(clock_pin) < ADC_THRESHOLD)
	{
		if (millis() > timeout)
			return -1;
	}
	// Read a bit
	int data = (analogRead(data_pin) > ADC_THRESHOLD) ? 1 : 0;
	return data;
}

/**
 * @brief Reads gauge value using ADC-based falling edge detection.
 *
 * Reads and parses a 24-bit packet into a gauge reading (deflection in mm).
 * The conversion uses only the lower 12 bits for the gauge value,
 * interprets bit 20 as the negative flag and bit 23 as the "inches" flag.
 *
 * @param clock_pin Analog pin number connected to gauge clock.
 * @param data_pin Analog pin number connected to gauge data.
 * @return Gauge value (mm, two decimals); -1000.0f on timeout.
 */
float read_gauge(uint8_t clock_pin, uint8_t data_pin)
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
				return -1000.0f;
			// Restart packet if a bit times out before overall timeout.
			bit_index = 0;
			packet = 0;
			continue;
		}
		packet |= ((long)(bit & 1)) << bit_index;
		bit_index++;
	}

    int gauge_val = packet & 0x0FFF;  // Lower 12 bits
	bool negative = (packet & (1 << 20)) != 0;
	bool inches   = (packet & (1 << 23)) != 0;
	int value = negative ? -gauge_val : gauge_val;
	if (inches)
		value = static_cast<int>((value / 2.0) * 2.54); // Strictly metric

	return static_cast<float>(value) / 100.0f;
}

/**
 * @brief Runs the full job for a single gauge.
 *
 * Reads the gauge value, compares it to the old value, checks for a timeout,
 * sends updated data to the send queue.
 *
 * @param clock_pin            The low channel
 * @param data_pin             The high channel
 * @param gauge_number         The number of the gauge (1, 2 or 3)
 * @param old_deflection_value The previous valid detection value reference
 */
void process_gauge(uint8_t clock_pin, uint8_t data_pin, const uint8_t gauge_number, float& old_deflection_value)
{
    float deflection_value = read_gauge(clock_pin, data_pin);
    // Skip timeouts and unchanged values
    if (deflection_value < -10.0f || deflection_value == old_deflection_value)
        return;

    // Timeout or garbage data
	if (deflection_value < MIN_VAL)
    {
        old_deflection_value = 0;
        return;
    }

    old_deflection_value = deflection_value;
    Message msg;
    snprintf(msg.message, sizeof(msg.message), "%d:%.2f", gauge_number, deflection_value);
    xQueueSend(send_queue, &msg, portMAX_DELAY);
}

/**
 * @brief Gauge reading task.
 *
 * Continuously reads from the gauges and posts updates if the value changes.
 *
 * @param *pvParameters  Standard FreeRTOS task parameters.
 */
void gauge_task(void *pvParameters)
{
    // Save the old values to reduce the data transfer over the serial port
    float gauge1_deflection_old = 0.1f;

    while (true)
    {
        process_gauge(PIN_GAUGE1_CLOCK, PIN_GAUGE1_DATA, 0, gauge1_deflection_old);
        vTaskDelay(pdMS_TO_TICKS(50));
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

void setup()
{
	Serial.begin(115200);
	SerialBT.begin("Spokeduino");
	// Only used in analog mode.
	analogReadResolution(11);
	analogSetAttenuation(ADC_6db);

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
	xTaskCreatePinnedToCore(bleScannerTask, "BLEScannerTask", 4096, NULL, 1, NULL, 0);
}

void loop()
{
	// Main loop is unused; all work is done in tasks.
	vTaskDelay(1000 / portTICK_PERIOD_MS);
}