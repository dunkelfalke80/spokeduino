from PySide6.QtCore import Qt
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import QLocale
from PySide6.QtGui import QClipboard
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QTableWidget
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import QPersistentModelIndex
from PySide6.QtGui import QValidator
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import QStyledItemDelegate
from PySide6.QtWidgets import QStyleOptionViewItem
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QWidget


class CustomTableWidget(QTableWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setItemDelegate(MeasurementItemDelegate(self))

    def keyPressEvent(self, event) -> None:
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            super().keyPressEvent(event)
            self.move_to_next_cell()
        # Check for Ctrl+V or Shift+Insert
        elif (event.key() == Qt.Key.Key_V and event.modifiers() & Qt.KeyboardModifier.ControlModifier) or \
           (event.key() == Qt.Key.Key_Insert and event.modifiers() & Qt.KeyboardModifier.ShiftModifier):
            self.paste_row()
        else:
            super().keyPressEvent(event)

    def paste_row(self) -> None:
            """
            Paste data from the clipboard into the currently selected column,
            starting at the selected row. Supports single-column clipboard data only.
            """
            selected_row: int = self.currentRow()
            selected_column: int = self.currentColumn()

            if selected_row == -1 or selected_column == -1:
                return  # No valid selection

            clipboard: QClipboard = QApplication.clipboard()
            clipboard_data: str = clipboard.text()

            # Split clipboard data into individual rows
            rows: list[str] = clipboard_data.strip().split("\n")

            for r_offset, cell_data in enumerate(rows):
                target_row: int = selected_row + r_offset

                # Check bounds to avoid pasting outside the table
                if target_row < self.rowCount():
                    item = QTableWidgetItem(cell_data.strip())
                    item.setFlags(Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled)
                    self.setItem(target_row, selected_column, item)

    def activate_cell_editing(self, row, column) -> None:
        """
        Programmatically activate editing for a specific cell.
        :param table_widget: The QTableWidget or QTableView.
        :param row: The row index of the cell to activate.
        :param column: The column index of the cell to activate.
        """
        index: QModelIndex = self.model().index(row, column)
        if index.isValid():
            self.edit(index)

    def move_to_next_cell(self):
        """
        Move to the next cell in the table and activate editing.
        """
        current_row: int = self.currentRow()
        current_column: int = self.currentColumn()

        if current_column < self.columnCount() - 1:
            next_row, next_column = current_row, current_column + 1
        elif current_row < self.rowCount() - 1:
            next_row, next_column = current_row + 1, 0
        else:
            return  # Already at the last cell

        self.setCurrentCell(next_row, next_column)
        self.activate_cell_editing(next_row, next_column)

    def move_to_previous_cell(self) -> None:
        """
        Move to the previous cell in the table and activate editing.
        """
        current_row: int = self.currentRow()
        current_column: int = self.currentColumn()

        if current_column > 0:
            prev_row, prev_column = current_row, current_column - 1
        elif current_row > 0:
            prev_row, prev_column = current_row - 1, self.columnCount() - 1
        else:
            return  # Already at the first cell

        self.setCurrentCell(prev_row, prev_column)
        self.activate_cell_editing(prev_row, prev_column)


class CustomDoubleValidator(QDoubleValidator):
    """
    Custom validator to allow both dot and comma as decimal separators.
    """

    def validate(self, arg__1, arg__2):
        # Allow empty input (Intermediate state for typing)
        if not arg__1:
            return QValidator.State.Intermediate, arg__1, arg__2

        decimal_point: str = QLocale().decimalPoint()
        for char in arg__1:
            if not (char.isdigit() or char == decimal_point):
                return QValidator.State.Invalid, arg__1, arg__2

        return super(CustomDoubleValidator, self).validate(arg__1, arg__2)

    def fixup(self, input: str) -> str:
        """
        Replace invalid characters with the locale's decimal point.
        """
        decimal_point = QLocale().decimalPoint()
        return ''.join(char if char.isdigit() or char == decimal_point else decimal_point for char in input)


class MeasurementItemDelegate(QStyledItemDelegate):
    """
    Custom delegate to allow both dot and comma
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