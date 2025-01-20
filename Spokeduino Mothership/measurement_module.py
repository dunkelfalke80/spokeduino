from typing import Any
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem
from setup_module import SetupModule
from customtablewidget import CustomTableWidget

class MeasurementModule:

    def __init__(self,
                 main_window: QMainWindow,
                 ui: Any) -> None:
        self.ui = ui
        self.main_window: QMainWindow = main_window
        self.setup_module = SetupModule

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
            self.ui.pushButtonCalculateFormula.setEnabled(all_filled)
            self.ui.pushButtonSaveMeasurement.setEnabled(all_filled)
        else:
            self.ui.pushButtonCalculateFormula.setEnabled(False)
            self.ui.pushButtonSaveMeasurement.setEnabled(False)
