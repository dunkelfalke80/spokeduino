# Spokeduino

Spokeduino is a small Arduino-based spoke tensioning aid that reads deflections from cheap dial gauges (0–12.7 mm, 0.01 mm resolution) and computes the resulting spoke tension using a simple quadratic approximation. It was conceived primarily for measuring tension with a Toopre TL-P11 spoke tensiometer gauge, but can be adapted to other deflection-based gauges as well.
  
> **Note**  
> This project is based on [David Pilling's DialGauge code](https://www.davidpilling.com/wiki/index.php/DialGauge), used with explicit permission.
  
## Features

* **Three gauge inputs** (only the first is currently connected).
* **LCD display** showing the deflection and computed tension in N for the first gauge.
* **Serial output** for all connected gauges.
* **Quadratic calibration** for computing tension from measured deflection.
* **Expandable** to up to three dial gauges (cheap Aliexpress 0–12.7 mm, 0.01 mm).
* **Pedal and four buttons** are planned but not currently implemented.
  
## Hardware

* **Microcontroller:** Arduino Nano  
* **Display:** 20×2 I2C LCD (address `0x27`)
* **Buttons:** 4 push-buttons (not yet implemented in software)
* **Pedal:** 1 pedal input (not yet implemented in software)
* **Dial Gauges:** 
  - 3 × 0–12.7 mm, 0.01 mm resolution dial gauges from Aliexpress
  - Data, clock, and ground pins manually soldered to each gauge’s PCB
  - Currently only **Gauge 1** is physically connected
  - Gauge 1 is mounted in a Toopre TL-P11 spoke tensiometer
  
### Pin Assignments

| **Signal**    | **Arduino Pin** | **Purpose**         |
|---------------|-----------------|---------------------|
| `PIN_PEDAL`   | `PD6`           | Pedal input         |
| `PIN_BTN_FUNC`| `PD5`           | Function button     |
| `PIN_BTN_UP`  | `PD4`           | Increment button    |
| `PIN_BTN_DOWN`| `PD3`           | Decrement button    |
| `PIN_BTN_GO`  | `PD2`           | Go/confirm button   |
| Gauge1 Clock  | `A0`            | Read deflection (clock)  |
| Gauge1 Data   | `A1`            | Read deflection (data)   |
| Gauge2 Clock  | `A2`            | Read deflection (clock)  |
| Gauge2 Data   | `A3`            | Read deflection (data)   |
| Gauge3 Clock  | `A6`            | Read deflection (clock)  |
| Gauge3 Data   | `A7`            | Read deflection (data)   |

> **Note**  
> For analog pins, the code toggles ADMUX to treat them as inputs for the analog comparator.

## Getting Started

### Prerequisites

1. **Arduino IDE** (or a compatible environment like PlatformIO).
2. **Libraries**  
   - [LiquidCrystal_I2C](https://github.com/fdebrabander/Arduino-LiquidCrystal-I2C-library) (or equivalent I2C LCD library).
3. **Hardware**  
   - An Arduino Nano (or similar) set up as described.
   - One or more dial gauges manually soldered for data and clock output.
   - Optional: Pedal and buttons.
  
### Installation

1. **Clone or Download** this repository:   
```
    git clone https://github.com/dunkelfalke80/spokeduino.git
    cd spokeduino
```    
1. **Open in Arduino IDE**
  - Click File > Open.
  - Select the spokeduino.ino (or main.ino, if renamed) file inside this repository.
3. **Install Dependencies**
  - In Arduino IDE, open Tools > Manage Libraries…
  - Search for LiquidCrystal_I2C and install the library.
4. **Connect the Hardware as described in the Hardware section.**
5. **Upload**
  - Select your board type (e.g., Arduino Nano) and appropriate COM port.
  - For cheap Nano clones, you may need to select the “old bootloader” option.
  - Click Upload.

## Usage
- Power on the Arduino Nano with the connected gauge(s) and LCD. Zero the gauge.
- Clamp the tensiometer on a spoke.
- The deflection value in mm will be shown on the LCD. If the gauge is set to inches, the value will be converted to mm.
- Between approximately 400 and 1500 N, the displayed value should be quite accurate (within about 10% deviation, maybe even less). For values above or below that range, it is still a good estimate, but for values over about 1900 N, no reliable estimates are possible.

## Quadratic Calculation of Tension
Spokeduino uses a simple quadratic formula to approximate tension based on measured deflection:
> T = (-b + sqrt(b^2 -4a * (c - deflection))) / 2a

The coefficients can be tweaked to match the gauge’s calibration in the code:
```
    static const float coefficient_a = -4.091e-7f;
    static const float coefficient_b =  0.00163f;
    static const float coefficient_c =  1.6497f;
```
These values are specific to the Toopre TL-P11 for Sapim Race spokes. In the next version, there will be a database containing spoke calibrations for at least 10 models. Future database extensions will follow as soon as I add a FeRAM module, since the Arduino Nano’s EEPROM is not large enough.

## Project Status
* **Current:** Reading from the first gauge, displaying on LCD, and sending data via Serial.
* **Planned in the short term:**
  - Implement pedal and buttons functionality (to store readings, change modes, etc.).
  - Connect and fully integrate the second and third gauges.
  - Add a large database of spoke calibrations.
  - Switch between two spoke types on the fly (left/right).
* **Planned in the medium term:** Provide an interface to a Windows application that lets you select the spoke types (left/right), set target tension for each, show a tension diagram, allow the user to add new spokes to the database by entering calibration values either manually or semi-automatically.
* **Planned in the long term:** Extend the Windows application to show lateral and radial wheel deviation of the whole wheel and to implement dishing suggestions. Connection to the PC via Bluetooth.
* **Maybe some day:** Port the PC application to Linux and Android.

## Trademarks and Disclaimer
All product names, trademarks, and registered trademarks mentioned in this project are the property of their respective owners. References to these names are for identification purposes only and do not imply endorsement or affiliation.

## Contributing
Contributions are welcome. Feel free to open issues or pull requests. I am also open for new feature suggestions.  
You can also contribute by sending me one spoke of the type not yet in the database. Currently I can only measure J-bend spokes.  
Every contribution (including suggested features that will be implemented) will be acknowledged below.

## License
This project is licensed under the MIT License.  
Original code copyright © David Pilling.  
Used with explicit permission.  

## Acknowledgments
* **David Pilling** for the original dial gauge reading code.
* [**The Internet Community Bike forum**](https://www.mtb-news.de) ([project thread](https://www.mtb-news.de/forum/t/softwareunterstutzter-laufradbau-mit-gunstigen-bauteilen-von-aliexpress.993827/) )
* All contributors and testers who help improve this project:
  - The ICB user **Das_Proletariat** for the original inspiration.
  - The ICB user **Freaky-blue** for some feature suggestions that definitely will be implemented in time.
