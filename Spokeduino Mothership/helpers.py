from typing import Any
from PySide6.QtCore import Qt
from PySide6.QtCore import QLocale
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QTableWidget
from PySide6.QtWidgets import QTableWidgetItem


class Messagebox:

    def __init__(self, main_window: QMainWindow, ui: Any) -> None:
        self.main_window: QMainWindow = main_window
        self.ui: Any = ui

    def info(self, text: str) -> None:
        QMessageBox.information(self.main_window, "Info", text)

    def err(self, text: str) -> None:
        QMessageBox.critical(self.main_window,
                             "Error",
                             text,
                             QMessageBox.StandardButton.Discard,
                             QMessageBox.StandardButton.Discard)


class TextChecker:

    @staticmethod
    def check_text(text: str, full_string: bool = False) -> str:
        """
        Replaces dot and comma with the locale decimal point.
        Allows only digits and one decimal point.
        Converts fractional inputs like '.2' to '0.2'.

        :param text: The input text to validate and format.
        :return: The formatted text or an empty string if invalid.
        """
        decimal_point: str = QLocale().decimalPoint()
        decimal_point_encountered: bool = False
        fixed_input: str = ""

        # Replace dot and comma with the locale decimal point
        # and only allow digits and decimal point
        for char in text:
            if char in [",", "."] and not decimal_point_encountered:
                fixed_input += decimal_point
                decimal_point_encountered = True
            elif char.isdigit():
                fixed_input += char

        # Only invalid characters in the text
        if fixed_input == "":
            return ""

        # for entering values that only have a fraction
        if fixed_input[0] == QLocale().decimalPoint():
            # Not a fraction, just text
            if full_string and len(fixed_input) == 1:
                return ""
            fixed_input = "0" + fixed_input

        if full_string and fixed_input.endswith(QLocale().decimalPoint()):
            fixed_input = fixed_input[:-1]
        return fixed_input


class Generics:

    @staticmethod
    def get_selected_row_id(view: QTableWidget) -> int:
        """
        Returns the id of the currently selected row.
        If no row is selected, returns -1
        """
        # No data in the table
        if view.rowCount() < 1:
            return -1

        # Determine the row
        selected_row: int = view.currentRow()
        if view.rowCount() > 1 and selected_row < 0:
            return -1

        # Default to the only row if none are explicitly selected
        if selected_row < 0:
            selected_row = 0

        # Get the ID of the selected row
        id_item: QTableWidgetItem | None = view.item(selected_row, 0)
        if id_item is None:
            return -1

        measurement_id = id_item.data(Qt.ItemDataRole.UserRole)
        if measurement_id is None:
            return -1
        return int(measurement_id)
