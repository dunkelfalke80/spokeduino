from PySide6.QtCore import Qt
from PySide6.QtCore import QAbstractTableModel
from PySide6.QtCore import QLocale
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QMessageBox

class SpokeTableModel(QAbstractTableModel):
    """
    Table model for displaying spokes data in a QTableView.
    """
    def __init__(
            self,
            data: list[tuple[int, list[str]]],
            headers: list[str]) -> None:
        """
        :param data: List of tuples, each containing:
                     - A unique ID (int)
                     - A list of strings representing row data
        :param headers: Column headers
        """
        super().__init__()
        self._data: list[tuple[int, list[str]]] = data
        self._headers: list[str] = headers

    def rowCount(self, parent=None) -> int:
        return len(self._data)

    def columnCount(self, parent=None) -> int:
        return len(self._headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole) -> str | None:
        if role == Qt.ItemDataRole.DisplayRole:
            row_data: list[str] = self._data[index.row()][1]  # Access row data
            return row_data[index.column()]
        return None

    def headerData(self, section: int, orientation: Qt.Orientation,
                   role: int = Qt.ItemDataRole.DisplayRole) -> str | None:
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers[section]
        return None

    def get_id(self, row: int) -> int | None:
        """
        Get the unique ID for a given row.
        """
        if 0 <= row < len(self._data):
            return self._data[row][0]  # Return ID part of the tuple
        return None


class Messagebox:

    def __init__(self, main_window: QMainWindow) -> None:
        self.main_window = main_window

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