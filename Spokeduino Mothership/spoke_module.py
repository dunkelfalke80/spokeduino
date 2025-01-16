import logging
from typing import Any, cast
from PySide6.QtCore import QTranslator
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QHeaderView
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QModelIndex
from PySide6.QtWidgets import QTableView
from database_module import DatabaseModule
from sql_queries import SQLQueries
from helpers import SpokeTableModel

class SpokeModule:

    def __init__(self,
                 main_window: QMainWindow,
                 ui: Any,
                 current_path: str,
                 db: DatabaseModule) -> None:
        self.ui = ui
        self.main_window: QMainWindow = main_window
        self.current_path: str = current_path
        self.translator = QTranslator()
        self.current_language = "en"
        self.db: DatabaseModule = db

        # Reducing verbosity
        self.__rm_stretch: QHeaderView.ResizeMode = \
            QHeaderView.ResizeMode.Stretch
        self.__rm_shrink: QHeaderView.ResizeMode =\
            QHeaderView.ResizeMode.ResizeToContents
        self.__select_rows: QAbstractItemView.SelectionBehavior = \
            QAbstractItemView.SelectionBehavior.SelectRows
        self.__select_single: QAbstractItemView.SelectionMode = \
            QAbstractItemView.SelectionMode.SingleSelection

    def get_selected_spoke_id(self) -> tuple[bool, int]:
        spoke_id: int | None = self.ui.comboBoxSpoke.currentData()
        if spoke_id is None:
            return False, 0
        return True, int(spoke_id)

    def update_fields(self, spoke: list[str]) -> None:
        """
        Update the fields and comboboxes on both tabs
        with the provided spoke data.
        If no spoke is provided, clear the fields.
        """
        if spoke:
            self.ui.lineEditName.setText(str(spoke[0]))
            self.ui.lineEditName2.setText(str(spoke[0]))
            self.ui.comboBoxType.setCurrentText(str(spoke[1]))
            self.ui.comboBoxType2.setCurrentText(str(spoke[1]))
            self.ui.lineEditGauge.setText(str(spoke[2]))
            self.ui.lineEditGauge2.setText(str(spoke[2]))
            self.ui.lineEditWeight.setText(str(spoke[3]))
            self.ui.lineEditWeight2.setText(str(spoke[3]))
            self.ui.lineEditDimension.setText(str(spoke[4]))
            self.ui.lineEditDimension2.setText(str(spoke[4]))
            self.ui.lineEditSpokeComment.setText(str(spoke[5]))
            self.ui.lineEditSpokeComment2.setText(str(spoke[5]))
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

    def update_spoke_details(self, sender: QComboBox) -> None:
        """
        Update the spoke details fields when a spoke is
        selected in comboBoxSpoke.
        """
        spoke_id: int | None = sender.currentData()

        if spoke_id is None:
            self.clear_spoke_details()
            return
        spoke_id = int(spoke_id)

        spokes: list[Any] = self.db.execute_select(
            query=SQLQueries.GET_SPOKES_BY_ID,
            params=(spoke_id,))
        if not spokes:
            return

        self.update_fields(spokes[0][1:])

    def sync_comboboxes(self, combo_box, value) -> None:
        """
        Synchronize the value of combo boxes between the two tabs.
        """
        if combo_box == self.ui.comboBoxSpoke:
            self.ui.comboBoxSpoke2.setCurrentText(value)
        elif combo_box == self.ui.comboBoxSpoke2:
            self.ui.comboBoxSpoke.setCurrentText(value)

    def sync_manufacturer_selection(self, sender: QComboBox, index: int) -> None:
        """
        Synchronize the manufacturer selection between the
        Database Tab and Measurement Tab. Trigger loading
        of spokes for the selected manufacturer.
        """
        combo1: QComboBox = self.ui.comboBoxManufacturer
        combo2: QComboBox = self.ui.comboBoxManufacturer2
        selected_manufacturer_id: int = sender.itemData(index)

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

        self.load_spokes()

    def load_manufacturers(self) -> None:
        """
        Load all manufacturer names from the database and populate the
        the dropdowns. Automatically loads spokes for the first manufacturer.
        """
        # Load manufacturers
        manufacturers: list[Any] = self.db.execute_select(
            query=SQLQueries.GET_MANUFACTURERS)
        if not manufacturers:
            return

        self.ui.comboBoxManufacturer.clear()
        self.ui.comboBoxManufacturer2.clear()
        for manufacturer in manufacturers:
            self.ui.comboBoxManufacturer.addItem(
                manufacturer[1], manufacturer[0])
            self.ui.comboBoxManufacturer2.addItem(
                manufacturer[1], manufacturer[0]
            )

        # Load types
        spoke_types: list[Any] = self.db.execute_select(
            query=SQLQueries.GET_TYPES)
        if not spoke_types:
            return

        self.ui.comboBoxType.clear()
        self.ui.comboBoxType2.clear()
        for spoke_type in spoke_types:
            self.ui.comboBoxType.addItem(
                spoke_type[1], spoke_type[0])
            self.ui.comboBoxType2.addItem(
                spoke_type[1], spoke_type[0])

        # Automatically load spokes for the first manufacturer
        if manufacturers:
            self.ui.comboBoxManufacturer.\
                setCurrentIndex(0)
            self.ui.comboBoxManufacturer2.\
                setCurrentIndex(0)
            self.load_spokes()

    def load_spokes(self) -> None:
        """
        Load all spokes for the currently selected manufacturer and populate
        the tableViewSpokesDatabase and comboBoxSpoke.
        """
        manufacturer_id: int | None = \
            self.ui.comboBoxManufacturer.currentData()

        if manufacturer_id is None:
            return
        manufacturer_id = int(manufacturer_id)

        spokes: list[Any] = self.db.execute_select(
            query=SQLQueries.GET_SPOKES_BY_MANUFACTURER,
            params=(manufacturer_id,))
        if not spokes:
            return

        headers: list[str] = [
            "Name",
            "Type",
            "Gauge",
            "Weight",
            "Dimensions",
            "Comment"]

        # Exclude ID
        self.current_spokes: list[tuple[Any, list[Any]]] = [
            (spoke[0], list(spoke[1:]))
            for spoke in spokes]
        model = SpokeTableModel(self.current_spokes, headers)
        view: QTableView = self.ui.tableViewSpokesDatabase
        view.setModel(model)

        # Populate comboBoxSpoke
        self.ui.comboBoxSpoke.clear()
        self.ui.comboBoxSpoke2.clear()
        for spoke in spokes:
            # Name and ID
            self.ui.comboBoxSpoke.addItem(
                spoke[1], spoke[0])
            self.ui.comboBoxSpoke2.addItem(
                spoke[1], spoke[0])

        # Adjust column widths
        resize_mode = view.horizontalHeader().setSectionResizeMode
        resize_mode(0, self.__rm_stretch)  # Name
        resize_mode(1, self.__rm_stretch)  # Type
        resize_mode(2, self.__rm_shrink)   # Gauge
        resize_mode(3, self.__rm_shrink)   # Weight
        resize_mode(4, self.__rm_stretch)  # Dimensions
        resize_mode(5, self.__rm_stretch)  # Comment

        # Configure table behavior
        view.setSelectionBehavior(self.__select_rows)
        view.setSelectionMode(self.__select_single)
        self.populate_filter_type()

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
        types: list[Any] = self.db.execute_select(SQLQueries.GET_TYPES)
        if not types:
            return

        # Populate comboBoxFilterType with applicable types
        self.ui.comboBoxFilterType.clear()
        # Empty means no filter is set
        self.ui.comboBoxFilterType.addItem("")

        for type_id, type_name in types:
            if type_name in type_ids_in_use:
                self.ui.comboBoxFilterType.addItem(type_name, type_id)

    def sort_by_column(self, column: int) -> None:
        """
        Sort the tableViewSpokesDatabase by the specified column.
        """
        self.current_spokes.sort(key=lambda x: x[1][column])
        self.ui.tableViewSpokesDatabase.model().layoutChanged.emit()

    def select_spoke_from_table(self, index: QModelIndex) -> None:
        """
        Select the corresponding spoke in comboBoxSpoke
        when a table row is clicked.
        """
        row = index.row()
        model: SpokeTableModel = cast(
            SpokeTableModel,
            self.ui.tableViewSpokesDatabase.model())
        spoke_id = model.get_id(row)

        if spoke_id is not None:
            combo_index = self.ui.comboBoxSpoke.findData(spoke_id)
            if combo_index != -1:
                self.ui.comboBoxSpoke.setCurrentIndex(combo_index)

    def select_spoke_row(self) -> None:
        """
        Select the corresponding row in tableViewSpokesDatabase
        based on the combobox.
        """
        res, spoke_id = self.get_selected_spoke_id()
        if not res:
            self.ui.tableViewSpokesDatabase.clearSelection()
            return

        model: SpokeTableModel = cast(
            SpokeTableModel,
            self.ui.tableViewSpokesDatabase.model())

        for row in range(model.rowCount()):
            if model.get_id(row) == spoke_id:
                self.ui.tableViewSpokesDatabase.selectRow(row)
                break

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

    def get_database_spoke_data(
            self, from_database: bool
            ) -> tuple[int, int, float, str, str, str]:
        """
        DRY helper
        """
        try:
            if from_database:
                return int(self.ui.comboBoxType.currentData()), \
                    int(self.ui.lineEditGauge.text() or 0), \
                    float(self.ui.lineEditWeight.text() or 0.0), \
                    self.ui.lineEditName.text() or "", \
                    self.ui.lineEditDimension.text() or "", \
                    self.ui.lineEditSpokeComment.text() or ""
            else:
                return int(self.ui.comboBoxType2.currentData()), \
                    int(self.ui.lineEditGauge2.text() or 0), \
                    float(self.ui.lineEditWeight2.text() or 0.0), \
                    self.ui.lineEditName2.text() or "", \
                    self.ui.lineEditDimension2.text() or "", \
                    self.ui.lineEditSpokeComment2.text() or ""

        except ValueError as e:
            logging.error(f"Invalid data provided: {e}")
            raise

    def modify_spoke(self) -> None:
        """
        Update the selected spoke with new values from the detail fields.
        """
        res, spoke_id = self.get_selected_spoke_id()
        if not res:
            return

        type_id, gauge, weight, \
            spoke_name, dimension, comment = \
            self.get_database_spoke_data(True)

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
        res, spoke_id = self.get_selected_spoke_id()
        if not res:
            return

        _ = self.db.execute_query(
            query=SQLQueries.DELETE_SPOKE,
            params=(spoke_id,)
        )
        self.load_spokes()
        # Clear selection
        self.ui.comboBoxSpoke.setCurrentIndex(-1)
        self.ui.tableViewSpokesDatabase.clearSelection()

    def filter_spoke_table(self) -> None:
        """
        Filter tableViewSpokesDatabase based on filter inputs.
        """
        name_filter: str = self.ui.lineEditFilterName.text().lower()
        type_filter: str = self.ui.comboBoxFilterType.currentText().lower()
        gauge_filter: str = self.ui.lineEditFilterGauge.text().lower()

        filtered_data: list[tuple[int, list[str]]] = [
            spoke for spoke in self.current_spokes
            if (name_filter in spoke[1][0].lower()) and  # Match Name
            (type_filter == spoke[1][1].lower()
             if type_filter else True) and  # Match Type
            (gauge_filter in str(spoke[1][2]).lower()
             if gauge_filter else True)  # Match Gauge
        ]

        # Update the table model with filtered data
        headers: list[str] = [
            "Name",
            "Type",
            "Gauge",
            "Weight",
            "Dimensions",
            "Comment"]
        model = SpokeTableModel(filtered_data, headers)
        self.ui.tableViewSpokesDatabase.setModel(model)

    def align_filters_with_table(self) -> None:
        """
        Align filter fields with tableViewSpokesDatabase columns.
        """
        if not self.ui.tableViewSpokesDatabase.isVisible():
            return

        header: QHeaderView = \
            self.ui.tableViewSpokesDatabase.horizontalHeader()

        # Get column positions and sizes
        offset_x: int = self.ui.tableViewSpokesDatabase.geometry().x() + \
            header.sectionPosition(0)
        name_pos: int = header.sectionPosition(0) + offset_x
        name_width: int = header.sectionSize(0)
        type_pos: int = header.sectionPosition(1) + offset_x
        type_width: int = header.sectionSize(1)
        gauge_pos: int = header.sectionPosition(2) + offset_x
        gauge_width: int = header.sectionSize(2)

        # Update filter field positions and sizes
        self.ui.lineEditFilterName.setGeometry(
            name_pos,
            self.ui.lineEditFilterName.y(),
            name_width,
            self.ui.lineEditFilterName.height())
        self.ui.comboBoxFilterType.setGeometry(
            type_pos,
            self.ui.comboBoxFilterType.y(),
            type_width,
            self.ui.comboBoxFilterType.height())
        self.ui.lineEditFilterGauge.setGeometry(
            gauge_pos,
            self.ui.lineEditFilterGauge.y(),
            gauge_width,
            self.ui.lineEditFilterGauge.height())