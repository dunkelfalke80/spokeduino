import sys
import sqlite3
from PySide6.QtCore import Qt
from PySide6.QtCore import QAbstractTableModel
from PySide6.QtCore import QModelIndex
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QHeaderView
from PySide6.QtWidgets import QAbstractItemView
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

    def headerData(self, section: int, orientation: Qt.Orientation,
                   role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers[section]
        return None


class SpokeduinoApp(QMainWindow):
    """
    Main application class for Spokeduino Mothership.

    This class initializes the UI, connects signals and slots,
    and interacts with the SQLite database to populate and
    manage data displayed in the application.
    """
    def __init__(self) -> None:
        """
        Initialize the main application window.
        """
        super().__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.setup_signals_and_slots()
        self.db_path: str = "spokeduino.sqlite"
        self.current_spokes: list[list[str]] = []  # Store current spokes data
        self.load_manufacturers()

    def setup_signals_and_slots(self) -> None:
        """
        Connect UI elements to their respective slots (event handlers).
        """
        self.ui.pushButtonCreateNewSpoke.clicked.connect(self.create_new_spoke)
        self.ui.pushButtonEditSpoke.clicked.connect(self.edit_spoke)
        self.ui.pushButtonDeleteSpoke.clicked.connect(self.delete_spoke)
        self.ui.pushButtonNewManufacturerDatabase.clicked.connect(
            self.create_new_manufacturer)

        self.ui.lineEditNewManufacturerDatabase.textChanged.connect(
            self.toggle_new_manufacturer_button)
        self.ui.lineEditNewSpokeName.textChanged.connect(
            self.toggle_spoke_buttons)
        self.ui.comboBoxSelectNewSpokeType.currentIndexChanged.connect(
            self.toggle_spoke_buttons)
        self.ui.lineEditNewSpokeGauge.textChanged.connect(
            self.toggle_spoke_buttons)
        self.ui.lineEditNewSpokeWeight.textChanged.connect(
            self.toggle_spoke_buttons)
        self.ui.lineEditNewSpokeDimension.textChanged.connect(
            self.toggle_spoke_buttons)

    def load_manufacturers(self) -> None:
        """
        Load all manufacturer names from the database and populate the
        the dropdowns. Automatically loads spokes for the first manufacturer.
        """
        try:
            connection: sqlite3.Connection = sqlite3.connect(self.db_path)
            cursor: sqlite3.Cursor = connection.cursor()

            # Load manufacturers
            cursor.execute("SELECT id, name FROM manufacturers")
            manufacturers = cursor.fetchall()

            combo_manufacturer = \
                self.ui.comboBoxSelectSpokeManufacturerDatabase

            combo_manufacturer.clear()
            for manufacturer in manufacturers:
                combo_manufacturer.addItem(manufacturer[1], manufacturer[0])

            # Load spoke types
            cursor.execute("SELECT id, type FROM types")
            spoke_types = cursor.fetchall()

            self.ui.comboBoxSelectNewSpokeType.clear()
            for spoke_type in spoke_types:
                self.ui.comboBoxSelectNewSpokeType.addItem(
                    spoke_type[1], spoke_type[0])

            connection.close()

            # Automatically load spokes for the first manufacturer
            if manufacturers:
                combo_manufacturer.setCurrentIndex(0)
                self.load_spokes_for_selected_manufacturer()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def load_spokes_for_selected_manufacturer(self) -> None:
        """
        Load all spokes for the currently selected manufacturer and populate
        the tableViewSpokesDatabase and comboBoxSelectSpoke.
        """
        manufacturer_id = \
            self.ui.comboBoxSelectSpokeManufacturerDatabase.currentData()

        try:
            connection: sqlite3.Connection = \
                sqlite3.connect(self.db_path)
            cursor: sqlite3.Cursor = connection.cursor()

            query = (
                "SELECT "
                "s.name, t.type, s.gauge, s.weight, "
                "s.dimensions, s.comment, s.id "
                "FROM spokes s "
                "JOIN types t ON s.type_id = t.id "
                "WHERE s.manufacturer_id = ?"
            )
            cursor.execute(query, (manufacturer_id,))
            spokes = cursor.fetchall()

            headers = [
                "Name",
                "Type",
                "Gauge",
                "Weight",
                "Dimensions",
                "Comment"]
            # Exclude ID
            self.current_spokes = [list(spoke[:-1]) for spoke in spokes]
            model = SpokeduinoTableModel(self.current_spokes, headers)
            self.ui.tableViewSpokesDatabase.setModel(model)

            # Populate comboBoxSelectSpoke
            self.ui.comboBoxSelectSpoke.clear()
            for spoke in spokes:
                # Name and ID
                self.ui.comboBoxSelectSpoke.addItem(spoke[0], spoke[-1])

            # Adjust column widths
            header = self.ui.tableViewSpokesDatabase.horizontalHeader()
            # reducing line length
            rm = QHeaderView.ResizeMode
            # Name
            header.setSectionResizeMode(0, rm.Stretch)
            # Type
            header.setSectionResizeMode(1, rm.Stretch)
            # Gauge
            header.setSectionResizeMode(2, rm.ResizeToContents)
            # Weight
            header.setSectionResizeMode(3, rm.ResizeToContents)
            # Dimensions
            header.setSectionResizeMode(4, rm.Stretch)
            # Comment
            header.setSectionResizeMode(5, rm.Stretch)

            self.ui.tableViewSpokesDatabase.setSelectionBehavior(
                QAbstractItemView.SelectionBehavior.SelectRows)
            connection.close()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def sort_by_column(self, column: int) -> None:
        """
        Sort the tableViewSpokesDatabase by the specified column.
        """
        self.current_spokes.sort(key=lambda x: x[column])
        self.ui.tableViewSpokesDatabase.model().layoutChanged.emit()

    def select_spoke_from_table(self, index: QModelIndex) -> None:
        """
        Select the corresponding spoke in comboBoxSelectSpoke
        when a row is clicked.
        """
        row = index.row()
        spoke_name = self.current_spokes[row][0]
        self.ui.comboBoxSelectSpoke.setCurrentText(spoke_name)

    def select_spoke_row(self) -> None:
        """
        Select the corresponding row in tableViewSpokesDatabase
        when a spoke is selected in comboBoxSelectSpoke.
        """
        spoke_id = self.ui.comboBoxSelectSpoke.currentData()
        if spoke_id is None:
            self.ui.tableViewSpokesDatabase.clearSelection()
            return

        for row, spoke in enumerate(self.current_spokes):
            if spoke_id == self.ui.comboBoxSelectSpoke.itemData(row):
                self.ui.tableViewSpokesDatabase.selectRow(row)
                break

    def update_spoke_details(self) -> None:
        """
        Update the spoke details fields when a spoke is
        selected in comboBoxSelectSpoke.
        """
        spoke_id = self.ui.comboBoxSelectSpoke.currentData()
        if spoke_id is None:
            self.clear_spoke_details()
            return

        try:
            connection: sqlite3.Connection = sqlite3.connect(self.db_path)
            cursor: sqlite3.Cursor = connection.cursor()

            query = (
                "SELECT "
                "s.name, t.type, s.gauge, s.weight, "
                "s.dimensions, s.comment, s.type_id "
                "FROM spokes s "
                "JOIN types t ON s.type_id = t.id "
                "WHERE s.id = ?"
            )
            cursor.execute(query, (spoke_id,))
            spoke = cursor.fetchone()

            if spoke:
                self.ui.lineEditNewSpokeName.setText(spoke[0])
                self.ui.comboBoxSelectNewSpokeType.setCurrentText(spoke[1])
                self.ui.lineEditNewSpokeGauge.setText(str(spoke[2]))
                self.ui.lineEditNewSpokeWeight.setText(str(spoke[3]))
                self.ui.lineEditNewSpokeDimension.setText(spoke[4])
                self.ui.lineEditNewSpokeComment.setText(spoke[5])

            connection.close()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def unselect_spoke(self) -> None:
        """
        Unselect the row in tableViewSpokesDatabase
        when pushButtonEditSpoke is clicked.
        """
        self.ui.tableViewSpokesDatabase.clearSelection()
        self.clear_spoke_details()

    def clear_spoke_selection(self) -> None:
        """
        Clear the row selection in tableViewSpokesDatabase
        and clear all spoke detail fields.
        """
        self.ui.tableViewSpokesDatabase.clearSelection()
        self.ui.comboBoxSelectSpoke.setCurrentIndex(-1)
        self.clear_spoke_details()

    def clear_spoke_details(self) -> None:
        """
        Clear all spoke detail fields.
        """
        self.ui.lineEditNewSpokeName.clear()
        self.ui.comboBoxSelectNewSpokeType.setCurrentIndex(-1)
        self.ui.lineEditNewSpokeGauge.clear()
        self.ui.lineEditNewSpokeWeight.clear()
        self.ui.lineEditNewSpokeDimension.clear()
        self.ui.lineEditNewSpokeComment.clear()

    def toggle_new_manufacturer_button(self) -> None:
        """
        Enable or disable pushButtonNewManufacturerDatabase
        based on lineEditNewManufacturerDatabase.
        """
        self.ui.pushButtonNewManufacturerDatabase.setEnabled(
            bool(self.ui.lineEditNewManufacturerDatabase.text()))

    def toggle_spoke_buttons(self) -> None:
        """
        Enable or disable pushButtonCreateNewSpoke
        and pushButtonEditSpoke based on spoke detail fields.
        """
        required_fields_filled = all([
            self.ui.lineEditNewSpokeName.text(),
            self.ui.comboBoxSelectNewSpokeType.currentIndex() >= 0,
            self.ui.lineEditNewSpokeGauge.text(),
            self.ui.lineEditNewSpokeWeight.text(),
            self.ui.lineEditNewSpokeDimension.text()
        ])
        self.ui.pushButtonCreateNewSpoke.setEnabled(required_fields_filled)
        self.ui.pushButtonEditSpoke.setEnabled(
            required_fields_filled and
            self.ui.comboBoxSelectSpoke.currentIndex() >= 0)

    def create_new_manufacturer(self) -> None:
        """
        Insert a new manufacturer into the manufacturers table.
        """
        manufacturer_name = self.ui.lineEditNewManufacturerDatabase.text()
        if not manufacturer_name:
            return

        try:
            connection: sqlite3.Connection = sqlite3.connect(self.db_path)
            cursor: sqlite3.Cursor = connection.cursor()

            cursor.execute("INSERT INTO manufacturers (name) "
                           "VALUES (?)", (manufacturer_name,))
            connection.commit()
            connection.close()

            self.ui.lineEditNewManufacturerDatabase.clear()
            self.load_manufacturers()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def create_new_spoke(self) -> None:
        """
        Insert a new spoke into the spokes table for the selected manufacturer.
        """
        manufacturer_id = \
            self.ui.comboBoxSelectSpokeManufacturerDatabase.currentData()
        spoke_name = self.ui.lineEditNewSpokeName.text()
        type_id = self.ui.comboBoxSelectNewSpokeType.currentData()
        gauge = self.ui.lineEditNewSpokeGauge.text()
        weight = self.ui.lineEditNewSpokeWeight.text()
        dimension = self.ui.lineEditNewSpokeDimension.text()
        comment = self.ui.lineEditNewSpokeComment.text()

        try:
            connection: sqlite3.Connection = sqlite3.connect(self.db_path)
            cursor: sqlite3.Cursor = connection.cursor()

            cursor.execute(
                "INSERT INTO spokes "
                "(manufacturer_id, name, type_id, "
                "gauge, weight, dimensions, comment) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (manufacturer_id, spoke_name, type_id,
                 gauge, weight, dimension, comment)
            )
            connection.commit()
            connection.close()

            self.load_spokes_for_selected_manufacturer()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def edit_spoke(self) -> None:
        """
        Update the selected spoke with new values from the detail fields.
        """
        spoke_id = self.ui.comboBoxSelectSpoke.currentData()
        if not spoke_id:
            return

        spoke_name = self.ui.lineEditNewSpokeName.text()
        type_id = self.ui.comboBoxSelectNewSpokeType.currentData()
        gauge = self.ui.lineEditNewSpokeGauge.text()
        weight = self.ui.lineEditNewSpokeWeight.text()
        dimension = self.ui.lineEditNewSpokeDimension.text()
        comment = self.ui.lineEditNewSpokeComment.text()

        try:
            connection: sqlite3.Connection = sqlite3.connect(self.db_path)
            cursor: sqlite3.Cursor = connection.cursor()

            cursor.execute(
                "UPDATE spokes SET "
                "name = ?, type_id = ?, gauge = ?, "
                "weight = ?, dimensions = ?, comment = ? "
                "WHERE id = ?",
                (spoke_name, type_id, gauge, weight,
                 dimension, comment, spoke_id)
            )
            connection.commit()
            connection.close()

            self.load_spokes_for_selected_manufacturer()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def delete_spoke(self) -> None:
        """
        Delete the currently selected spoke from the spokes table.
        """
        spoke_id = self.ui.comboBoxSelectSpoke.currentData()
        if not spoke_id:
            return

        try:
            connection: sqlite3.Connection = sqlite3.connect(self.db_path)
            cursor: sqlite3.Cursor = connection.cursor()

            cursor.execute("DELETE FROM spokes WHERE id = ?", (spoke_id,))
            connection.commit()
            connection.close()

            self.load_spokes_for_selected_manufacturer()
        except sqlite3.Error as e:
            print(f"Database error: {e}")


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
