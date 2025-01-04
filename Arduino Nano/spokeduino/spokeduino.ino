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
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define GAUGE_TIMEOUT     90
#define GAUGE_MUXWAIT     16
#define SOFTWARE_VERSION 0.1

#define PIN_PEDAL    PD6
#define PIN_BTN_FUNC PD5
#define PIN_BTN_UP   PD4
#define PIN_BTN_DOWN PD3
#define PIN_BTN_GO   PD2

// The -14 converts the pin number to the ADC channel number
#define PIN_GAUGE1_CLOCK A0 - 14
#define PIN_GAUGE1_DATA  A1 - 14
#define PIN_GAUGE2_CLOCK A2 - 14
#define PIN_GAUGE2_DATA  A3 - 14
#define PIN_GAUGE3_CLOCK A6 - 14
#define PIN_GAUGE3_DATA  A7 - 14

// Coefficients for the quadratic function
static const float coefficient_a = -4.091e-7f;
static const float coefficient_b = 0.00163f;
static const float coefficient_c = 1.6497f;

//LiquidCrystal_I2C lcd(0x27, 16, 2);  // I2C address 0x27
LiquidCrystal_I2C lcd(0x27, 20, 2);  // I2C address 0x27

// Save the old deflection value to reduce LCD flickering and data transfer over the serial port
float gauge1_deflection_old = 0.1f;
float gauge2_deflection_old = 0.1f;
float gauge3_deflection_old = 0.1f;

/**
 * @brief Calculates tension from a deflection using a quadratic equation.
 *
 * The equation is: a*x^2 + b*x + (c - deflection) = 0 and is solved for x:
 * T = (-b + sqrt(b^2 -4a * (c - deflection))) / 2a
 *
 * @param deflection  The measured deflection (mm).
 * @param a           The quadratic coefficient a.
 * @param b           The quadratic coefficient b.
 * @param c           The quadratic coefficient c.
 *
 * @return float The tension in Newton. Returns 0.0 if the discriminant or the root are negative.
 */
float calculate_tension(float deflection, float a, float b, float c)
{
    float discriminant = b * b - 4 * a * (c - deflection);
    if (discriminant < 0)
        return 0.0f;  // No real roots

    float tension = (-b + sqrt(discriminant)) / (2 * a);  // Use the positive root
    return (tension > 0) ? tension : 0.0f;
}

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
 * @param gauge_number  Identifier for the gauge (for printing).
 * @param value         The gauge deflection value in mm.
 */
void send_gauge_value(const uint8_t gauge_number, float value)
{
    Serial.print(gauge_number);
    Serial.print(':');
    Serial.print(value);
    Serial.print('\n');
}

/**
 * @brief Displays the gauge deflection and tension on the second row of the LCD.
 *
 * @param deflection  The current gauge deflection in mm.
 * @param tension     The calculated tension in N.
 */
void display_main_gauge_value(float deflection, float tension)
{
    lcd.setCursor(0, 1);
    lcd.print(deflection, 2);
    lcd.print("mm ");
    lcd.print(tension, 0);
    lcd.print("N      ");
}

/**
 * @brief Runs the full job for a single gauge.
 *
 * Reads the gauge value, compares it to the old value, checks for a timeout,
 * sends updated data to the serial port and, for the first gauge, also the LCD.
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

    if (gauge_number != 1)
        return;

    display_main_gauge_value(deflection_value, calculate_tension(deflection_value, coefficient_a, coefficient_b, coefficient_c));
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
    pinMode(PIN_BTN_UP, INPUT_PULLUP);
    pinMode(PIN_BTN_DOWN, INPUT_PULLUP);
    pinMode(PIN_BTN_GO, INPUT_PULLUP);

    lcd.init();
    lcd.backlight();
    lcd.setCursor(0, 0);
    lcd.print("Sapim Race");
}


void loop()
{
    process_gauge(PIN_GAUGE1_CLOCK, PIN_GAUGE1_DATA, 1, gauge1_deflection_old);
    process_gauge(PIN_GAUGE2_CLOCK, PIN_GAUGE2_DATA, 2, gauge2_deflection_old);
    process_gauge(PIN_GAUGE3_CLOCK, PIN_GAUGE3_DATA, 3, gauge3_deflection_old);
    delay(50);
}