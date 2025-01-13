from typing import Any
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QTableWidget
from quartic_fit import PiecewiseQuarticFit
from setup_module import SetupModule

class MeasurementModule:

    def __init__(self,
                 main_window: QMainWindow,
                 ui: Any
                 ) -> None:
        self.ui = ui
        self.main_window: QMainWindow = main_window
        self.setup_module = SetupModule

    def calculate_formula(self, measurements: list[tuple[int, float]]) -> None:
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

        measurements = example_measurements

        # Create PiecewiseQuarticFit object
        fit: str = PiecewiseQuarticFit.generate_model(measurements)

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

    def update_measurement_button_states(self) -> None:
        """
        Enable or disable measurement buttons based
        on the completeness of the current column.
        """
        table: QTableWidget = self.ui.tableWidgetMeasurements
        selected_column: int = table.currentColumn()

        if selected_column != -1:
            all_filled: bool = all(
                table.item(row, selected_column) and
                table.item(row, selected_column).text().strip() # type: ignore
                for row in range(table.rowCount())
            )
            self.ui.pushButtonCalculateFormula.setEnabled(all_filled)
            self.ui.pushButtonSaveMeasurement.setEnabled(all_filled)
        else:
            self.ui.pushButtonCalculateFormula.setEnabled(False)
            self.ui.pushButtonSaveMeasurement.setEnabled(False)
