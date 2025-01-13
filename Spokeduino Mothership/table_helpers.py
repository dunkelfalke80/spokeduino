from PySide6.QtCore import Qt
from PySide6.QtCore import QAbstractTableModel
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import QStyledItemDelegate
from PySide6.QtWidgets import QLineEdit


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
            row_data = self._data[index.row()][1]  # Access row data
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


class FloatValidatorDelegate(QStyledItemDelegate):
    """
    Delegate to enforce floating-point input validation in CustomTableWidget cells.
    """

    def createEditor(self, parent, option, index) -> QLineEdit:
        editor = QLineEdit(parent)
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        validator.setDecimals(2)
        editor.setValidator(validator)
        return editor
