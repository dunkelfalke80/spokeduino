#include <pins_arduino.h>
#include "Adafruit_TinyUSB.h"
#include "nrf.h"
#include "delay.h"
#include <math.h>

#include <Arduino.h>
#include <FreeRTOS.h>

// Digital pins used for the short detection test
#define PIN_DIGITAL_1  PIN_009
#define PIN_DIGITAL_2  PIN_010

float randomFloat(float min_val, float max_val)
{
    return min_val + (static_cast<float>(random(0, 1000) / 1000.0f) * (max_val - min_val));
}

void gaugeSimulatorTask(void* pvParameters)
{
    (void) pvParameters;
    char buffer[64];
    while (true)
    {
        float value = randomFloat(2.55f, 3.12f);
        snprintf(buffer, sizeof(buffer), "1:%.2f", value);
        Serial.println(buffer);
        vTaskDelay(pdMS_TO_TICKS(1000));  // Delay for 1 second
    }
}

// Task: Every 5 seconds, send a "9:" message with a random value between 90.22 and 100.53.
void bleSimulatorTask(void* pvParameters)
{
    char buffer[64];
    while (true)
    {
        float value = randomFloat(90.22f, 100.53f);
        snprintf(buffer, sizeof(buffer), "9:%.2f", value);
        Serial.println(buffer);
        vTaskDelay(pdMS_TO_TICKS(5000));  // Delay for 5 seconds
    }
}

void digitalInputSimulatorTask(void *pvParameters)
{
    bool previously_shorted = false;    
    while (true)
    {
        int reading = digitalRead(PIN_DIGITAL_2);
        bool currently_shorted = (reading == HIGH);
        if (currently_shorted && !previously_shorted)
        {
            Serial.println("6:1");
            previously_shorted = true;
        }
        else if (!currently_shorted)
        {
            previously_shorted = false;
        }
        vTaskDelay(pdMS_TO_TICKS(50));
    }
}

void setup()
{
    Serial.begin(115200);    
    randomSeed(analogRead(PIN_031));    
    pinMode(PIN_DIGITAL_1, OUTPUT);
    pinMode(PIN_DIGITAL_2, INPUT_PULLDOWN);
    digitalWrite(PIN_DIGITAL_1, HIGH);
    xTaskCreate(gaugeSimulatorTask, "GaugeSim", 2048, NULL, 1, NULL);
    xTaskCreate(bleSimulatorTask, "BLESim", 2048, NULL, 1, NULL);
    xTaskCreate(digitalInputSimulatorTask, "DigitalSim", 2048, NULL, 1, NULL);
}

void loop()
{    
    vTaskDelay(pdMS_TO_TICKS(1000));
}
