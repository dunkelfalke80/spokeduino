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
#include <pins_arduino.h>
#include <avr/builtins.h>
#include <math.h>
#include <stdarg.h>

#define GAUGE_TIMEOUT     90
#define GAUGE_MUXWAIT     16
#define SOFTWARE_VERSION 0.2

#define PIN_PEDAL     PD6
#define PIN_BTN_FUNC  PD5
#define PIN_BTN_FUNC2 PD4

// The -14 converts the pin number to the ADC channel number
#define PIN_GAUGE1_CLOCK A0 - 14
#define PIN_GAUGE1_DATA  A1 - 14
#define PIN_GAUGE2_CLOCK A2 - 14
#define PIN_GAUGE2_DATA  A3 - 14
#define PIN_GAUGE3_CLOCK A6 - 14
#define PIN_GAUGE3_DATA  A7 - 14

// Save the old values to reduce the data transfer over the serial port
float gauge1_deflection_old = 0.1f;
float gauge2_deflection_old = 0.1f;
float gauge3_deflection_old = 0.1f;

int pedal_value_old = 0;
int btn_func_value_old = 0;
int btn_func2_value_old = 0;

/**
 * @brief Reads the gauge by toggling ADMUX between two channels
 * @author Original code by David Pilling, extracted to a function for multiple gauges support
 *
 * @param admux_channel_a The low channel to wait for a falling edge
 * @param admux_channel_b The high channel to check whether the comparator is low
 * @param timeout         The maximum time (ms) to wait for a falling edge on each bit
 *
 * @return float Gauge value in mm, two decimal places; -1000.0 on timeout
 */
float read_gauge(const uint8_t admux_channel_a, const uint8_t admux_channel_b, unsigned long timeout)
{
    int val = 0;
    int oldval = 0;
    int outputval = 0;
    int shift = 0;

    unsigned long looptime = millis();
    bool inches = false;
    bool negative = false;

    while (shift < 24)
    {
        // Phase A: set ADMUX to Channel A, wait for the comparator falling edge
        ADMUX = admux_channel_a;
        __builtin_avr_delay_cycles(GAUGE_MUXWAIT);
        val = (ACSR & (1 << ACO)); // Read comparator

        while (true)
        {
            oldval = val;
            val = (ACSR & (1 << ACO));
            // Falling edge detection: was HIGH, now LOW
            if (!val && oldval)
                break;

            // Timed out waiting for falling edge
            if ((millis() - looptime) > timeout)
                return -1000.0f;
        }

        // Phase B: set ADMUX to Channel B, set the bit if the comparator is LOW
        ADMUX = admux_channel_b;
        __builtin_avr_delay_cycles(GAUGE_MUXWAIT);
        val = (ACSR & (1 << ACO));

        if (!val)  // If comparator is LOW
        {
            if (shift < 12)
                outputval |= (1 << shift);

            if (shift == 23)
                inches = true;

            if (shift == 20)
                negative = true;
        }

        shift++;
    }

    // Interpret the bitfield
    int value = (negative ? -outputval : outputval);
    if (inches)
        value = static_cast<int>((value / 2.0) * 2.54); // Strictly metric

    // Convert to float mm with two decimal places
    return static_cast<float>(value) / 100.0f;
}

/**
 * @brief Sends the gauge value to the serial output.
 *
 * @param gauge_number      Identifier for the gauge (1, 2 or 3)
 * @param deflection_value  The gauge deflection value in mm.
 */
void send_gauge_value(const uint8_t gauge_number, float deflection_value)
{
    Serial.print(gauge_number);
    Serial.print(':');
    Serial.print(deflection_value);
    Serial.print('\n');
}

/**
 * @brief Sends an input status value to the serial output.
 *
 * @param input_number      Identifier for the digital input
 * @param value             The gauge deflection value in mm.
 */
void send_input_value(const uint8_t pin_number, int value)
{
    Serial.print(pin_number);
    Serial.print(':');
    Serial.print(value);
    Serial.print('\n');
}

/**
 * @brief Runs the full job for a single gauge.
 *
 * Reads the gauge value, compares it to the old value, checks for a timeout,
 * sends updated data to the serial port.
 *
 * @param admux_channel_a      The low channel
 * @param admux_channel_b      The high channel
 * @param gauge_number         The number of the gauge (1, 2 or 3)
 * @param old_deflection_value The previous valid detection value reference
 */
void process_gauge(const uint8_t admux_channel_a, const uint8_t admux_channel_b, const uint8_t gauge_number, float& old_deflection_value)
{
    float deflection_value = read_gauge(admux_channel_a, admux_channel_b, GAUGE_TIMEOUT);

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
 * sends updated data to the serial port and.
 *
 * @param pin_number  The number of the pin
 * @param old_value   The previous valid detection value reference
 */
void process_pin(const uint8_t pin_number, int& old_value)
{
    int value = digitalRead(pin_number);

    // Skip unchanged values
    if (value == old_value)
        return;

    old_value = value;
    send_input_value(pin_number, value);
}

/**
 * @brief Initializes the hardware and peripherals.
 *
 * Sets up serial communication and digital inputs, disables default ADC,
 * enables the comparator, and initializes the LCD display.
 */
void setup()
{
    Serial.begin(9600);

    ADCSRA = 0;            // ADC Control and Status Register A
    ADCSRB = (1 << ACME);  // Enable muliplxer
    ADMUX = 0;             // ADC Multiplexer Selection Register
    ACSR = (1 << ACBG);    // Analog Comparator Bandgap Select

    // Enable the internal pullup resistor for all controller inputs
    pinMode(PIN_PEDAL, INPUT_PULLUP);
    pinMode(PIN_BTN_FUNC, INPUT_PULLUP);
    pinMode(PIN_BTN_FUNC2, INPUT_PULLUP);

    // Reset all checked digital input values
    pedal_value_old = digitalRead(PIN_PEDAL);
    btn_func_value_old = digitalRead(PIN_BTN_FUNC);
    btn_func2_value_old = digitalRead(PIN_BTN_FUNC2);
}


void loop()
{
    process_pin(PIN_PEDAL, pedal_value_old);
    process_pin(PIN_BTN_FUNC, btn_func_value_old);
    process_pin(PIN_BTN_FUNC2, btn_func2_value_old);
    process_gauge(PIN_GAUGE1_CLOCK, PIN_GAUGE1_DATA, 0, gauge1_deflection_old);
    process_gauge(PIN_GAUGE2_CLOCK, PIN_GAUGE2_DATA, 1, gauge2_deflection_old);
    process_gauge(PIN_GAUGE3_CLOCK, PIN_GAUGE3_DATA, 2, gauge3_deflection_old);
    delay(50);
}