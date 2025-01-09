import inspect
import logging
import os
import sys
import sqlite3
from PySide6.QtCore import Qt
from PySide6.QtCore import QAbstractTableModel
from PySide6.QtCore import QModelIndex
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QHeaderView
from PySide6.QtWidgets import QAbstractItemView
from mothership_ui import Ui_mainWindow


def get_line_info() -> str:
    return f"{inspect.stack()[1][2]}:{inspect.stack()[1][3]}"


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
        self.current_path: str = os.path.dirname(os.path.realpath(sys.argv[0]))
        self.db_path: str = f"{self.current_path}/spokeduino.sqlite"
        if not os.path.exists(self.db_path):
            logging.error(f"Database file not found at: {self.db_path}")
            sys.exit("Error: Database file not found.")

        self.current_spokes: list[list[str]] = []  # Store current spokes data
        self.load_manufacturers()

    def setup_signals_and_slots(self) -> None:
        """
        Connect UI elements to their respective event handlers for both tabs.
        """
        # Create and Edit Spoke Buttons
        self.ui.pushButtonCreateSpoke.clicked.connect(self.create_new_spoke)
        self.ui.pushButtonCreateSpoke2.clicked.connect(
            self.create_new_spoke
        )
        self.ui.pushButtonEditSpoke.clicked.connect(self.edit_spoke)
        self.ui.pushButtonDeleteSpoke.clicked.connect(self.delete_spoke)

        # Manufacturer-related buttons
        self.ui.lineEditNewManufacturer.textChanged.connect(
            self.toggle_new_manufacturer_button
        )
        self.ui.lineEditNewManufacturer2.textChanged.connect(
            self.toggle_new_manufacturer_button
        )
        self.ui.pushButtonNewManufacturer.clicked.connect(
            self.create_new_manufacturer
        )
        self.ui.pushButtonNewManufacturer2.clicked.connect(
            self.create_new_manufacturer
        )

        # Synchronize fields and buttons
        self.ui.lineEditName.textChanged.connect(
            self.toggle_spoke_buttons)
        self.ui.lineEditName2.textChanged.connect(
            self.toggle_spoke_buttons)

        self.ui.comboBoxType.currentIndexChanged.connect(
            self.toggle_spoke_buttons)
        self.ui.comboBoxType2.currentIndexChanged.connect(
            self.toggle_spoke_buttons)

        self.ui.lineEditGauge.textChanged.connect(
            self.toggle_spoke_buttons)
        self.ui.lineEditGauge2.textChanged.connect(
            self.toggle_spoke_buttons)

        self.ui.lineEditWeight.textChanged.connect(
            self.toggle_spoke_buttons)
        self.ui.lineEditWeight2.textChanged.connect(
            self.toggle_spoke_buttons)

        self.ui.lineEditDimension.textChanged.connect(
            self.toggle_spoke_buttons)
        self.ui.lineEditDimension2.textChanged.connect(
            self.toggle_spoke_buttons)

        # Synchronize combobox and table for spokes
        self.ui.comboBoxSpoke.currentIndexChanged.connect(
            self.update_spoke_details)
        self.ui.comboBoxSpoke2.currentIndexChanged.connect(
            self.update_spoke_details)

        self.ui.comboBoxSpoke.currentIndexChanged.connect(
            self.select_spoke_row)
        self.ui.comboBoxSpoke2.currentIndexChanged.connect(
            self.select_spoke_row)

        self.ui.comboBoxSpoke.currentIndexChanged.connect(
            self.sync_spoke_selection)
        self.ui.comboBoxSpoke2.currentIndexChanged.connect(
            self.sync_spoke_selection
        )
        self.ui.tableViewSpokesDatabase.clicked.connect(
            self.select_spoke_from_table)

        # Manufacturer-related buttons and combo boxes
        self.ui.comboBoxManufacturer.\
            currentIndexChanged.connect(
                self.load_spokes_for_selected_manufacturer)
        self.ui.comboBoxManufacturer2.\
            currentIndexChanged.connect(
                self.load_spokes_for_selected_manufacturer)
        self.ui.comboBoxManufacturer2.\
            currentIndexChanged.connect(
                self.sync_manufacturer_selection)
        self.ui.comboBoxManufacturer.\
            currentIndexChanged.connect(
                self.sync_manufacturer_selection)

        # Tensiometer-related signals
        self.ui.comboBoxTensiometer.currentIndexChanged.connect(
            self.load_measurements_for_selected_spoke
        )
        self.ui.lineEditNewTensiometer.textChanged.connect(
            self.toggle_new_tensiometer_button
        )
        self.ui.pushButtonNewTensiometer.clicked.connect(
            self.create_new_tensiometer)

        # Measurement-related signals
        self.ui.pushButtonDeleteMeasurement.clicked.connect(
            self.delete_measurement)
        self.ui.pushButtonAddMeasurement.clicked.connect(
            lambda: self.ui.tabWidget.setCurrentIndex(
                self.ui.tabWidget.indexOf(self.ui.measurementTab)
            )
        )
        self.ui.tableViewMeasurements.clicked.connect(
            self.select_measurement_row
        )

        # Table sorting
        header = self.ui.tableViewSpokesDatabase.horizontalHeader()
        header.sectionClicked.connect(self.sort_by_column)

    def update_fields(self, spoke=None) -> None:
        """
        Update the fields and comboboxes on both tabs
        with the provided spoke data.
        If no spoke is provided, clear the fields.
        """
        if spoke:
            self.ui.lineEditName.setText(spoke[0])
            self.ui.lineEditName2.setText(spoke[0])
            self.ui.comboBoxType.setCurrentText(spoke[1])
            self.ui.comboBoxType2.setCurrentText(spoke[1])
            self.ui.lineEditGauge.setText(str(spoke[2]))
            self.ui.lineEditGauge2.setText(str(spoke[2]))
            self.ui.lineEditWeight.setText(str(spoke[3]))
            self.ui.lineEditWeight2.setText(str(spoke[3]))
            self.ui.lineEditDimension.setText(spoke[4])
            self.ui.lineEditDimension2.setText(spoke[4])
            self.ui.lineEditSpokeComment.setText(spoke[5])
            self.ui.lineEditSpokeComment2.setText(spoke[5])
        else:
            self.clear_spoke_details()

    def clear_spoke_details(self) -> None:
        """
        Clear all spoke detail fields on both tabs.
        """
        for widget in [
            self.ui.lineEditName,
            self.ui.lineEditName2,
            self.ui.lineEditGauge,
            self.ui.lineEditGauge2,
            self.ui.lineEditWeight,
            self.ui.lineEditWeight2,
            self.ui.lineEditDimension,
            self.ui.lineEditDimension2,
            self.ui.lineEditSpokeComment,
            self.ui.lineEditSpokeComment2,
        ]:
            widget.clear()

        self.ui.comboBoxType.setCurrentIndex(-1)
        self.ui.comboBoxType2.setCurrentIndex(-1)

    def synchronize_comboboxes(self, combo_box, value) -> None:
        """
        Synchronize the value of combo boxes between the two tabs.
        """
        if combo_box == self.ui.comboBoxSpoke:
            self.ui.comboBoxSpoke2.setCurrentText(value)
        elif combo_box == self.ui.comboBoxSpoke2:
            self.ui.comboBoxSpoke.setCurrentText(value)

    def sync_spoke_selection(self) -> None:
        """
        Synchronize the spoke selection between the Database Tab and
        Measurement Tab while preventing circular calls.
        """
        if self.sender() == self.ui.comboBoxSpoke:
            # Sync comboBoxSpoke2 with comboBoxSpoke
            self.ui.comboBoxSpoke2.blockSignals(True)
            self.ui.comboBoxSpoke2.setCurrentIndex(
                self.ui.comboBoxSpoke.currentIndex()
            )
            self.ui.comboBoxSpoke2.blockSignals(False)
        elif self.sender() == self.ui.comboBoxSpoke2:
            # Sync comboBoxSpoke with comboBoxSpoke2
            self.ui.comboBoxSpoke.blockSignals(True)
            self.ui.comboBoxSpoke.setCurrentIndex(
                self.ui.comboBoxSpoke2.currentIndex()
            )
            self.ui.comboBoxSpoke.blockSignals(False)

        # Update the details for the currently selected spoke
        self.update_spoke_details()

    def sync_manufacturer_selection(self) -> None:
        """
        Synchronize the manufacturer selection between the
        Database Tab and Measurement Tab. Trigger loading
        of spokes for the selected manufacturer.
        """
        combo1 = self.ui.comboBoxManufacturer
        combo2 = self.ui.comboBoxManufacturer2
        selected_manufacturer_id = (
            combo1.currentData()
            if self.sender() == combo1
            else self.ui.combo2.currentData()
        )

        if combo1.currentData() != selected_manufacturer_id:
            combo1.blockSignals(True)
            combo1.setCurrentIndex(
                combo1.findData(selected_manufacturer_id)
            )
            combo1.blockSignals(False)

        if combo2.currentData() != selected_manufacturer_id:
            combo2.blockSignals(True)
            combo2.setCurrentIndex(
                combo2.findData(selected_manufacturer_id)
            )
            combo2.blockSignals(False)

        self.load_spokes_for_selected_manufacturer()

    def load_tensiometers(self) -> None:
        """
        Load all tensiometers from the database
        and populate comboBoxTensiometer.
        """
        query: str = """
                    SELECT
                        id, name
                    FROM
                        tensioners"""
        try:
            connection: sqlite3.Connection = sqlite3.connect(self.db_path)
            cursor: sqlite3.Cursor = connection.cursor()

            cursor.execute("SELECT id, name FROM tensioners")
            tensioners = cursor.fetchall()

            self.ui.comboBoxTensiometer.clear()
            for tensioner in tensioners:
                self.ui.comboBoxTensiometer.addItem(tensioner[1], tensioner[0])

            connection.close()
        except sqlite3.Error as e:
            logging.error(f"{get_line_info()}: SQL error: {e}\nQuery: {query}")

    def load_manufacturers(self) -> None:
        """
        Load all manufacturer names from the database and populate the
        the dropdowns. Automatically loads spokes for the first manufacturer.
        """
        query: str = """
                    SELECT
                        id, name
                    FROM
                        manufacturers"""
        try:
            connection: sqlite3.Connection = sqlite3.connect(self.db_path)
            cursor: sqlite3.Cursor = connection.cursor()

            # Load manufacturers
            cursor.execute(query)
            manufacturers = cursor.fetchall()

            self.ui.comboBoxManufacturer.clear()
            self.ui.comboBoxManufacturer2.clear()

            for manufacturer in manufacturers:
                self.ui.comboBoxManufacturer.addItem(
                    manufacturer[1], manufacturer[0])
                self.ui.comboBoxManufacturer2.addItem(
                    manufacturer[1], manufacturer[0]
                )

            # Load spoke types
            query = """
                        SELECT
                            id, type
                        FROM
                            types"""
            cursor.execute(query)
            spoke_types = cursor.fetchall()

            self.ui.comboBoxType.clear()
            self.ui.comboBoxType2.clear()
            for spoke_type in spoke_types:
                self.ui.comboBoxType.addItem(
                    spoke_type[1], spoke_type[0])
                self.ui.comboBoxType2.addItem(
                    spoke_type[1], spoke_type[0])

            connection.close()

            # Automatically load spokes for the first manufacturer
            if manufacturers:
                self.ui.comboBoxManufacturer.\
                    setCurrentIndex(0)
                self.ui.comboBoxManufacturer2.\
                    setCurrentIndex(0)
                self.load_spokes_for_selected_manufacturer()
        except sqlite3.Error as e:
            logging.error(f"{get_line_info()}: SQL error: {e}\nQuery: {query}")
        except Exception as e:
            logging.error(f"{get_line_info()}: Unexpected error: {e}")

    def load_spokes_for_selected_manufacturer(self) -> None:
        """
        Load all spokes for the currently selected manufacturer and populate
        the tableViewSpokesDatabase and comboBoxSpoke.
        """
        manufacturer_id = \
            self.ui.comboBoxManufacturer.currentData()

        query: str = """
                    SELECT
                        s.name, t.type, s.gauge, s.weight,
                        s.dimensions, s.comment, s.id
                    FROM
                        spokes s
                    JOIN
                        types t
                    ON
                        s.type_id = t.id
                    WHERE
                        s.manufacturer_id = ?"""

        try:
            connection: sqlite3.Connection = \
                sqlite3.connect(self.db_path)
            cursor: sqlite3.Cursor = connection.cursor()
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

            # Populate comboBoxSpoke
            self.ui.comboBoxSpoke.clear()
            self.ui.comboBoxSpoke2.clear()
            for spoke in spokes:
                # Name and ID
                self.ui.comboBoxSpoke.addItem(
                    spoke[0], spoke[-1])
                self.ui.comboBoxSpoke2.addItem(
                    spoke[0], spoke[-1])

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
            logging.error(f"{get_line_info()}: SQL error: {e}\nQuery: {query}")
        except Exception as e:
            logging.error(f"{get_line_info()}: Unexpected error: {e}")

    def load_measurements_for_selected_spoke(self) -> None:
        """
        Load all measurements for the selected spoke and tensiometer
        and populate tableViewMeasurements.
        """
        spoke_id = self.ui.comboBoxSpoke.currentData()
        tensiometer_id = self.ui.comboBoxTensiometer.currentData()

        if not spoke_id or not tensiometer_id:
            self.ui.tableViewMeasurements.setModel(None)
            return

        query = """
                SELECT
                    tension_300N, tension_400N, tension_500N,
                    tension_600N, tension_700N, tension_800N,
                    tension_900N, tension_1000N, tension_1100N,
                    tension_1200N, tension_1300N, tension_1400N,
                    tension_1500N, id
                FROM
                    measurements
                WHERE
                    spoke_id = ?
                AND
                    tensioner_id = ?"""

        try:
            connection: sqlite3.Connection = sqlite3.connect(self.db_path)
            cursor: sqlite3.Cursor = connection.cursor()
            cursor.execute(query, (spoke_id, tensiometer_id))
            measurements = cursor.fetchall()

            headers = [
                "300N", "400N", "500N", "600N", "700N", "800N", "900N",
                "1000N", "1100N", "1200N", "1300N", "1400N", "1500N"
            ]
            model = SpokeduinoTableModel(
                [list(measurement[:-1])
                    for measurement in measurements], headers
            )
            self.ui.tableViewMeasurements.setModel(model)

            # Configure table behavior
            self.ui.tableViewMeasurements.setSelectionBehavior(
                QAbstractItemView.SelectionBehavior.SelectRows
            )
            self.ui.tableViewMeasurements.setSelectionMode(
                QAbstractItemView.SelectionMode.SingleSelection
            )

            # Set column headers
            self.ui.tableViewMeasurements.horizontalHeader().\
                setSectionResizeMode(
                QHeaderView.ResizeMode.ResizeToContents
            )
            self.ui.tableViewMeasurements.horizontalHeader().\
                setStretchLastSection(True)
            connection.close()
        except sqlite3.Error as e:
            logging.error(f"{get_line_info()}: SQL error: {e}\nQuery: {query}")

    def delete_measurement(self) -> None:
        """
        Delete the currently selected measurement from the measurements table.
        """
        selected_index = self.ui.tableViewMeasurements.currentIndex()
        if not selected_index.isValid():
            return

        measurement_id = self.ui.tableViewMeasurements.model().index(
            selected_index.row(), len(selected_index.model()._headers)
        ).data()

        query: str = """
                    DELETE FROM
                        measurements
                    WHERE
                        id = ?"""
        try:
            connection: sqlite3.Connection = sqlite3.connect(self.db_path)
            cursor: sqlite3.Cursor = connection.cursor()

            cursor.execute(query, (measurement_id,))
            connection.commit()
            connection.close()

            self.ui.tableViewMeasurements.clearSelection()
            self.load_measurements_for_selected_spoke()
        except sqlite3.Error as e:
            logging.error(f"{get_line_info()}: SQL error: {e}\nQuery: {query}")

    def sort_by_column(self, column: int) -> None:
        """
        Sort the tableViewSpokesDatabase by the specified column.
        """
        self.current_spokes.sort(key=lambda x: x[column])
        self.ui.tableViewSpokesDatabase.model().layoutChanged.emit()

    def select_spoke_from_table(self, index: QModelIndex) -> None:
        """
        Select the corresponding spoke in comboBoxSpoke
        when a row is clicked.
        """
        row = index.row()
        spoke_name = self.current_spokes[row][0]
        self.ui.comboBoxSpoke.setCurrentText(spoke_name)

    def select_spoke_row(self) -> None:
        """
        Select the corresponding row in tableViewSpokesDatabase
        and synchronize the comboboxes.
        """
        spoke_id = self.ui.comboBoxSpoke.currentData()
        if spoke_id is None:
            self.ui.tableViewSpokesDatabase.clearSelection()
            return

        for row, spoke in enumerate(self.current_spokes):
            if spoke_id == self.ui.comboBoxSpoke.itemData(row):
                self.ui.tableViewSpokesDatabase.selectRow(row)
                self.synchronize_comboboxes(
                    self.ui.comboBoxSpoke,
                    self.ui.comboBoxSpoke.currentText())
                break

    def update_spoke_details(self) -> None:
        """
        Update the spoke details fields when a spoke is
        selected in comboBoxSpoke.
        """
        spoke_id = self.ui.comboBoxSpoke.currentData()
        if spoke_id is None:
            self.clear_spoke_details()
            return

        query = """
                SELECT
                    s.name, t.type, s.gauge, s.weight,
                    s.dimensions, s.comment, s.type_id
                FROM
                    spokes s
                JOIN
                    types t
                ON
                    s.type_id = t.id
                WHERE s.id = ?"""

        try:
            connection: sqlite3.Connection = sqlite3.connect(self.db_path)
            cursor: sqlite3.Cursor = connection.cursor()
            cursor.execute(query, (spoke_id,))
            spoke = cursor.fetchone()

            if spoke:
                self.update_fields(spoke)

            connection.close()
        except sqlite3.Error as e:
            logging.error(f"{get_line_info()}: SQL error: {e}\nQuery: {query}")
        except Exception as e:
            logging.error(f"{get_line_info()}: Unexpected error: {e}")

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
        self.ui.comboBoxSpoke.setCurrentIndex(-1)
        self.clear_spoke_details()

    def select_measurement_row(self, index: QModelIndex) -> None:
        """
        Handle row selection in tableViewMeasurements
        This function ensures that the correct measurement row is highlighted.
        """
        if not index.isValid():
            return

        row = index.row()
        self.ui.tableViewMeasurements.selectRow(row)

    def toggle_new_tensiometer_button(self) -> None:
        """
        Enable or disable pushButtonNewTensiometer based on the text in
        lineEditNewTensiometer.
        """
        is_filled = bool(self.ui.lineEditNewTensiometer.text())
        self.ui.pushButtonNewTensiometer.setEnabled(is_filled)

    def toggle_new_manufacturer_button(self) -> None:
        """
        Enable or disable pushButtonNewManufacturer
        based on lineEditNewManufacturer.
        """
        is_measurement_filled = bool(
            self.ui.lineEditNewManufacturer.text())
        is_database_filled = bool(
            self.ui.lineEditNewManufacturer2.text())

        self.ui.pushButtonNewManufacturer.setEnabled(
            is_database_filled)
        self.ui.pushButtonNewManufacturer2.setEnabled(
            is_measurement_filled
        )

    def toggle_spoke_buttons(self) -> None:
        """
        Enable or disable pushButtonCreateSpoke
        and pushButtonEditSpoke based on spoke detail fields.
        """
        required_fields_filled = all([
            self.ui.lineEditName.text(),
            self.ui.comboBoxType.currentIndex() >= 0,
            self.ui.lineEditGauge.text(),
            self.ui.lineEditWeight.text(),
            self.ui.lineEditDimension.text()
        ])
        self.ui.pushButtonCreateSpoke.setEnabled(required_fields_filled)
        self.ui.pushButtonEditSpoke.setEnabled(
            required_fields_filled and
            self.ui.comboBoxSpoke.currentIndex() >= 0)

    def create_new_tensiometer(self) -> None:
        """
        Insert a new tensiometer into the tensiometers table.
        """
        tensiometer_name = self.ui.lineEditNewTensiometer.text()
        if not tensiometer_name:
            return

        query: str = """
                    INSERT INTO
                        tensioners (name)
                    VALUES
                        (?)"""
        try:
            connection: sqlite3.Connection = sqlite3.connect(self.db_path)
            cursor: sqlite3.Cursor = connection.cursor()

            cursor.execute(query, (tensiometer_name,))
            connection.commit()
            connection.close()

            self.ui.lineEditNewTensiometer.clear()
            self.load_tensiometers()
        except sqlite3.Error as e:
            logging.error(f"{get_line_info()}: SQL error: {e}\nQuery: {query}")

    def create_new_manufacturer(self) -> None:
        """
        Insert a new manufacturer into the manufacturers table and select it.
        """
        manufacturer_name = (
            self.ui.lineEditNewManufacturer.text()
            if self.sender() == self.ui.pushButtonNewManufacturer
            else self.ui.lineEditNewManufacturer2.text()
        )
        if not manufacturer_name:
            return

        query: str = """
                    INSERT INTO
                        manufacturers (name)
                    VALUES
                        (?)"""

        try:
            connection: sqlite3.Connection = sqlite3.connect(self.db_path)
            cursor: sqlite3.Cursor = connection.cursor()

            cursor.execute(query, (manufacturer_name,))
            new_manufacturer_id = cursor.lastrowid
            connection.commit()
            connection.close()

            self.ui.lineEditNewManufacturer.clear()
            self.ui.lineEditNewManufacturer2.clear()
            self.load_manufacturers()
            self.ui.comboBoxManufacturer.setCurrentIndex(
                self.ui.comboBoxManufacturer.findData(
                    new_manufacturer_id)
            )
        except sqlite3.Error as e:
            logging.error(f"{get_line_info()}: SQL error: {e}\nQuery: {query}")

    def create_new_spoke(self) -> None:
        """
        Insert a new spoke into the spokes table for the selected manufacturer.
        """
        if self.sender() == self.ui.pushButtonCreateSpoke:
            manufacturer_id = self.ui.comboBoxManufacturer.currentData()
            spoke_name = self.ui.lineEditName.text()
            type_id = self.ui.comboBoxType.currentData()
            gauge = self.ui.lineEditGauge.text()
            weight = self.ui.lineEditWeight.text()
            dimension = self.ui.lineEditDimension.text()
            comment = self.ui.lineEditSpokeComment.text()
        else:
            manufacturer_id = self.ui.comboBoxManufacturer2.currentData()
            spoke_name = self.ui.lineEditName2.text()
            type_id = self.ui.comboBoxType2.currentData()
            gauge = self.ui.lineEditGauge2.text()
            weight = self.ui.lineEditWeight2.text()
            dimension = self.ui.lineEditDimension2.text()
            comment = self.ui.lineEditSpokeComment2.text()

        query: str = """
                    INSERT INTO
                        spokes(manufacturer_id, name, type_id,
                        gauge, weight, dimensions, comment)
                    VALUES
                        (?, ?, ?, ?, ?, ?, ?)"""

        try:
            connection: sqlite3.Connection = sqlite3.connect(self.db_path)
            cursor: sqlite3.Cursor = connection.cursor()

            cursor.execute(query, (manufacturer_id, spoke_name, type_id,
                                   gauge, weight, dimension, comment))
            new_spoke_id = cursor.lastrowid
            connection.commit()
            connection.close()

            self.load_spokes_for_selected_manufacturer()
            self.ui.comboBoxSpoke.setCurrentIndex(
                self.ui.comboBoxSpoke.findData(new_spoke_id)
            )
            self.ui.comboBoxSpoke2.setCurrentIndex(
                self.ui.comboBoxSpoke2.findData(new_spoke_id)
            )
        except sqlite3.Error as e:
            logging.error(f"{get_line_info()}: SQL error: {e}\nQuery: {query}")

    def edit_spoke(self) -> None:
        """
        Update the selected spoke with new values from the detail fields.
        """
        spoke_id = self.ui.comboBoxSpoke.currentData()
        if not spoke_id:
            return

        spoke_name = self.ui.lineEditName.text()
        type_id = self.ui.comboBoxType.currentData()
        gauge = self.ui.lineEditGauge.text()
        weight = self.ui.lineEditWeight.text()
        dimension = self.ui.lineEditDimension.text()
        comment = self.ui.lineEditSpokeComment.text()

        query: str = """
                    UPDATE
                        spokes
                    SET
                        name = ?, type_id = ?, gauge = ?,
                        weight = ?, dimensions = ?, comment = ?
                    WHERE id = ?"""

        try:
            connection: sqlite3.Connection = sqlite3.connect(self.db_path)
            cursor: sqlite3.Cursor = connection.cursor()

            cursor.execute(query, (spoke_name, type_id, gauge,
                                   weight, dimension, comment, spoke_id))
            connection.commit()
            connection.close()

            self.load_spokes_for_selected_manufacturer()
        except sqlite3.Error as e:
            logging.error(f"{get_line_info()}: SQL error: {e}\nQuery: {query}")

    def delete_spoke(self) -> None:
        """
        Delete the currently selected spoke from the spokes table.
        """
        spoke_id = self.ui.comboBoxSpoke.currentData()
        if not spoke_id:
            return

        query: str = """DELETE FROM
                            spokes
                        WHERE
                            id = ?"""

        try:
            connection: sqlite3.Connection = sqlite3.connect(self.db_path)
            cursor: sqlite3.Cursor = connection.cursor()

            cursor.execute(query, (spoke_id,))
            connection.commit()
            connection.close()

            self.load_spokes_for_selected_manufacturer()
        except sqlite3.Error as e:
            logging.error(f"{get_line_info()}: SQL error: {e}\nQuery: {query}")


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
