from typing import Any
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem
from quartic_fit import PiecewiseQuarticFit
from setup_module import SetupModule
from customtablewidget import CustomTableWidget

class MeasurementModule:

    def __init__(self,
                 main_window: QMainWindow,
                 ui: Any) -> None:
        self.ui = ui
        self.main_window: QMainWindow = main_window
        self.setup_module = SetupModule

    def calculate_formula(self,
                          column: int) -> tuple[list[tuple[int, float]], str]:
        """
        Calculate the quartic fit formula for the specified column.
        :param column: The column index to extract measurements from.
        :return: The calculated fit formula as a string.
        :raises ValueError: If data is invalid or the formula cannot be calculated.
        """
        table: CustomTableWidget = self.ui.tableWidgetMeasurements
        # Determine the measurement direction
        if self.ui.radioButtonMeasurementUp.isChecked():
            tensions = list(range(300, 1700, 100))  # 300 N to 1600 N
        elif self.ui.radioButtonMeasurementDown.isChecked():
            tensions = list(range(1600, 200, -100))  # 1600 N to 300 N
        else:
            raise ValueError("Measurement direction not selected")

        # Extract deflection values and pair with tensions
        measurements : list[tuple[int, float]] = []
        for i, tension in enumerate(tensions):
            row: int = (i if self.ui.radioButtonMeasurementUp.isChecked()
                        else len(tensions) - 1 - i)
            item: QTableWidgetItem | None = table.item(row, column)
            if item and item.text().strip():
                try:
                    deflection = float(item.text().replace(",", "."))
                    measurements.append((tension, deflection))
                except ValueError:
                    raise ValueError("Invalid data in table")

        if not measurements:
            raise ValueError("No data in selected column")

        # Run the quartic fit model
        return measurements, PiecewiseQuarticFit.generate_model(measurements)

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
            _, fit = self.calculate_formula(selected_column)
            self.ui.lineEditFormula.setText(fit)
        except ValueError as e:
            self.ui.lineEditFormula.setText(str(e))
        except Exception as e:
            self.ui.lineEditFormula.setText(f"Error calculating formula: {e}")


    def activate_first_cell(self) -> None:
        """
        Activate the first cell in tableWidgetMeasurements.
        """
        table = self.ui.tableWidgetMeasurements
        if table.rowCount() > 0 and table.columnCount() > 0:
            table.setCurrentCell(0, 0)
            table.setFocus()

    def move_to_next_cell(self) -> None:
        """
        Move to the next editable cell in tableWidgetMeasurements.
        Wrap around rows and columns as needed.
        """
        table = self.ui.tableWidgetMeasurements
        current_row = table.currentRow()
        current_column = table.currentColumn()

        if current_row == -1 or current_column == -1:
            return

        # Calculate the next cell
        if current_column < table.columnCount() - 1:
            target_row = current_row
            target_column = current_column + 1
        else:
            target_row = (current_row + 1) % table.rowCount()
            target_column = 0

        # Ugly hack
        QTimer.singleShot(50, lambda: table.setCurrentCell(target_row, target_column))

    def move_to_previous_cell(self) -> None:
        """
        Move to the previous editable cell in tableWidgetMeasurements.
        Wrap around to the previous row/column if needed.
        """
        table = self.ui.tableWidgetMeasurements
        current_row = table.currentRow()
        current_column = table.currentColumn()

        if current_row == -1 or current_column == -1:
            return

        # Calculate the previous cell
        if current_column > 0:
            target_row = current_row
            target_column = current_column - 1
        else:
            # Wrap around to the last column of the previous row
            target_row = (current_row - 1) if current_row > 0 else table.rowCount() - 1
            target_column = table.columnCount() - 1

        # Set the previous cell as active
        table.setCurrentCell(target_row, target_column)
        table.setFocus()

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
            self.ui.pushButtonCalculateFormula.setEnabled(all_filled)
            self.ui.pushButtonSaveMeasurement.setEnabled(all_filled)
        else:
            self.ui.pushButtonCalculateFormula.setEnabled(False)
            self.ui.pushButtonSaveMeasurement.setEnabled(False)
