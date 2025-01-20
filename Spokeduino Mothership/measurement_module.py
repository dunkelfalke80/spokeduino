from typing import Any
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QTableWidget
from PySide6.QtWidgets import QTableWidgetItem
from setup_module import SetupModule
from helpers import Messagebox
from customtablewidget import CustomTableWidget

class MeasurementModule:

    def __init__(self,
                 main_window: QMainWindow,
                 ui: Any,
                 messagebox: Messagebox
                 ) -> None:
        self.ui = ui
        self.main_window: QMainWindow = main_window
        self.setup_module = SetupModule
        self.messagebox: Messagebox = messagebox

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

    def get_selected_measurement_id(self) -> int | None:
        # No measurements in the table
        view: QTableWidget = self.ui.tableWidgetMeasurementList
        if view.rowCount() < 1:
            self.messagebox.info("No measurements to delete.")
            return None

        # Determine the row to delete
        selected_row: int = view.currentRow()
        if view.rowCount() > 1 and selected_row < 0:
            self.messagebox.err("No measurement row selected.")
            return  None

        # Default to the only row if none are explicitly selected
        if selected_row < 0:
            selected_row = 0

        # Get the ID of the measurement to delete
        id_item: QTableWidgetItem | None = view.item(selected_row, 0)
        if id_item is None:
            self.messagebox.err("Unable to retrieve measurement ID.")
            return  None

        measurement_id = id_item.data(Qt.ItemDataRole.UserRole)
        if measurement_id is None:
            self.messagebox.err("Invalid measurement ID.")
            return  None
        return int(measurement_id)