# Spokeduino

Spokeduino is a small Arduino-based spoke tensioning aid that reads deflections from cheap dial gauges (0–12.7 mm, 0.01 mm resolution) and computes the resulting spoke tension using a simple quadratic approximation. It was conceived primarily for measuring tension with a Toopre TL-P11 spoke tensiometer gauge, but can be adapted to other deflection-based gauges as well.
  
> **Note**  
> This project is based on [David Pilling's DialGauge code](https://www.davidpilling.com/wiki/index.php/DialGauge), used with explicit permission.
  
## Features

* **Three gauge inputs** (only the first is currently connected).
* **Serial output** for all connected gauges.
* **Expandable** to up to three dial gauges (cheap Aliexpress 0–12.7 mm, 0.01 mm).
* **Pedal and two buttons**
  
## Hardware

* **Microcontroller:** Arduino Nano  
* **Buttons:** 2 push-buttons
* **Pedal:** 1 pedal input
* **Dial Gauges:** 
  - 3 × 0–12.7 mm, 0.01 mm resolution dial gauges from Aliexpress
  - Data, clock, and ground pins manually soldered to each gauge’s PCB
  
### Pin Assignments

| **Signal**    | **Arduino Pin** | **Purpose**         |
|---------------|-----------------|---------------------|
| `PIN_PEDAL`   | `PD6`           | Pedal input         |
| `PIN_BTN_FNC1`| `PD5`           | Function button     |
| `PIN_BTN_FNC2`| `PD4`           | Function  button    |
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
2. **Hardware**  
   - An Arduino Nano (or similar) set up as described.
   - One or more dial gauges manually soldered for data and clock output.
   - Pedal
   - Optional: buttons
  
### Installation

1. **Clone or Download** this repository:   
```
    git clone https://github.com/dunkelfalke80/spokeduino.git
    cd spokeduino
```    
1. **Open in Arduino IDE**
  - Click File > Open.
  - Select the spokeduino.ino (or main.ino, if renamed) file inside this repository.
2. **Connect the Hardware as described in the Hardware section.**
3. **Upload**
  - Select your board type (e.g., Arduino Nano) and appropriate COM port.
  - For cheap Nano clones, you may need to select the “old bootloader” option.
  - Click Upload.

## Usage
- Power on the Arduino Nano with the connected gauge(s) and LCD. Zero the gauge.
- Clamp the tensiometer on a spoke.
- The deflection value of each gauge in mm will be sent over the serial port. If the gauge is set to inches, the value will be converted to mm.

## Project Status
* **Current:**
- Reading from all three gauges
- Sending the data over the serial port
- Pedal and buttons
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
  - The ICB user **Freaky-blue** for feature suggestions that definitely will be implemented in time.
  - The ICB user **morph027** for adding the ZTTO TC-02 data
  - The ICB user **kinderzeitung** for the suggestion about different charges of the same spoke type
