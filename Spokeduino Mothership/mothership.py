import sys
import sqlite3
from PySide6.QtWidgets import QApplication, QMainWindow
from mothership_main_ui import Ui_mainWindow

class SpokeduinoApp(QMainWindow):
    """
    Main application class for Spokeduino Mothership.

    This class initializes the UI, connects signals and slots, and interacts with
    the SQLite database to populate and manage data displayed in the application.
    """
    def __init__(self) -> None:
        """
        Initialize the main application window.
        """
        super().__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.setup_signals_and_slots()
        self.database_path: str = "spokeduino.sqlite"
        self.load_manufacturers()

    def setup_signals_and_slots(self) -> None:
        """
        Connect UI elements to their respective slots (event handlers).
        """
        self.ui.pushButtonCreateNewSpoke.clicked.connect(self.button_create_new_spoke_onclick)

    def button_create_new_spoke_onclick(self) -> None:
        """
        Handle the "Create New Spoke" button click event.

        This is a placeholder for the actual implementation.
        """
        print("Create New Spoke button")

    def load_manufacturers(self) -> None:
        """
        Load all manufacturer names from the database and populate the
        comboBoxSelectSpokeManufacturerDatabase dropdown.
        """
        try:
            connection: sqlite3.Connection = sqlite3.connect(self.database_path)
            cursor: sqlite3.Cursor = connection.cursor()

            cursor.execute("SELECT name FROM manufacturers")
            manufacturers = cursor.fetchall()

            self.ui.comboBoxSelectSpokeManufacturerDatabase.clear()
            for manufacturer in manufacturers:
                self.ui.comboBoxSelectSpokeManufacturerDatabase.addItem(manufacturer[0])

            connection.close()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

def main() -> None:
    """
    Entry point for the Spokeduino Mothership application.

    Initializes the QApplication and the main application window.
    """
    app = QApplication(sys.argv)
    window = SpokeduinoApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
