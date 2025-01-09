import sys
import sqlite3
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt, QAbstractTableModel
from mothership_main_ui import Ui_mainWindow

class SpokeduinoTableModel(QAbstractTableModel):
    """
    Table model for displaying spokes data in a QTableView.
    """
    def __init__(self, data: list[list[str]], headers: list[str]) -> None:
        super().__init__()
        self._data = data
        self._headers = headers

    def rowCount(self, parent=None) -> int:
        return len(self._data)

    def columnCount(self, parent=None) -> int:
        return len(self._headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]
        return None

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
        self.ui.comboBoxSelectSpokeManufacturerDatabase.currentIndexChanged.connect(self.load_spokes_for_selected_manufacturer)

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

            cursor.execute("SELECT id, name FROM manufacturers")
            manufacturers = cursor.fetchall()

            self.ui.comboBoxSelectSpokeManufacturerDatabase.clear()
            self.ui.comboBoxSelectSpokeManufacturerDatabase.addItem("Select Manufacturer", -1)
            for manufacturer in manufacturers:
                self.ui.comboBoxSelectSpokeManufacturerDatabase.addItem(manufacturer[1], manufacturer[0])

            connection.close()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def load_spokes_for_selected_manufacturer(self) -> None:
        """
        Load all spokes for the currently selected manufacturer and populate the
        tableViewSpokesDatabase.
        """
        manufacturer_id = self.ui.comboBoxSelectSpokeManufacturerDatabase.currentData()

        if manufacturer_id == -1:
            # Clear the table if no manufacturer is selected
            self.ui.tableViewSpokesDatabase.setModel(None)
            return

        try:
            connection: sqlite3.Connection = sqlite3.connect(self.database_path)
            cursor: sqlite3.Cursor = connection.cursor()

            query = (
                "SELECT name, gauge, weight, dimensions, comment "
                "FROM spokes WHERE manufacturer_id = ?"
            )
            cursor.execute(query, (manufacturer_id,))
            spokes = cursor.fetchall()

            headers = ["Name", "Gauge", "Weight", "Dimensions", "Comment"]
            model = SpokeduinoTableModel(spokes, headers)
            self.ui.tableViewSpokesDatabase.setModel(model)

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
