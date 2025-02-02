import logging
import time
from typing import Any, cast
from PySide6.QtCore import Qt
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QTableWidget
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtWidgets import QHeaderView
from ui import Ui_mainWindow
from enum import Enum
from setup_module import SetupModule
from helpers import Messagebox, Generics, TextChecker
from customtablewidget import CustomTableWidget, NumericTableWidgetItem
from sql_queries import SQLQueries
from unit_module import UnitEnum, UnitModule
from database_module import DatabaseModule
from tensiometer_module import TensiometerModule
from fast_visualisation_module import PyQtGraphCanvas, VisualisationModule
from calculation_module import TensionDeflectionFitter, FitType


class MeasurementModeEnum(Enum):
    DEFAULT = 0
    EDIT = 1
    CUSTOM = 2


class MeasurementModule:

    def __init__(self,
                 main_window: QMainWindow,
                 ui: Ui_mainWindow,
                 unit_module: UnitModule,
                 tensiometer_module: TensiometerModule,
                 messagebox: Messagebox,
                 db: DatabaseModule,
                 fitter: TensionDeflectionFitter,
                 chart: VisualisationModule,
                 canvas: PyQtGraphCanvas) -> None:
        self.ui: Ui_mainWindow = ui
        self.unit_module: UnitModule = unit_module
        self.main_window: QMainWindow = main_window
        self.setup_module = SetupModule
        self.messagebox: Messagebox = messagebox
        self.tensiometer_module: TensiometerModule = tensiometer_module
        self.db: DatabaseModule = db
        self.fitter: TensionDeflectionFitter = fitter
        self.canvas: PyQtGraphCanvas = canvas
        self.chart: VisualisationModule = chart
        self.__mode: MeasurementModeEnum = MeasurementModeEnum.DEFAULT
        self.__add_row_signal_connected = False

    def set_mode(self, mode: MeasurementModeEnum) -> None:
        if mode == MeasurementModeEnum.DEFAULT:
            if self.ui.radioButtonMeasurementCustom.isChecked:
                mode = MeasurementModeEnum.CUSTOM
        self.__mode = mode

    def update_measurement_button_states(self) -> None:
        """
        Enable or disable measurement buttons based
        on the completeness of the current column.
        """
        view: CustomTableWidget = self.ui.tableWidgetMeasurements
        selected_column: int = view.currentColumn()

        if selected_column != -1:
            all_filled: bool = all(
                view.item(row, selected_column) and
                view.item(row, selected_column).text().strip() # type: ignore
                for row in range(view.rowCount())
            )
            self.ui.pushButtonSaveMeasurement.setEnabled(all_filled)
        else:
            self.ui.pushButtonSaveMeasurement.setEnabled(False)

    def load_measurements(
            self,
            spoke_id: int | None,
            tensiometer_id: int | None,
            list_only: bool) -> list[Any] | None:
        """
        Load all measurements for the selected spoke and tensiometer
        and populate the measurement list.
        Each row corresponds to a measurement set with:
        - The first column as a comment
        - The second as the timestamp (up to minutes)
        - Subsequent columns displaying tension:deflection pairs with unit conversion.
        """
        if spoke_id is None:
            spoke_id = Generics.get_selected_row_id(
                self.ui.tableWidgetSpokesDatabase)

        if tensiometer_id is None:
            tensiometer_id = self.tensiometer_module.get_primary_tensiometer()
        view: QTableWidget = self.ui.tableWidgetMeasurementList

        if spoke_id < 0 or tensiometer_id < 0:
            view.clearContents()
            view.setRowCount(0)
            return None

        # Fetch measurement sets
        measurement_sets: list[Any] = self.db.execute_select(
            query=SQLQueries.GET_MEASUREMENT_SETS,
            params=(spoke_id, tensiometer_id)
        )

        if not measurement_sets:
            view.clearContents()
            view.setRowCount(0)
            return None

        # Fetch all measurements linked to the retrieved measurement sets
        set_ids: list[Any] = [ms[0] for ms in measurement_sets]
        query_string: str = f"{SQLQueries.GET_MEASUREMENTS} " \
                            f"({', '.join('?' for _ in set_ids)}) ORDER BY tension ASC"
        measurements: list[Any] = self.db.execute_select(
            query=query_string,
            params=set_ids
        )

        if not measurements:
            view.clearContents()
            view.setRowCount(0)
            return None

        if list_only:
            return measurements

        # Prepare rows for the table
        unit: UnitEnum = self.unit_module.get_unit()

        # Prepare set information and initialize the data structure
        set_info: dict[Any, Any] = {ms[0]: ms[1:] for ms in measurement_sets}
        data: list[tuple[Any, list[str]]] = []

        # Organize measurements by set and sort by tension
        grouped_measurements = {}
        for set_id, tension, deflection in measurements:
            if set_id not in grouped_measurements:
                grouped_measurements[set_id] = []
            # Convert the tension to the selected unit
            converted_tensions: tuple[float, float, float] = \
                self.unit_module.convert_units(value=tension, source=UnitEnum.NEWTON)
            tension_converted: str = {
                UnitEnum.NEWTON: f"{converted_tensions[0]:.0f}N",
                UnitEnum.KGF: TextChecker.check_text(f"{converted_tensions[1]:.1f} kgF", True),
                UnitEnum.LBF: TextChecker.check_text(f"{converted_tensions[2]:.1f} lbF", True)
            }[unit]
            # Add the tension-deflection pair to the set's measurements
            grouped_measurements[set_id].append((tension, f"{tension_converted}: {deflection:.2f}mm"))

        # Build rows for each set, with measurements sorted by tension
        for set_id, measurements_list in grouped_measurements.items():
            comment, ts = set_info[set_id]
            timestamp = ts.rsplit(":", 1)[0]  # Truncate to minutes
            row_data = [comment, timestamp] + [m[1] for m in measurements_list]
            data.append((set_id, row_data))

        # Update the table
        view.clearContents()
        view.setRowCount(len(data))
        view.setColumnCount(max(len(row[1]) for row in data))  # Ensure enough columns

        for row_idx, (row_id, row_data) in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                item = NumericTableWidgetItem(cell_data)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                if col_idx == 0:  # Store the ID in the first visible column
                    item.setData(Qt.ItemDataRole.UserRole, row_id)
                view.setItem(row_idx, col_idx, item)

        # Adjust column sizes
        header: QHeaderView = view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        # Hide headers
        view.verticalHeader().setVisible(False)
        view.horizontalHeader().setVisible(False)
        return None

    def delete_measurement(self) -> None:
        """
        Delete the currently selected measurement from the measurements list.
        Deletes only if a valid measurement row is selected or if there's only one measurement.
        """
        view: QTableWidget = self.ui.tableWidgetMeasurementList
        measurement_id: int = Generics.get_selected_row_id(view)
        if (measurement_id < 0):
            return
        # Execute the deletion query
        try:
            self.db.execute_query(
                query=SQLQueries.DELETE_MEASUREMENT_SET,
                params=(measurement_id,)
            )
        except Exception as e:
            self.messagebox.err(f"Failed to delete measurement: {str(e)}")
            return

        # Clear selection, update the table, and inform the user
        view.clearSelection()
        self.load_measurements(None, None, False)
        self.messagebox.info("Measurement deleted.")

    def select_measurement_row(self, index: QModelIndex) -> None:
        """
        Handle row selection in the measurement list
        This function ensures that the correct measurement row is highlighted.
        """
        if not index.isValid():
            return

        row: int = index.row()
        self.ui.tableWidgetMeasurementList.selectRow(row)

    def setup_measurements_table(self) -> None:
        """
        Set up the tableWidgetMeasurements based on the current mode.
        - If self.__edit_mode is False and self.__custom_mode is False:
            Populate with editable tension values and tensiometers.
        - If self.__edit_mode is True:
            Populate with tension:deflection pairs for the selected measurement.
        - If self.__edit_mode is False and self.__custom_mode is True:
            Prepare an empty table with one editable row for custom entries.
        """
        view: CustomTableWidget = self.ui.tableWidgetMeasurements
        view.clearContents()
        view.setRowCount(0)
        view.setColumnCount(0)

        match self.__mode:
            case MeasurementModeEnum.DEFAULT:
                self.populate_measurements_table_default(view)
            case MeasurementModeEnum.EDIT:
                self.populate_measurements_table_edit_mode(view, False)
            case MeasurementModeEnum.CUSTOM:
                self.populate_measurements_table_edit_mode(view, True)

    def populate_measurements_table_default(
            self,
            view: CustomTableWidget) -> None:
        """
        Populate the table with editable tension values and tensiometers.
        """
        if self.__add_row_signal_connected:
            view.verticalHeader().sectionClicked.disconnect(
                self.insert_empty_row_below)
        # Handle the measurement direction
        if self.ui.radioButtonMeasurementDown.isChecked():
            tensions_newton = list(range(1600, 200, -100))
        else:
            tensions_newton = list(range(300, 1700, 100))

        # Convert tensions to the selected unit
        unit_index_map: dict[UnitEnum, int] = {
            UnitEnum.NEWTON: 0,
            UnitEnum.KGF: 1,
            UnitEnum.LBF: 2,
        }
        unit_index: int = unit_index_map[self.unit_module.get_unit()]
        tensions_converted: list[float] = [
            self.unit_module.convert_units(
                value=value,
                source=UnitEnum.NEWTON)[unit_index]
            for value in tensions_newton
        ]

        # Set row headers
        view.setRowCount(len(tensions_converted))
        unit: UnitEnum = self.unit_module.get_unit()
        row_headers: list[str] = [
            f"{value} {unit.value}"
            if unit == UnitEnum.NEWTON
            else f"{TextChecker.check_text(f'{value:.1f}', True)} {unit.value}"
            for value in tensions_converted
        ]
        view.setVerticalHeaderLabels(row_headers)

        # Populate column headers with selected tensiometers
        tensiometers: list[tuple[int, str]] = \
            self.tensiometer_module.get_selected_tensiometers()
        view.setColumnCount(len(tensiometers))
        for column, (
            tensiometer_id,
            tensiometer_name) in enumerate(tensiometers):

            item = QTableWidgetItem(tensiometer_name)
            item.setData(Qt.ItemDataRole.UserRole, tensiometer_id)
            view.setHorizontalHeaderItem(column, item)

        # Populate cells
        for row in range(len(tensions_converted)):
            for column in range(len(tensiometers)):
                item = NumericTableWidgetItem()
                item.setFlags(
                    Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled)
                view.setItem(row, column, item)

        # Move focus to the first cell
        view.move_to_specific_cell(0, 0)

    def populate_measurements_table_edit_mode(
            self,
            view: CustomTableWidget, custom_mode: bool) -> None:
        """
        Populate the table with tension:deflection pairs
        for the selected measurement.
        """
        # Set the headers
        unit: UnitEnum = self.unit_module.get_unit()
        view.setColumnCount(2)
        view.setHorizontalHeaderLabels([
            f"Tension ({unit.value})", "Deflection"])
        view.setVerticalHeaderLabels(["+"] * (1 if custom_mode else 0))

        if custom_mode:
            # Add one empty editable row
            view.setRowCount(1)
            for column in range(2):
                item = NumericTableWidgetItem()
                item.setFlags(
                    Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled)
                # Initialize with an empty string or a locale-formatted zero
                # Here, we'll use an empty string to prevent sorting
                cell_text = ""
                item.setText(cell_text)
                # Do not set UserRole initially
                view.setItem(0, column, item)
        else:
            # Load measurements as a list
            measurements = self.load_measurements(
                spoke_id=None,
                tensiometer_id=None,
                list_only=True)
            measurement_id: int = Generics.get_selected_row_id(
                self.ui.tableWidgetMeasurementList)
            if measurement_id < 0 or not measurements:
                return

            # Filter measurements for the selected ID
            filtered_measurements = [
                (mid, tension, deflection)
                for mid, tension, deflection in measurements
                if mid == measurement_id
            ]

            if not filtered_measurements:
                return

            # Prepare table headers
            view.setRowCount(len(filtered_measurements))
            view.setVerticalHeaderLabels(["+"] * len(filtered_measurements))

            # Populate the table
            unit_index_map: dict[UnitEnum, int] = {
                UnitEnum.NEWTON: 0,
                UnitEnum.KGF: 1,
                UnitEnum.LBF: 2,
            }
            unit_index: int = unit_index_map[unit]

            for row, (_, tension, deflection) in enumerate(
                filtered_measurements):
                # Convert tension to the selected unit
                converted_tension: float = self.unit_module.convert_units(
                    tension,
                    UnitEnum.NEWTON)[unit_index]

                # Format numbers according to locale
                tension_text: str = TextChecker.check_text(str(converted_tension), True)
                deflection_text: str = TextChecker.check_text(str(deflection), True)

                tension_item = NumericTableWidgetItem(tension_text)
                tension_item.setFlags(
                    Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled)
                deflection_item = NumericTableWidgetItem(deflection_text)
                deflection_item.setFlags(
                    Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled)

                # Set UserRole data for sorting
                try:
                    tension_item.setData(Qt.ItemDataRole.UserRole, tension)
                except ValueError:
                    logging.error(f"Invalid value '{tension_text}' at 1:{row}")
                    tension_item.setData(Qt.ItemDataRole.UserRole, None)

                try:
                    deflection_item.setData(Qt.ItemDataRole.UserRole, deflection)
                except ValueError:
                    logging.error(f"Invalid value '{deflection}' at 1:{row}")
                    deflection_item.setData(Qt.ItemDataRole.UserRole, None)

                view.setItem(row, 0, tension_item)
                view.setItem(row, 1, deflection_item)

        # Enable sorting by columns and sort by tension
        view.setSortingEnabled(True)
        view.sortItems(0, Qt.SortOrder.AscendingOrder)

        # Connect the row header click signal
        if not self.__add_row_signal_connected:
            self.__add_row_signal_connected = True
            view.verticalHeader().sectionClicked.connect(
                self.insert_empty_row_below)
        self.plot_measurements()

    def insert_empty_row_below(self, row: int) -> None:
        """
        Insert an empty row below the clicked row header.
        """
        view: CustomTableWidget = self.ui.tableWidgetMeasurements
        row += 1
        view.insertRow(row)
        row_headers: list[str] = ["+"] * view.rowCount()
        view.setVerticalHeaderLabels(row_headers)
        view.move_to_specific_cell(row, 0)

    def on_cell_changing(self, row: int, column: int, value: str) -> None:
        if self.__mode == MeasurementModeEnum.DEFAULT:
            return

        try:
            parsed_val = float(value.replace(",", "."))
        except ValueError:
            return

        view: CustomTableWidget = self.ui.tableWidgetMeasurements
        view.setSortingEnabled(False)

        if column == 0:
            converted_tensions: tuple[float, float, float] = \
            self.unit_module.convert_units(
                value=parsed_val,
                source=self.unit_module.get_unit())
            print(f"Tension: {converted_tensions[0]}")
            tension_item = NumericTableWidgetItem(value)
            tension_item.setFlags(
                Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled)
            try:
                tension_item.setData(Qt.ItemDataRole.UserRole, converted_tensions[0])
            except ValueError:
                logging.error(f"Invalid value '{value}' at {column}:{row}")
                tension_item.setData(Qt.ItemDataRole.UserRole, None)
            view.setItem(row, 0, tension_item)
        else:
            print(f"Deflection: {parsed_val}")
            deflection_item = NumericTableWidgetItem(value)
            deflection_item.setFlags(
                Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled)
            try:
                deflection_item.setData(Qt.ItemDataRole.UserRole, parsed_val)
            except ValueError:
                logging.error(f"Invalid value '{value}' at {column}:{row}")
                deflection_item.setData(Qt.ItemDataRole.UserRole, None)
            view.setItem(row, 1, deflection_item)

    def move_to_next_cell(self, no_delay: bool) -> None:
        """
        Callback for moving to the next cell in the table.
        Moves to the cell below if possible, otherwise to the first cell
        of the next column if possible. If in edit/custom mode and the cell is
        the last one, adds an empty row below and goes to the first cell of it.

        :param no_delay: If True, immediately move to the next cell.
                        Otherwise, introduce a slight delay.
        """
        self.plot_measurements()
        view: CustomTableWidget = self.ui.tableWidgetMeasurements
        row: int = view.currentRow()
        column: int = view.currentColumn()

        print(f"column: {column} row {row}")
        item: QTableWidgetItem | None = view.itemAt(row, column)
        print(item)
        if item is not None:
            print(f"Item role = {item.data(Qt.ItemDataRole.UserRole)}")
            print(f"Item text = {item.text()}")

        if column < view.columnCount() - 1:
            column += 1
        elif row < view.rowCount() - 1:
            column = 0
            row += 1
        else:
            if self.__mode == MeasurementModeEnum.DEFAULT:
                return  # Already at the last cell
            time.sleep(0.05)
            self.insert_empty_row_below(row)
            column = 0
            row += 1

        # Delay to ensure Qt's focus/selection state is updated
        if no_delay:
            view.move_to_specific_cell(row, column)
        else:
            QTimer.singleShot(50,
                lambda: view.move_to_specific_cell(
                    row=row, column=column))

    def save_measurements(self) -> None:
        """
        Save measurement data for all columns in tableWidgetMeasurements.
        Handles different modes: DEFAULT, EDIT, and CUSTOM.
        """
        view: CustomTableWidget = self.ui.tableWidgetMeasurements

        # Ensure a valid spoke ID is selected
        spoke_id: int = Generics.get_selected_row_id(self.ui.tableWidgetSpokesDatabase)
        if spoke_id < 0:
            self.messagebox.err("No spoke selected")
            return

        # Get the comment
        comment: str = self.ui.lineEditMeasurementComment.text().strip()

        # Check the mode and handle accordingly
        match self.__mode:
            case MeasurementModeEnum.DEFAULT:
                # Save default mode measurements
                self.__save_default_mode_measurements(view, spoke_id, comment)
            case MeasurementModeEnum.EDIT | MeasurementModeEnum.CUSTOM:
                # Save edit or custom mode measurements
                self.__save_custom_mode_measurements(view, spoke_id, comment)

        # Notify the user
        self.messagebox.info("Measurements saved successfully")
        self.load_measurements(None, None, False)

    def __save_default_mode_measurements(
            self, view: CustomTableWidget, spoke_id: int, comment: str) -> None:
        """
        Save measurements in DEFAULT mode with multiple tensiometers.
        """
        for column in range(view.columnCount()):
            # Fetch the tensiometer ID for the column
            header_item: QTableWidgetItem | None = view.horizontalHeaderItem(column)
            if header_item is None:
                self.messagebox.err(f"Column {column + 1}: Missing header")
                return

            tensiometer_id = header_item.data(Qt.ItemDataRole.UserRole)
            if tensiometer_id is None:
                self.messagebox.err(f"Column {column + 1}: Missing tensiometer ID")
                return

            # Validate and gather tension-deflection data
            data: list[tuple[float, float]] = []
            for row in range(view.rowCount()):
                tension_item: NumericTableWidgetItem = cast(NumericTableWidgetItem, view.verticalHeaderItem(row))
                deflection_item: NumericTableWidgetItem = cast(NumericTableWidgetItem, view.item(row, column))

                if tension_item is None or deflection_item is None:
                    self.messagebox.err(f"Row {row + 1}: Missing data in column {column + 1}")
                    return

                try:
                    tension = float(tension_item.text().split()[0])
                    deflection = float(deflection_item.text())
                    data.append((tension, deflection))
                except ValueError:
                    self.messagebox.err(f"Row {row + 1}, Column {column + 1}: Invalid data")
                    return

            # Save the data to the database
            self.__save_measurement_set(
                spoke_id=spoke_id,
                tensiometer_id=tensiometer_id,
                data=data,
                comment=comment)

    def __save_custom_mode_measurements(
                self, view: CustomTableWidget, spoke_id: int, comment: str) -> None:
        """
        Save measurements in EDIT or CUSTOM mode.
        In EDIT mode, delete the existing measurement set before saving new data.
        """
        # Fetch the tensiometer ID for the column (assumes a single tensiometer)
        tensiometer_id = self.tensiometer_module.get_primary_tensiometer()
        if tensiometer_id < 0:
            self.messagebox.err("No tensiometer selected")
            return

        # Validate and gather tension-deflection data
        data: list[tuple[float, float]] = []
        for row in range(view.rowCount()):
            tension_item = view.item(row, 0)
            deflection_item = view.item(row, 1)

            if tension_item is None or deflection_item is None:
                continue  # Ignore rows with missing data

            try:
                tension = float(tension_item.text())
                deflection = float(deflection_item.text())
                data.append((tension, deflection))
            except ValueError:
                continue  # Ignore rows with invalid data

        if not data:
            self.messagebox.err("No valid data to save")
            return

        # Handle EDIT mode: Delete the existing measurement set
        if self.__mode == MeasurementModeEnum.EDIT:
            # Get the current measurement set ID
            measurement_id: int = Generics.get_selected_row_id(self.ui.tableWidgetMeasurementList)
            if measurement_id < 0:
                self.messagebox.err("No measurement set selected to overwrite")
                return

            # Delete the existing measurement set
            try:
                self.db.execute_query(
                    query=SQLQueries.DELETE_MEASUREMENT_SET,
                    params=(measurement_id,)
                )
            except Exception as ex:
                self.messagebox.err(f"Failed to delete previous measurement set: {str(ex)}")
                return

        # Save the new data
        self.__save_measurement_set(spoke_id, tensiometer_id, data, comment)

    def __save_measurement_set(
            self,
            spoke_id: int,
            tensiometer_id: int,
            data: list[tuple[float, float]],
            comment: str) -> None:
        """
        Save a single measurement set and its associated measurements.
        """
        # Save the measurement set
        set_id = self.db.execute_query(
            query=SQLQueries.ADD_MEASUREMENT_SET,
            params=(spoke_id, tensiometer_id, comment)
        )
        if set_id is None:
            self.messagebox.err("Failed to save measurement set")
            return

        # Save each measurement
        for tension, deflection in data:
            try:
                self.db.execute_query(
                    query=SQLQueries.ADD_MEASUREMENT,
                    params=(set_id, tension, deflection)
                )
            except Exception as ex:
                self.messagebox.err(f"Failed to save measurement: {str(ex)}")

    def plot_measurements(self) -> None:
        """
        Gathers tension/deflection data from a QTableWidget,
        fits it, and plots inside the verticalLayoutMeasurementRight.
        """
        # Collect data from tableWidgetMeasurements
        data = []
        row_count: int = self.ui.tableWidgetMeasurements.rowCount()
        for row in range(row_count):
            tension_item: QTableWidgetItem | None = \
                self.ui.tableWidgetMeasurements.item(row, 0)
            deflection_item: QTableWidgetItem | None = \
                self.ui.tableWidgetMeasurements.item(row, 1)

            # Check that both cells exist and are not empty
            if tension_item and deflection_item:
                tension_text: str = tension_item.text().strip()
                deflection_text: str = deflection_item.text().strip()
                if tension_text and deflection_text:
                    # Attempt to parse floats
                    try:
                        tension_val = float(tension_text.replace(",", "."))
                        deflection_val = float(deflection_text.replace(",", "."))
                        data.append((tension_val, deflection_val))
                    except ValueError:
                        # Non-numeric in that row => skip it
                        pass

        if not data:
            print("No valid tension/deflection data found.")
            return

        data.sort(key=lambda pair: pair[0])
        fit_type, header = self.get_fit()
        fit_model = self.fitter.fit_data(data, fit_type)

        self.canvas.clear()
        self.chart.update_fit_plot(
            plot_widget=self.canvas.plot_widget,
            fit_model=fit_model,
            data=data,
            step=10.0,
            deviation_range=(-20, 20),
            header=f"{header} fit"
        )

    def get_fit(self) -> tuple[FitType, str]:
        if self.ui.radioButtonFitQuadratic.isChecked():
            return FitType.QUADRATIC, "Quadratic"
        if self.ui.radioButtonFitCubic.isChecked():
            return FitType.CUBIC, "Cubic"
        if self.ui.radioButtonFitQuartic.isChecked():
            return FitType.QUARTIC, "Quartic"
        if self.ui.radioButtonFitSpline.isChecked():
            return FitType.SPLINE, "Spline"
        if self.ui.radioButtonFitExponential.isChecked():
            return FitType.EXPONENTIAL, "Exponential"
        if self.ui.radioButtonFitLogarithmic.isChecked():
            return FitType.LOGARITHMIC, "Logarithmic"
        if self.ui.radioButtonFitPowerLaw.isChecked():
            return FitType.POWER_LAW, "Power law"
        return FitType.LINEAR, "Linear"

