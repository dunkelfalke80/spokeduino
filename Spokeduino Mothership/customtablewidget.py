from typing import override, cast
from PySide6.QtCore import Qt
from PySide6.QtCore import QObject
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import QLocale
from PySide6.QtCore import QTimer
from PySide6.QtCore import QEvent
from PySide6.QtCore import QSize
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import QPersistentModelIndex
from PySide6.QtGui import QClipboard
from PySide6.QtGui import QValidator
from PySide6.QtGui import QDoubleValidator
from PySide6.QtGui import QFont
from PySide6.QtGui import QShortcut
from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtWidgets import QTableWidget
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtWidgets import QStyledItemDelegate
from PySide6.QtWidgets import QStyleOptionViewItem
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QWidget


class CustomTableWidget(QTableWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Configure table behavior
        self.__select_rows: QAbstractItemView.SelectionBehavior = \
            QAbstractItemView.SelectionBehavior.SelectRows
        self.__select_single: QAbstractItemView.SelectionMode = \
            QAbstractItemView.SelectionMode.SingleSelection
        self.setSelectionBehavior(self.__select_rows)
        self.setSelectionMode(self.__select_single)
        self.setItemDelegate(CustomTableWidgetItemDelegate(self))

    @override
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
            target_row: int = selected_row
            for r_offset, cell_data in enumerate(rows):
                target_row = selected_row + r_offset

                # Check bounds to avoid pasting outside the table
                if target_row < self.rowCount():
                    item = QTableWidgetItem(cell_data.strip())
                    item.setFlags(Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled)
                    self.setItem(target_row, selected_column, item)
            self.move_to_specific_cell(target_row, selected_column)
            self.move_to_next_cell()

    def refocus(self, zero: bool) -> None:
        item: QTableWidgetItem | None = (self.item(0, 0)
                                         if zero
                                         else self.currentItem())
        if item is None:
            return
        item = cast(QTableWidgetItem, item)
        item.setSelected(True)

    def move_to_specific_cell(self, row: int, column: int) -> None:
        index: QModelIndex = self.model().index(row, column)
        if not index.isValid():
            return
        # Ensures the first cell becomes active
        if row == 0 and column == 0:
            self.refocus(True)
        self.setCurrentIndex(index)
        self.edit(index)
        print(f"moving to {column}:{row}")

    def move_to_next_cell(self) -> None:
        """
        Move to the next cell in the table and activate editing.
        """
        row: int = self.currentRow()
        column: int = self.currentColumn()

        if row < self.rowCount() - 1:
            row += 1
        elif column < self.columnCount() - 1:
            row = 0
            column += 1
        else:
            return  # Already at the last cell

        # Delay to ensure Qt's focus/selection state is updated
        QTimer.singleShot(50, lambda: self.move_to_specific_cell(row, column))

    def move_to_previous_cell(self) -> None:
        """
        Move to the previous cell in the table and activate editing.
        """
        row: int = self.currentRow()
        column: int = self.currentColumn()

        if row > 0:
            row -= 1
        elif column > 0:
            column -= 1
        else:
            return  # Already at the first cell

        # Delay to ensure Qt's focus/selection state is updated
        QTimer.singleShot(50, lambda: self.move_to_specific_cell(row, column))

    def resize_table_font(self) -> None:
            """
            Resize the table font, row heights, and column widths so it fits within the parent layout.
            """
            row_count = self.rowCount()
            if row_count == 0:
                return  # No rows to resize

            # Get the size of the parent widget
            parent_widget: QWidget | None = self.parentWidget()
            if parent_widget is None:
                return  # Cannot determine parent size
            parent_widget = cast(QWidget, parent_widget)

            layout_size: QSize = parent_widget.size()
            layout_height: int = layout_size.height()
            layout_width: int = layout_size.width()

            # Estimate row height and font size
            row_height: int = layout_height // row_count
            font_size = row_height // 3  # Adjust font size relative to row height

            # Ensure minimum font size
            font_size: int = max(font_size, 8)

            # Set font for the table
            font: QFont = self.font()
            font.setPointSize(font_size)
            self.setFont(font)

            # Adjust row height and column widths
            self.verticalHeader().setDefaultSectionSize(row_height)
            self.horizontalHeader().setDefaultSectionSize(layout_width // self.columnCount())
            self.resizeRowsToContents()


class CustomDoubleValidator(QDoubleValidator):
    """
    Custom validator to allow both dot and comma as decimal separators.
    """
    @override
    def validate(self, arg__1, arg__2):
        # Allow empty input (Intermediate state for typing)
        if not arg__1:
            return QValidator.State.Intermediate, arg__1, arg__2

        decimal_point: str = QLocale().decimalPoint()
        fixed_input: str = ""
        for char in arg__1:
            fixed_input += (char
                            if char.isdigit()
                            or char == decimal_point
                            else decimal_point)

        return super(CustomDoubleValidator, self).validate(fixed_input, arg__2)


class CustomTableWidgetItemDelegate(QStyledItemDelegate):
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
        editor.installEventFilter(self)
        return editor

    def _find_table_widget(self, widget: QObject) -> CustomTableWidget | None:
        """
        Traverse the widget hierarchy to find the parent table widget.
        """
        while widget is not None:
            # Check if the parent is the table
            if isinstance(widget, CustomTableWidget):
                return cast(CustomTableWidget, widget)
            # Move up the widget hierarchy
            widget = widget.parent()
        return None

    @override
    def eventFilter(self, object: QObject, event: QEvent) -> bool:
        if event == QKeySequence.StandardKey.Paste:
            table_widget: CustomTableWidget | None = \
                self._find_table_widget(object)
            if table_widget is not None:
                table_widget.paste_row()
                return True
        return super().eventFilter(object, event)
