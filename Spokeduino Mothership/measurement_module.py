from typing import Any
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QTableWidgetItem
from quartic_fit import PiecewiseQuarticFit
from setup_module import SetupModule
from table_helpers import FloatValidatorDelegate
from unit_converter import UnitConverter

class MeasurementModule:

    def __init__(self,
                 main_window: QMainWindow,
                 ui: Any,
                 setup_module: SetupModule,
                 unit_converter: UnitConverter) -> None:
        self.ui = ui
        self.main_window: QMainWindow = main_window
        self.setup_module = SetupModule
        self.unit_converter = unit_converter

    def setup_table_widget_measurements(self) -> None:
        """
        Set up the tableWidgetMeasurements with
        editable fields for tension values
        and selected tensiometers.
        """
        # Clear all cells, rows, and columns
        self.ui.tableWidgetMeasurements.clearContents()
        self.ui.tableWidgetMeasurements.setRowCount(0)
        self.ui.tableWidgetMeasurements.setColumnCount(0)

        # Handle the measurement direction
        if self.ui.radioButtonMeasurementDown.isChecked():
            tensions_newton = list(range(1600, 200, -100))
        else:
            tensions_newton = list(range(300, 1700, 100))

        # Handle the measurement units
        unit: str = "Newton"
        if self.ui.radioButtonKgF.isChecked():
            unit = "kgF"
        elif self.ui.radioButtonLbF.isChecked():
            unit = "lbF"
        tensions_converted = [
            self.unit_converter.convert_units(value, "newton")[{
                "Newton": 0,
                "kgF": 1,
                "lbF": 2}[unit]]
            for value in tensions_newton
        ]

        # Populate row headers with converted force values
        self.ui.tableWidgetMeasurements.setRowCount(len(tensions_converted))
        if unit == "Newton":
            self.ui.tableWidgetMeasurements.setVerticalHeaderLabels(
                [f"{value} {unit}" for value in tensions_converted]
            )
        else:
            self.ui.tableWidgetMeasurements.setVerticalHeaderLabels(
                [f"{value:.1f} {unit}" for value in tensions_converted]
            )

        # Get selected tensiometers and populate column headers
        tensiometers = self.setup_module.get_selected_tensiometers()
        self.ui.tableWidgetMeasurements.setColumnCount(len(tensiometers))
        self.ui.tableWidgetMeasurements.setHorizontalHeaderLabels(
            [tensiometer[1] for tensiometer in tensiometers]
        )

        delegate = FloatValidatorDelegate(self.ui.tableWidgetMeasurements)
        self.ui.tableWidgetMeasurements.setItemDelegate(delegate)

        # Make all cells editable
        for row in range(len(tensions_converted)):
            for col in range(len(tensiometers)):
                item = QTableWidgetItem()
                item.setFlags(Qt.ItemFlag.ItemIsEditable |
                              Qt.ItemFlag.ItemIsEnabled)
                self.ui.tableWidgetMeasurements.setItem(row, col, item)

    def update_measurement_button_states(self):
        """
        Enable or disable measurement buttons based
        on the completeness of the current column.
        """
        table = self.ui.tableWidgetMeasurements
        selected_column = table.currentColumn()

        if selected_column != -1:
            all_filled = all(
                table.item(row, selected_column) and
                table.item(row, selected_column).text().strip() # type: ignore
                for row in range(table.rowCount())
            )
            self.ui.pushButtonCalculateFormula.setEnabled(all_filled)
            self.ui.pushButtonSaveMeasurement.setEnabled(all_filled)
        else:
            self.ui.pushButtonCalculateFormula.setEnabled(False)
            self.ui.pushButtonSaveMeasurement.setEnabled(False)

    def calculate_formula(self):
        """
        Calculates the quartic fit equations for the spoke measurements and
        shows the calculated coefficients and the ranges in lineEditFormula
        """
        # Example measurements
        example_measurements: list[tuple[int, float]] = [
            (1500, 3.1),
            (1400, 3.05),
            (1300, 3.01),
            (1200, 2.95),
            (1100, 2.89),
            (1000, 2.82),
            (900, 2.76),
            (800, 2.67),
            (700, 2.57),
            (600, 2.49),
            (500, 2.34),
            (400, 2.2)
        ]

        # Create PiecewiseQuarticFit object
        fit: str = PiecewiseQuarticFit.generate_model(example_measurements)

        # Evaluate tension for a given deflection
        deflection_value = 3.06  # Example deflection
        tension: float = PiecewiseQuarticFit.evaluate(fit, deflection_value)
        self.ui.lineEditFormula.setText(f"{tension:.2f}")

    def move_to_previous_cell(self):
        """
        Navigate to the previous editable cell in tableWidgetMeasurements.
        Wrap around to the previous row/column if needed.
        """
        table = self.ui.tableWidgetMeasurements
        current_row = table.currentRow()
        current_column = table.currentColumn()

        # Calculate the previous cell
        if current_column > 0:
            target_row = current_row
            target_column = current_column - 1
        else:
            # Wrap around to the previous row
            target_row = (current_row - 1) \
                if current_row > 0  \
                else table.rowCount() - 1
            target_column = table.columnCount() - 1

        # Select the previous cell
        table.setCurrentCell(target_row, target_column)

    def move_to_next_cell(self):
        """
        Navigate to the next editable cell in tableWidgetMeasurements.
        Wrap around to the next row/column if needed.
        """
        table = self.ui.tableWidgetMeasurements
        current_row = table.currentRow()
        current_column = table.currentColumn()

        # Calculate the next cell
        if current_column < table.columnCount() - 1:
            target_row = current_row
            target_column = current_column + 1
        else:
            # Wrap around to the next row
            target_row = (current_row + 1) % table.rowCount()
            target_column = 0

        # Select the next cell
        table.setCurrentCell(target_row, target_column)