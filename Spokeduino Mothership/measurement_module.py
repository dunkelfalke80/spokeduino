from typing import Any
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QTableWidget
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtWidgets import QHeaderView
from setup_module import SetupModule
from helpers import Messagebox, Generics
from customtablewidget import CustomTableWidget
from sql_queries import SQLQueries
from unit_converter import UnitEnum, UnitConverter
from database_module import DatabaseModule

class MeasurementModule:

    def __init__(self,
                 main_window: QMainWindow,
                 ui: Any,
                 unit_converter: UnitConverter,
                 messagebox: Messagebox,
                 db: DatabaseModule) -> None:
        self.ui = ui
        self.unit_converter: UnitConverter = unit_converter
        self.main_window: QMainWindow = main_window
        self.setup_module = SetupModule
        self.messagebox: Messagebox = messagebox
        self.db: DatabaseModule = db

    def toggle_calculate_button(self) -> None:
        """
        Handle pushButtonCalculateFormula click event.
        """
        table = self.ui.tableWidgetMeasurements
        selected_column = table.currentColumn()

        if selected_column == -1:
            self.ui.lineEditFormula.setText("No column selected")
            return

        try:
            pass
        except ValueError as e:
            self.ui.lineEditFormula.setText(str(e))
        except Exception as e:
            self.ui.lineEditFormula.setText(f"Error calculating formula: {e}")

    def update_measurement_button_states(self) -> None:
        """
        Enable or disable measurement buttons based
        on the completeness of the current column.
        """
        table: CustomTableWidget = self.ui.tableWidgetMeasurements
        selected_column: int = table.currentColumn()

        if selected_column != -1:
            all_filled: bool = all(
                table.item(row, selected_column) and
                table.item(row, selected_column).text().strip() # type: ignore
                for row in range(table.rowCount())
            )
            self.ui.pushButtonSaveMeasurement.setEnabled(all_filled)
        else:
            self.ui.pushButtonSaveMeasurement.setEnabled(False)

    def load_measurements(
            self,
            spoke_id: int | None,
            tensiometer_id: int | None) -> list[Any] | None:
        """
        Load all measurements for the selected spoke and tensiometer
        and populate tableWidgetMeasurements.
        Each row corresponds to a measurement set
        with the first column as a comment,
        the second as the timestamp (up to minutes),
        and subsequent columns displaying
        tension:deflection pairs with unit conversion.
        """
        list_only: bool = False
        if spoke_id is None:
            view: QTableWidget = self.ui.tableWidgetSpokesDatabase
            spoke_id = Generics.get_selected_row_id(view)
        else:
            list_only = True

        if tensiometer_id is None:
            tensiometer_id = self.ui.comboBoxTensiometer.currentData()
        view: QTableWidget = self.ui.tableWidgetMeasurements

        if spoke_id is None or tensiometer_id is None:
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
        set_info: dict[Any, Any] = {ms[0]: ms[1:] for ms in measurement_sets}
        data: list[tuple[Any, list[str]]] = []

        # Organize measurements by set and sort by tension
        grouped_measurements = {}
        for set_id, tension, deflection in measurements:
            if set_id not in grouped_measurements:
                grouped_measurements[set_id] = []
            # Convert the tension to the selected unit
            converted_tensions: tuple[float, float, float] = \
                self.unit_converter.convert_units(
                value=tension, source=UnitEnum.NEWTON)
            tension_converted: str = {
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
        resize_mode(QHeaderView.ResizeMode.ResizeToContents)
        return None