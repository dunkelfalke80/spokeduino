import logging
from typing import Any, cast
from PySide6.QtCore import Qt
from PySide6.QtCore import QTranslator
from PySide6.QtCore import QModelIndex
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QHeaderView
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QTableWidget
from PySide6.QtWidgets import QTableView
from PySide6.QtWidgets import QTableWidgetItem
from database_module import DatabaseModule
from sql_queries import SQLQueries
from helpers import SpokeTableModel
from unit_converter import UnitConverter
from unit_converter import UnitEnum

class SpokeModule:

    def __init__(self,
                 main_window: QMainWindow,
                 ui: Any,
                 unit_converter: UnitConverter,
                 db: DatabaseModule,
                 current_path: str) -> None:
        self.ui = ui
        self.main_window: QMainWindow = main_window
        self.current_path: str = current_path
        self.translator = QTranslator()
        self.current_language = "en"
        self.db: DatabaseModule = db
        self.unit_converter: UnitConverter = unit_converter

        # Reducing verbosity
        self.__rm_stretch: QHeaderView.ResizeMode = \
            QHeaderView.ResizeMode.Stretch
        self.__rm_shrink: QHeaderView.ResizeMode =\
            QHeaderView.ResizeMode.ResizeToContents
        self.__select_rows: QAbstractItemView.SelectionBehavior = \
            QAbstractItemView.SelectionBehavior.SelectRows
        self.__select_single: QAbstractItemView.SelectionMode = \
            QAbstractItemView.SelectionMode.SingleSelection

        self._spoke_headers: list[str] = [
            "Name",
            "Type",
            "Gauge",
            "Weight",
            "Dimensions",
            "Comment"]


    def get_selected_spoke_id(self) -> tuple[bool, int]:
        spoke_id: int | None = self.ui.comboBoxSpoke.currentData()
        if spoke_id is None:
            return False, 0
        return True, int(spoke_id)

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
            self.ui.comboBoxManufacturer.\
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

        # Exclude ID
        self.current_spokes: list[tuple[Any, list[Any]]] = [
            (spoke[0], list(spoke[1:]))
            for spoke in spokes]
        view = self.ui.tableViewSpokesDatabase

        # Populate comboBoxSpoke
        self.ui.comboBoxSpoke.clear()
        for spoke in spokes:
            # Name and ID
            self.ui.comboBoxSpoke.addItem(
                spoke[1], spoke[0])
            broken here

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
        types: list[Any] = self.db.execute_select(SQLQueries.GET_TYPES, None)
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
        row: int = index.row()
        model: SpokeTableModel = cast(
            SpokeTableModel,
            self.ui.tableViewSpokesDatabase.model())
        spoke_id: int | None = model.get_id(row)

        if spoke_id is not None:
            combo_index = self.ui.comboBoxSpoke.findData(spoke_id)
            if combo_index != -1:
                self.ui.comboBoxSpoke.setCurrentIndex(combo_index)

    def select_spoke_row(self) -> None:
        """
        Select the corresponding row in tableViewSpokesDatabase
        based on the combobox.
        """
        view: QTableView = self.ui.tableViewSpokesDatabase
        model = SpokeTableModel(self.current_spokes, self._spoke_headers)
        view.setModel(model)
        res, spoke_id = self.get_selected_spoke_id()
        if not res:
            view.clearSelection()
            return

        model: SpokeTableModel = cast(
            SpokeTableModel,
            view.model())
        if model is None:
            return

        for row in range(model.rowCount()):
            if model.get_id(row) == spoke_id:
                view.selectRow(row)
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

    def get_spoke_data(
            self, from_database: bool
            ) -> tuple[int, int, float, str, str, str]:
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

    def modify_spoke(self) -> None:
        """
        Update the selected spoke with new values from the detail fields.
        """
        res, spoke_id = self.get_selected_spoke_id()
        if not res:
            return

        type_id, gauge, weight, \
            spoke_name, dimension, comment = \
            self.get_spoke_data(True)

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

    def load_measurements(
            self,
            spoke_id: int | None,
            tensiometer_id: int | None) -> list[Any] | None:
        """
        Load all measurements for the selected spoke and tensiometer
        and populate tableViewMeasurements.
        Each row corresponds to a measurement set
        with the first column as a comment,
        the second as the timestamp (up to minutes),
        and subsequent columns displaying
        tension:deflection pairs with unit conversion.
        """
        list_only: bool = False
        if spoke_id is None:
            res, spoke_id = self.get_selected_spoke_id()
        else:
            res: bool = True
            list_only = True

        if tensiometer_id is None:
            tensiometer_id = self.ui.comboBoxTensiometer.currentData()
        view: QTableWidget = self.ui.tableWidgetMeasurements

        if not res or tensiometer_id is None:
            view.clear()
            return None
        tensiometer_id = int(tensiometer_id)

        # Fetch measurement sets
        measurement_sets: list[Any] = self.db.execute_select(
            query=SQLQueries.GET_MEASUREMENT_SETS,
            params=(spoke_id, tensiometer_id)
        )

        if not measurement_sets:
            view.clear()
            return None

        # Fetch all measurements linked to the retrieved measurement sets
        set_ids: list[Any] = [ms[0] for ms in measurement_sets]
        query_string: str = f"{SQLQueries.GET_MEASUREMENTS} " \
            f"({', '.join('?' for _ in set_ids)}) ORDER BY tension ASC"
        measurements: list[Any] = self.db.execute_select(
            query=query_string,
            params=set_ids  # Pass the list directly
        )

        if not measurements:
            view.clear()
            return None

        if list_only:
            return measurements

        # Prepare rows for the table
        unit: UnitEnum = self.unit_converter.get_unit()

        # Prepare set information and initialize the data structure
        set_info: dict[Any, Any] = {ms[0]: ms[1:] for ms in measurement_sets}  # {set_id: (comment, timestamp)}
        data: list[tuple[Any, list[str]]] = []

        # Organize measurements by set and sort by tension
        grouped_measurements = {}
        for set_id, tension, deflection in measurements:
            if set_id not in grouped_measurements:
                grouped_measurements[set_id] = []
            # Convert the tension to the selected unit
            converted_tensions = self.unit_converter.convert_units(
                value=tension, source=UnitEnum.NEWTON
            )
            tension_converted = {
                UnitEnum.NEWTON: f"{converted_tensions[0]:.0f}N",
                UnitEnum.KGF: f"{converted_tensions[1]:.1f}kgF",
                UnitEnum.LBF: f"{converted_tensions[2]:.1f}lbF"
            }[unit]
            # Add the tension-deflection pair to the set's measurements
            grouped_measurements[set_id].append((tension, f"{tension_converted}: {deflection:.2f}mm"))

        # Build rows for each set, with measurements sorted by tension
        for set_id, measurements_list in grouped_measurements.items():
            comment, ts = set_info[set_id]
            timestamp = ts.rsplit(":", 1)[0]  # Trunc to minutes
            # Create the row: [comment, timestamp, sorted measurements]
            row = (comment, [timestamp] + [m[1] for m in measurements_list])
            data.append(row)

        view.setRowCount(len(data))  # Set the number of rows

        # Fill the table
        for row_idx, (row_id, row_data) in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                item = QTableWidgetItem(cell_data)
                # Make it read-only
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                if col_idx == 0:  # Store the ID in the first visible column
                    item.setData(Qt.ItemDataRole.UserRole, row_id)
                view.setItem(row_idx, col_idx, item)
        resize_mode = view.horizontalHeader().setSectionResizeMode
        resize_mode(self.__rm_shrink)
        return None
