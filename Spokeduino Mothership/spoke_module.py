import logging
from typing import Any, TYPE_CHECKING
from PySide6.QtCore import Qt
from PySide6.QtCore import QTranslator
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QHeaderView
from PySide6.QtWidgets import QTableWidget
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtWidgets import QComboBox
from database_module import DatabaseModule
from measurement_module import MeasurementModule
from sql_queries import SQLQueries
from helpers import Messagebox, Generics
from ui import Ui_mainWindow

if TYPE_CHECKING:
    from mothership import Spokeduino


class SpokeModule:

    def __init__(self,
                 ui: Ui_mainWindow,
                 main_window: "Spokeduino",
                 measurement_module: MeasurementModule,
                 messagebox: Messagebox,
                 db: DatabaseModule,
                 current_path: str) -> None:
        self.ui: Ui_mainWindow = ui
        self.main_window: Spokeduino = main_window
        self.current_path: str = current_path
        self.translator = QTranslator()
        self.current_language = "en"
        self.db: DatabaseModule = db
        self.measurement_module: MeasurementModule = measurement_module
        self.messagebox: Messagebox = messagebox
        self.__spoke_headers: list[str] = [
                "Name",
                "Type",
                "Gauge",
                "Weight",
                "Dimensions",
                "Comment"]

    def update_fields(self, spoke: list[str]) -> None:
        """
        Update the fields and comboboxes with the provided spoke data.
        If no spoke is provided, clear the fields.
        """
        if spoke:
            self.ui.lineEditName.setText(str(spoke[0]))
            self.ui.comboBoxType.setCurrentText(str(spoke[1]))
            self.ui.lineEditGauge.setText(str(spoke[2]))
            self.ui.lineEditWeight.setText(str(spoke[3]))
            self.ui.lineEditDimension.setText(str(spoke[4]))
            self.ui.lineEditSpokeComment.setText(str(spoke[5]))
            self.main_window.status_label_spoke.setText(
                f"{self.ui.comboBoxManufacturer.currentText()} "
                f"{self.ui.lineEditName.text()} {self.ui.lineEditDimension.text()}")
        else:
            self.clear_spoke_details()

    def clear_spoke_details(self) -> None:
        """
        Clear all spoke detail fields on both tabs.
        """
        for widget in [
            self.ui.lineEditName,
            self.ui.lineEditGauge,
            self.ui.lineEditWeight,
            self.ui.lineEditDimension,
            self.ui.lineEditSpokeComment,
        ]:
            widget.clear()

        self.ui.comboBoxType.setCurrentIndex(-1)
        self.main_window.status_label_spoke.setText("")

    def load_spoke_details(self) -> None:
        """
        Update the spoke details fields when a spoke is selected.
        """
        view: QTableWidget = self.ui.tableWidgetSpokesDatabase
        spoke_id: int = Generics.get_selected_row_id(view)
        if spoke_id < 0:
            return

        spokes: list[Any] = self.db.execute_select(
            query=SQLQueries.GET_SPOKES_BY_ID,
            params=(spoke_id,))

        if not spokes:
            return

        self.update_fields(spokes[0][1:])
        self.measurement_module.load_measurements(spoke_id, None, False)

    def load_manufacturers(self) -> None:
        """
        Load all manufacturer names from the database and populate the
        the dropdowns. Automatically loads spokes for the first manufacturer.
        """
        # Load manufacturers
        manufacturers: list[Any] = self.db.execute_select(
            query=SQLQueries.GET_MANUFACTURERS, params=None)
        if not manufacturers:
            return

        self.ui.comboBoxManufacturer.clear()
        for manufacturer in manufacturers:
            self.ui.comboBoxManufacturer.addItem(
                manufacturer[1], manufacturer[0])

        # Load types
        spoke_types: list[Any] = self.db.execute_select(
            query=SQLQueries.GET_TYPES, params=None)
        if not spoke_types:
            return

        self.ui.comboBoxType.clear()
        for spoke_type in spoke_types:
            self.ui.comboBoxType.addItem(
                spoke_type[1], spoke_type[0])

        # Automatically load spokes for the first manufacturer
        if manufacturers:
            self.ui.comboBoxManufacturer.setCurrentIndex(0)
            self.load_spokes()

    def load_spokes(self) -> None:
        """
        Load all spokes for the currently selected manufacturer
        and populate the tableWidgetSpokesDatabase
        """
        manufacturer_id: int | None = \
            self.ui.comboBoxManufacturer.currentData()

        if manufacturer_id is None:
            return
        manufacturer_id = int(manufacturer_id)

        # Fetch spokes from the database
        spokes: list[Any] = self.db.execute_select(
            query=SQLQueries.GET_SPOKES_BY_MANUFACTURER,
            params=(manufacturer_id,)
        )
        view: QTableWidget = self.ui.tableWidgetSpokesDatabase
        view.clearContents()  # Clear existing data
        view.setColumnCount(6)  # Set column count for your table structure

        if not spokes:
            view.setRowCount(0)  # Set row count
            self.toggle_spoke_related_buttons()
            return

        # Store current spokes with their IDs
        self.current_spokes: list[tuple[Any, list[Any]]] = [
            (spoke[0], list(spoke[1:]))
            for spoke in spokes
        ]
        view.setRowCount(len(spokes))  # Set row count

        # Populate the table widget
        for row_idx, (spoke_id, spoke_data) in enumerate(self.current_spokes):
            for col_idx, cell_data in enumerate(spoke_data):
                item = QTableWidgetItem(str(cell_data))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Read-only
                if col_idx == 0:  # Store the spoke ID in the first column
                    item.setData(Qt.ItemDataRole.UserRole, spoke_id)
                view.setItem(row_idx, col_idx, item)

        # Adjust column widths (QHeaderView methods)
        header: QHeaderView = view.horizontalHeader()
        view.setHorizontalHeaderLabels(self.__spoke_headers)
        rm = header.ResizeMode
        header.setSectionResizeMode(0, rm.Stretch)  # Name
        header.setSectionResizeMode(1, rm.Stretch)  # Type
        header.setSectionResizeMode(2, rm.ResizeToContents)  # Gauge
        header.setSectionResizeMode(3, rm.ResizeToContents)  # Weight
        header.setSectionResizeMode(4, rm.Stretch)  # Dimensions
        header.setSectionResizeMode(5, rm.Stretch)  # Comment
        view.verticalHeader().setVisible(False)

        # Configure table behavior
        view.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        view.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.populate_filter_type()
        self.filter_spoke_table()
        self.load_spoke_details()
        self.toggle_spoke_related_buttons()
        # Delay to ensure Qt's focus/selection state is updated
        QTimer.singleShot(50,
            self.align_filters_with_table)
        view.setFocus()

    def populate_filter_type(self) -> None:
        """
        Populate comboBoxFilterType with unique spoke types applicable
        to the current dataset in database order.
        """
        # Extract applicable types from current spokes
        type_ids_in_use: set[Any] = {
            spoke[1][1]
            for spoke in self.current_spokes}

        # Fetch all types from the database
        types: list[Any] = self.db.execute_select(SQLQueries.GET_TYPES, None)
        if not types:
            return
        combo: QComboBox = self.ui.comboBoxFilterType
        # Populate comboBoxFilterType with applicable types
        combo.clear()
        # Empty means no filter is set
        combo.addItem("")

        for type_id, type_name in types:
            if type_name in type_ids_in_use:
                combo.addItem(type_name, type_id)
        self.ui.lineEditFilterName.clear()
        self.ui.lineEditFilterGauge.clear()
        combo.setCurrentIndex(0)

    def filter_spoke_table(self) -> None:
        """
        Filter tableWidgetSpokesDatabase based on filter inputs.
        """
        name_filter: str = self.ui.lineEditFilterName.text().lower()
        type_filter: str = self.ui.comboBoxFilterType.currentText().lower()
        gauge_filter: str = self.ui.lineEditFilterGauge.text().lower()

        filtered_spokes: list[tuple[int, list[str]]] = [
            spoke for spoke in self.current_spokes
            if (name_filter in spoke[1][0].lower()) and  # Match Name
            (type_filter == spoke[1][1].lower()
             if type_filter else True) and  # Match Type
            (gauge_filter in str(spoke[1][2]).lower()
             if gauge_filter else True)  # Match Gauge
        ]

        view: QTableWidget = self.ui.tableWidgetSpokesDatabase
        view.clearContents()
        view.setRowCount(len(filtered_spokes))

        for row_idx, (spoke_id, spoke_data) in enumerate(filtered_spokes):
            for col_idx, cell_data in enumerate(spoke_data):
                item = QTableWidgetItem(str(cell_data))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Make read-only
                if col_idx == 0:  # Store the spoke ID in the first column
                    item.setData(Qt.ItemDataRole.UserRole, spoke_id)
                view.setItem(row_idx, col_idx, item)

        # Automatically select the first row if data is present
        if filtered_spokes:
            view.selectRow(0)
        else:
            view.clearSelection()

    def align_filters_with_table(self) -> None:
        """
        Align filter fields with the columns of tableWidgetSpokesDatabase.
        """
        view: QTableWidget = self.ui.tableWidgetSpokesDatabase
        if not view.isVisible():
            return

        header: QHeaderView = view.horizontalHeader()
        if header.count() == 0:
            return  # No headers to align with

        # Get the global position of the table's top-left corner
        table_offset_x: int = view.geometry().x() + \
            header.sectionPosition(0)

        # Align each filter to its corresponding column
        filter_fields = [
            self.ui.lineEditFilterName,
            self.ui.comboBoxFilterType,
            self.ui.lineEditFilterGauge,
        ]

        for col_idx, widget in enumerate(filter_fields):
            widget.setGeometry(
                table_offset_x + header.sectionPosition(col_idx),
                widget.y(),
                header.sectionSize(col_idx),
                widget.height()
            )

    def sort_by_column(self, column: int) -> None:
        """
        Sort the tableWidgetSpokesDatabase by the specified column.
        """
        self.current_spokes.sort(key=lambda x: x[1][column])
        self.ui.tableWidgetSpokesDatabase.model().layoutChanged.emit()

    def get_spoke_data(self) -> tuple[int, int, float, str, str, str]:
        """
        DRY helper
        """
        try:
            return int(self.ui.comboBoxType.currentData()), \
                int(self.ui.lineEditGauge.text() or 0), \
                float(self.ui.lineEditWeight.text() or 0.0), \
                self.ui.lineEditName.text() or "", \
                self.ui.lineEditDimension.text() or "", \
                self.ui.lineEditSpokeComment.text() or ""
        except ValueError as e:
            logging.error(f"Invalid data provided: {e}")
            raise

    def update_spoke(self) -> None:
        """
        Update the selected spoke with new values from the detail fields.
        """
        view: QTableWidget = self.ui.tableWidgetSpokesDatabase
        spoke_id: int = Generics.get_selected_row_id(view)
        if spoke_id < 0:
            return

        type_id, gauge, weight, \
            spoke_name, dimension, comment = \
            self.get_spoke_data()

        _ = self.db.execute_query(
            query=SQLQueries.MODIFY_SPOKE,
            params=(spoke_name, type_id, gauge, weight,
                    dimension, comment, spoke_id),
        )
        self.load_spokes()

    def delete_spoke(self) -> None:
        """
        Delete the currently selected spoke from the spokes table.
        """
        view: QTableWidget = self.ui.tableWidgetSpokesDatabase
        spoke_id: int = Generics.get_selected_row_id(view)
        if spoke_id < 0:
            self.messagebox.err("spoke not selected")
            return

        _ = self.db.execute_query(
            query=SQLQueries.DELETE_SPOKE,
            params=(spoke_id,)
        )
        self.load_spokes()

    def save_as_spoke(self) -> None:
        """
        Insert a new spoke into the spokes table for the selected manufacturer.
        """
        manufacturer_id: int | None = self.ui.comboBoxManufacturer.currentData()

        if manufacturer_id is None:
            return
        manufacturer_id = int(manufacturer_id)

        type_id, gauge, weight, \
            spoke_name, dimension, comment = \
            self.get_spoke_data()

        new_spoke_id: int | None = self.db.execute_query(
            query=SQLQueries.ADD_SPOKE,
            params=(manufacturer_id, spoke_name,
                    type_id, gauge, weight, dimension, comment),
        )
        if new_spoke_id is None:
            return
        new_spoke_id = int(new_spoke_id)

        self.load_spokes()

    def create_new_manufacturer(self) -> None:
        """
        Insert a new manufacturer into the manufacturers table and select it.
        """
        manufacturer_name: str = self.ui.lineEditNewManufacturer.text()
        if not manufacturer_name:
            return

        new_manufacturer_id: int | None = self.db.execute_query(
            query=SQLQueries.ADD_MANUFACTURER,
            params=(manufacturer_name,),
        )

        self.ui.lineEditNewManufacturer.clear()
        self.load_manufacturers()

        if new_manufacturer_id is None:
            return
        new_manufacturer_id = int(new_manufacturer_id)

        self.ui.comboBoxManufacturer.setCurrentIndex(
            self.ui.comboBoxManufacturer.findData(
                new_manufacturer_id))

    def toggle_spoke_related_buttons(self) -> None:
        """
        Enable or disable spoke related buttons
        based on spoke detail fields.
        """
        self.ui.pushButtonSaveAsManufacturer.setEnabled(
            len(self.ui.lineEditNewManufacturer.text()) > 0)

        required_fields_save_spoke: bool = all([
            self.ui.lineEditName.text(),
            self.ui.comboBoxType.currentIndex() >= 0,
            self.ui.lineEditGauge.text(),
            self.ui.lineEditWeight.text(),
            self.ui.lineEditDimension.text()])
        current_spoke_row: int = \
            Generics.get_selected_row_id(self.ui.tableWidgetSpokesDatabase)
        current_measurement_row: int = \
            Generics.get_selected_row_id(self.ui.tableWidgetMeasurementList)
        self.ui.tableWidgetSpokesDatabase.currentRow()
        self.ui.pushButtonUpdateSpoke.setEnabled(required_fields_save_spoke
                                                 and current_spoke_row >= 0)
        self.ui.pushButtonDeleteSpoke.setEnabled(current_spoke_row >= 0)
        self.ui.pushButtonSaveAsSpoke.setEnabled(required_fields_save_spoke)
        self.ui.pushButtonUseLeft.setEnabled(current_measurement_row >= 0)
        self.ui.pushButtonUseRight.setEnabled(current_measurement_row >= 0)
        self.ui.pushButtonDeleteMeasurement.setEnabled(
            current_measurement_row >= 0)
        self.ui.measurementTab.setEnabled(current_spoke_row >= 0)
        self.ui.pushButtonNewMeasurement.setEnabled(current_spoke_row >= 0)
        self.ui.pushButtonEditMeasurement.setEnabled(current_measurement_row >= 0)
