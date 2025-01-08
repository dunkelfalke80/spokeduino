import sqlite3
import serial

from typing import List


def create_database(db_name: str) -> None:
    """
    Creates the SQLite database and tables if they do not exist.

    Args:
        db_name (str): The name of the SQLite database file.
    """
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()

        # Create manufacturer table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS manufacturers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
            """
        )

        # Create measurements table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS measurements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                manufacturer_id INTEGER NOT NULL,
                name TEXT,
                description TEXT,
                tension REAL,
                deflection REAL,
                FOREIGN KEY (manufacturer_id) REFERENCES manufacturers (id)
            )
            """
        )


def main() -> None:
    """
    Main function to read deflection measurements from a serial port
    and save the results to a SQLite database.
    """
    db_name: str = "measurements.db"
    create_database(db_name)

    port_name: str = "COM3"
    baud_rate: int = 9600

    # Ask for manufacturer and measurement details
    manufacturer_name: str = input("Enter the manufacturer name: ").strip()

    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()

        # Check if manufacturer already exists
        cursor.execute(
            "SELECT id FROM manufacturers WHERE LOWER(name) = LOWER(?)",
            (manufacturer_name,)
        )
        result = cursor.fetchone()

        if result is not None:
            manufacturer_id: int = result[0]
            print(f"Manufacturer '{manufacturer_name}' "
                  f"already exists with ID {manufacturer_id}.")
        else:
            # Insert manufacturer
            cursor.execute(
                "INSERT INTO manufacturers (name) VALUES (?)",
                (manufacturer_name,)
            )
            manufacturer_id: int = cursor.lastrowid
            print(f"Manufacturer '{manufacturer_name}' "
                  f"added with ID {manufacturer_id}.")
            conn.commit()

        # Ask for measurement details
        spoke_name: str = input("Enter spoke name: ").strip()
        spoke_description: str = input("Enter spoke description: ").strip()

        # Initialize serial port
        with serial.Serial(port_name, baud_rate, timeout=1) as serial_port:
            serial_port.reset_input_buffer()

            tensions: List[float] = [
                1500, 1400, 1300, 1200, 1100, 1000,
                900, 800, 700, 600, 500, 400
            ]
            index: int = 0

            while index < len(tensions):
                print(f"Set to {tensions[index]} N, "
                      "press pedal when ready.")
                deflection: float = 0.0

                while True:
                    try:
                        # Read a line from the serial port
                        data: str = serial_port.readline().decode("ascii")
                        parts: List[str] = data.split(":")

                        if len(parts) != 2:
                            continue
                        print(f"{deflection:.2f} mm", end="\r")
                        # First gauge
                        if parts[0][0] == "1":
                            deflection = float(parts[1])
                            print(f"{deflection:.2f} mm", end="\r")
                        # Pedal pressed
                        elif parts[0][0] == "6" and parts[1][0] == "0":
                            # Insert measurement into database
                            cursor.execute(
                                """
                                INSERT INTO
                                    measurements
                                    (
                                        manufacturer_id,
                                        name,
                                        description,
                                        tension,
                                        deflection
                                    )
                                VALUES (?, ?, ?, ?, ?)
                                """,
                                (
                                    manufacturer_id,
                                    spoke_name,
                                    spoke_description,
                                    tensions[index],
                                    deflection
                                )
                            )
                            conn.commit()
                            print(f"{tensions[index]} N = {deflection:.2f} mm")
                            index += 1
                            break

                    except ValueError as ve:
                        print(f"Error parsing data: {data}: {ve}")
                    except serial.SerialException as se:
                        print(f"Serial communication error: {se}")
                    except Exception as ex:
                        print(f"Unexpected error: {ex}")


if __name__ == "__main__":
    main()
