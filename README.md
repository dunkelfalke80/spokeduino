# Spokeduino

**Spokeduino** a small Arduino-based (PlatformIO) wheel building aid that reads deflections from cheap dial gauges (0–12.7 mm, 0.01 mm resolution), BLE crane scales and foot pedals and functions as a hub for the Spokeduino mothership application

When connected, Spokeduino automatically feeds live values into the appropriate cells.
The foot pedal triggers Next in measurement/tensioning mode.
The software can detect toggle and ignore unchanged readings to reduce noise.

## Supported Hardware

| Feature                          | ESP32              | Arduino Nano  |
|----------------------------------|--------------------|---------------|
| Wired gauge support              | yes                | yes           |
| Wired pedal support              | yes                | yes           |
| Bluetooth Serial (SPP)           | yes                | no            |
| BLE WH-C06 Scale                 | yes                | no            |
| Multi-threaded task handling     | yes (FreeRTOS)     | no            |

## Wiring Instructions

### Gauge Connection
For gauges with a Micro-USB style port: **White = Clock (D-), Green = Data (D+)**

#### ESP32
| Gauge # | Line  | MCU Pin |
|---------|-------|---------|
| 1       | Clock | GPIO14  |
| 1       | Data  | GPIO12  |
| 2       | Clock | GPIO32  |
| 2       | Data  | GPIO33  |
| 3       | Clock | GPIO25  |
| 3       | Data  | GPIO26  |

#### Arduino Nano
| Gauge # | Line  | MCU Pin |
|---------|-------|---------|
| 1       | Clock | A0      |
| 1       | Data  | A1      |
| 2       | Clock | A2      |
| 2       | Data  | A3      |
| 3       | Clock | A6      |
| 3       | Data  | A7      |

### Pedal Connection

#### ESP32
| Pedal   | Line  | MCU Pin |
|---------|-------|---------|
| 1       | 1     | GPIO13  |
| 1       | 2     | GND     |

#### Arduino Nano
| Pedal   | Line  | MCU Pin |
|---------|-------|---------|
| 1       | 1     | PD6     |
| 1       | 2     | GND     |

### Using Without Spokeduino
All features except automatic data input work without the microcontroller. You can:

* Manually enter measurements
* Fit curves and plot graphs
* Simulate wheel tensioning
* Export and store data locally

## License
MIT License. Developed by Roman Galperin, 2025.
Original code copyright © David Pilling.  
Used with explicit permission.  

# Spokeduino Mothership

**Spokeduino Mothership** is a desktop application for measuring spoke tension, visualizing tension-deflection curves, and guiding wheel building through real-time feedback. It can function standalone or integrate with a connected Spokeduino device (e.g., ESP32 or Arduino Nano).

## Features

* Manage spoke database (types, dimensions, metadata)
* Record tension/deflection measurements
* Fit and visualize measurement curves
* Convert units between Newton, kgF, and lbF
* Generate real-time radar charts for wheel tensioning
* Automatic data input from the tensiometer gauge
* Automatic data input from the Lateral and radial deflection gauges (not yet fully implemented)
* Bluetooth support for BLE scales (ESP32 only)
* Pedal input for hands-free data entry

## Short user manual

### Software Setup

* Requires **Python 3.10+**
* Uses **PySide6** for GUI and **PyQtGraph** for plots

### Install Requirements

```bash
pip install -r requirements.txt
```

### Run Application

```bash
python mothership.py
```

### Getting Started
On first launch, a database is initialized with standard manufacturers and spoke types.
Connect your Spokeduino device (if available) and select the appropriate serial port under Setup → Spokeduino Port.
You can operate the software entirely without Spokeduino, by manually entering measurements.

### Spokes Tab – Managing spokes
Use the "Spokes" tab to:

* View, filter, and search for spokes by name, type, or gauge.
* Create new spokes with full metadata (name, type, gauge, weight, dimensions, comment).
* Assign manufacturers or create new ones on the fly.
* View saved measurements associated with a spoke.

> Use the “Use on the left/right” buttons to assign a spoke to one side of the wheel for tensioning later.

### Measurements Tab – Measuring spokes
This tab allows you to record tension/deflection pairs from either:
* Manual input (default or custom mode)
* Spokeduino foot pedal, BLE crane scale connection and live deflection input can be used for hands-free workflow

Modes:
* Default: Select tensiometers and enter deflection for predefined tension levels.
* Edit: Modify an existing measurement set.
* Custom: Enter free-form tension/deflection pairs.

Features:
* Automatic unit conversion (N, kgF, lbF)
* Fit selection (e.g., quadratic, spline)
* Curve visualization and deviation analysis
* Automatic progression using keyboard or foot pedal

> Add a comment before saving a measurement. Each measurement is tied to a specific spoke and tensiometer.

### Tensioning Tab – Tensioning a wheel
This is your virtual tensioning workspace:

* Define left/right spoke counts
* Set target tension for each side
* Choose clockwise or counterclockwise rotation
* Define measurement sequence (Left→Right, Right→Left, Side-by-side)

Radar Chart:
* Shows current tensions
* Draws reference targets as dashed polygons
* Visualizes deviation from goal in real time
* Spokeduino foot pedal and live deflection input can be used for hands-free workflow

### Settings and Customization <a name="settings-and-customization"></a>
Available in the Setup tab:

* Language (multi-language support with .qm files)
* Unit system
* Spokeduino port and toggle
* Tensiometer selection
* Measurement behavior:
    - Direction (up/down)
    - Fit curve
    - Entry type (default/custom)
    - Sequence type (Left-Right, etc.)

> All settings persist via the internal SQLite database.

### Fit Types and Curve Fitting
Curve fitting transforms raw tension/deflection data into analytical models.

Supported fits:

* Linear
* Quadratic, Cubic, Quartic
* Spline (natural cubic)
* Exponential
* Logarithmic
* Power Law

Each fit is used to:

* Render the main curve (blue line)
* Overlay measured points (red dots)
* Plot deviations (green markers) on a secondary Y-axis

> Extrapolation is limited and controlled for each fit type to prevent nonsense predictions.

### Help
See the in-app Help menu for step-by-step instructions on measuring spokes and building wheels.

## License

MIT License. Developed by Roman Galperin, 2025.

## Trademarks and Disclaimer
All product names, trademarks, and registered trademarks mentioned in this project are the property of their respective owners. References to these names are for identification purposes only and do not imply endorsement or affiliation.

## Contributing
Contributions are welcome. Feel free to open issues or pull requests. I am also open for new feature suggestions.  
You can also contribute by sending me one spoke of the type not yet in the database. Currently I can only measure J-bend spokes.  
Every contribution (including suggested features that will be implemented) will be acknowledged below.

## Acknowledgments
* **David Pilling** for the original dial gauge reading code.
* [**The Internet Community Bike forum**](https://www.mtb-news.de) ([project thread](https://www.mtb-news.de/forum/t/softwareunterstutzter-laufradbau-mit-gunstigen-bauteilen-von-aliexpress.993827/) )
* All contributors and testers who help improve this project:
  - The ICB user **Das_Proletariat** for the original inspiration.
  - The ICB user **Freaky-blue** for feature suggestions that definitely will be implemented in time.
  - The ICB user **morph027** for adding the ZTTO TC-02 data
  - The ICB user **kinderzeitung** for the suggestion about different charges of the same spoke type
