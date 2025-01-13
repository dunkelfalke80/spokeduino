from typing import cast
from PySide6.QtCore import Qt
from PySide6.QtCore import QLocale
from PySide6.QtCore import QAbstractTableModel
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import QPersistentModelIndex
from PySide6.QtGui import QValidator
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import QStyledItemDelegate
from PySide6.QtWidgets import QStyleOptionViewItem
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QWidget


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


class CustomDoubleValidator(QDoubleValidator):
    """
    Custom validator to allow both dot and comma as decimal separators.
    """

    def validate(self, arg__1, arg__2):
        # Allow empty input (Intermediate state for typing)
        if not arg__1:
            return QValidator.State.Intermediate, arg__1, arg__2

        decimal_point: str = QLocale().decimalPoint()
        fixed_input: str = ""
        for char in arg__1:
            if char.isdigit() or char == decimal_point:
                fixed_input += char
            else:
                fixed_input += decimal_point

        return super(CustomDoubleValidator, self).validate(fixed_input, arg__2)


class MeasurementItemDelegate(QStyledItemDelegate):
    """
    Custom delegate for tableWidgetMeasurements to allow both dot and comma
    as decimal separators.
    """
    def createEditor(self,
                     parent: QWidget,
                     option: QStyleOptionViewItem,
                     index: QModelIndex | QPersistentModelIndex) -> QLineEdit:
        editor = QLineEdit(parent)
        validator = CustomDoubleValidator()
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        editor.setValidator(validator)
        return editor
