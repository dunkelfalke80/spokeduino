from typing import override, cast, Callable, Optional
from PySide6.QtCore import Qt
from PySide6.QtCore import QAbstractItemModel
from PySide6.QtCore import QObject
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import QLocale
from PySide6.QtCore import QTimer
from PySide6.QtCore import QEvent
from PySide6.QtCore import QSize
from PySide6.QtCore import Signal
from PySide6.QtCore import QPersistentModelIndex
from PySide6.QtGui import QClipboard
from PySide6.QtGui import QValidator
from PySide6.QtGui import QDoubleValidator
from PySide6.QtGui import QFont
from PySide6.QtGui import QKeyEvent
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
    """
    A custom table widget designed to handle specific features such as custom
    navigation callbacks, cell editing, and clipboard paste operations.
    """
    onCellDataChanging = Signal(int, int, str)  # row, column, value

    def __init__(self,
                 move_to_next_cell_callback:
                    Optional[Callable[[bool], None]] = None,
                 move_to_previous_cell_callback:
                    Optional[Callable[[], None]] = None,
                 *args,
                 **kwargs) -> None:
        """
        Initialize the CustomTableWidget.

        :param move_to_next_cell_callback: Optional callback for navigating
                                           to the next cell.
                                           Defaults to the internal
                                           __move_to_next_cell_default.
        :param move_to_previous_cell_callback: Optional callback for navigating
                                               to the previous cell.
                                               Defaults to the internal
                                               __move_to_previous_cell_default.
        """
        ...
        super().__init__(*args, **kwargs)
        # Configure table behavior
        self.__select_rows: QAbstractItemView.SelectionBehavior = \
            QAbstractItemView.SelectionBehavior.SelectRows
        self.__select_single: QAbstractItemView.SelectionMode = \
            QAbstractItemView.SelectionMode.SingleSelection
        self.setSelectionBehavior(self.__select_rows)
        self.setSelectionMode(self.__select_single)
        self.setItemDelegate(CustomTableWidgetItemDelegate(self))

        if move_to_next_cell_callback is None:
            self.move_to_next_cell: Callable[[bool], None] = \
                self.__move_to_next_cell_default
        else:
            self.move_to_next_cell = move_to_next_cell_callback

        if move_to_previous_cell_callback is None:
            self.move_to_previous_cell: Callable[[], None] = \
                self.__move_to_previous_cell_default
        else:
            self.move_to_previous_cell = move_to_previous_cell_callback

    def emit_on_cell_data_changing(self, value: str) -> None:
        """
        Emit the onCellDataChanged signal on editing a cell.
        """
        self.onCellDataChanging.emit(self.currentRow(), self.currentColumn(), value)

    @override
    def keyPressEvent(self, event) -> None:
        """
        Handle key press events.

        Supports Enter/Return for moving to the next cell and Ctrl+V/Shift+Insert
        for pasting clipboard data.

        :param event: The key press event to handle.
        """
        if event.matches(QKeySequence.StandardKey.Paste):
            self.paste_row()
        elif event.matches(QKeySequence.StandardKey.InsertParagraphSeparator):
            super().keyPressEvent(event)
            self.move_to_next_cell(False)
        else:
            super().keyPressEvent(event)

    def get_row_header_text(self, row: Optional[int]) -> str | None:
        """
        Retrieve the header text for a specific row.

        :param row: The row index.
        :return: The header text or None if no header is set.
        """
        if row is None:
            row = self.currentRow()
        header_item: QTableWidgetItem = self.verticalHeaderItem(row)
        return header_item.text() if header_item else None

    def paste_row(self) -> None:
            """
            Paste data from the clipboard into the currently selected column,
            starting at the selected cell. If the clipboard data is multi-line,
            automatically moves to next cell for each line, wrapping around columns
            if required.
            """
            clipboard: QClipboard = QApplication.clipboard()
            clipboard_data: str = clipboard.text()

            # Split clipboard data into individual rows
            rows: list[str] = clipboard_data.strip().split("\n")
            for entry in rows:
                text: str= CustomDoubleValidator(None).check_text(entry, True)
                if text in ["", ","]:
                    continue
                self.currentItem().setText(entry)
                self.move_to_next_cell(True)

    def refocus(self, zero: bool) -> None:
        """
        Refocus the table, either on the first cell or the currently active cell.

        :param zero: If True, refocus on the first cell (0, 0).
                     Otherwise, refocus on the currently active cell.
        """
        item: QTableWidgetItem | None = (self.item(0, 0)
                                         if zero
                                         else self.currentItem())
        if item is None:
            return
        item = cast(QTableWidgetItem, item)
        item.setSelected(True)

    def move_to_specific_cell(self, row: int, column: int) -> None:
        """
        Move focus to a specific cell and activate editing.

        :param row: The row index of the target cell.
        :param column: The column index of the target cell.
        """
        index: QModelIndex = self.model().index(row, column)
        if not index.isValid():
            return
        # Ensures the first cell becomes active
        if row == 0 and column == 0:
            self.refocus(True)
        self.setCurrentIndex(index)
        self.edit(index)

    def __move_to_next_cell_default(self, no_delay: bool) -> None:
        """
        Default implementation for moving to the next cell in the table.
        Moves to the cell below if possible, otherwise to the first cell
        of the next column if possible.

        :param no_delay: If True, immediately move to the next cell.
                        Otherwise, introduce a slight delay.
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
        if no_delay:
            self.move_to_specific_cell(row, column)
        else:
            QTimer.singleShot(50, lambda: self.move_to_specific_cell(row, column))

    def __move_to_previous_cell_default(self) -> None:
        """
        Default implementation for moving to the previous cell in the table.
        Moves to the cell above if possible, otherwise to the last cell
        of the previous column if possible.
        """
        row: int = self.currentRow()
        column: int = self.currentColumn()

        if row > 0:
            row -= 1
        elif column > 0:
            column -= 1
            row = self.rowCount() - 1
        else:
            return  # Already at the first cell

        # Delay to ensure Qt's focus/selection state is updated
        QTimer.singleShot(
            50,
            lambda: self.move_to_specific_cell(row, column))

    def resize_table_font(self) -> None:
        """
        Resize the table's font, row heights, and column widths
        to better fit within the parent layout.
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

        # Ensure maximum font size
        font_size: int = min(font_size, 16)

        # Set font for the table
        font: QFont = self.font()
        font.setPointSize(font_size)
        self.setFont(font)

        # Adjust row height and column widths
        self.verticalHeader().setDefaultSectionSize(row_height)
        self.horizontalHeader().setDefaultSectionSize(
            layout_width // self.columnCount())
        self.resizeRowsToContents()


class CustomDoubleValidator(QDoubleValidator):
    """
    A custom double validator that allows both dot and comma
    as decimal separators, allows fractional inputs and
    and ensures these are formatted correctly based on the locale.
    """
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)
        self.__parent_table: CustomTableWidget = cast(CustomTableWidget, parent)

    @override
    def validate(self, arg__1, arg__2):
        """
        Validate the input dynamically as the user types.

        :param arg__1: The input string to validate.
        :param arg__2: The current cursor position (not used).
        :return: A tuple containing the validation state,
                 the validated string, and the cursor position.
        """
        if not arg__1:
            # Allow empty input (Intermediate state for typing)
            self.__parent_table.emit_on_cell_data_changing("")
            return QValidator.State.Intermediate, arg__1, arg__2

        res: str = self.check_text(arg__1)
        if res == "":
            # check_text returns empty string if invalid
            self.__parent_table.emit_on_cell_data_changing("")
            return QValidator.State.Invalid, "", 0
        self.__parent_table.emit_on_cell_data_changing(res)
        return QValidator.State.Acceptable, res, len(res)

    def check_text(self, text: str, full_string: bool = False) -> str:
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

        return fixed_input


class CustomTableWidgetItemDelegate(QStyledItemDelegate):
    """
    A custom delegate for table widget items, enabling custom validation
    and handling of cell editing.
    """
    def __init__(self, parent: QObject) -> None:
        super().__init__(parent)
        self.__parent_table: CustomTableWidget = cast(CustomTableWidget, parent)

    def createEditor(self,
                     parent: QWidget,
                     option: QStyleOptionViewItem,
                     index: QModelIndex | QPersistentModelIndex) -> QLineEdit:
        """
        Create an editor widget for editing table cells.

        :param parent: The parent widget for the editor.
        :param option: The style options for the editor.
        :param index: The index of the cell being edited.
        :return: The editor widget.
        """
        editor = QLineEdit(parent)
        validator = CustomDoubleValidator(self.__parent_table)
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        editor.setValidator(validator)
        editor.installEventFilter(self)
        return editor

    @override
    def eventFilter(self, object: QObject, event: QEvent) -> bool:
        """
        Intercept paste-related key events and delegate them
        to the parent table widget.

        :param object: The widget receiving the event.
        :param event: The event to filter.
        :return: True if the event is handled,
                 otherwise passes it to the default implementation.
        """
        if event.type() == QEvent.Type.KeyPress:
            if cast(QKeyEvent, event).matches(QKeySequence.StandardKey.Paste):
                # table_widget: CustomTableWidget | None = \
                #     self.__find_table_widget(object)
                # if table_widget is not None:
                #    table_widget.paste_row()
                self.__parent_table.paste_row()
                return True
        return super().eventFilter(object, event)

    @override
    def setModelData(self,
                    editor: QWidget,
                    model: QAbstractItemModel,
                    index: QModelIndex | QPersistentModelIndex) -> None:
        """
        Finalize editing by setting the data in the model.
        Removes trailing decimal separators before saving.

        :param editor: The editor widget.
        :param model: The model to update.
        :param index: The index of the cell being edited.
        """
        if isinstance(editor, QLineEdit):
            text: str = editor.text()
            if text.endswith(QLocale().decimalPoint()):
                text = text[:-1]
            # Final check for a valid entry
            validated_text: str = CustomDoubleValidator(None).check_text(
                text=text,
                full_string=True)
            if validated_text == "":
                return

            model.setData(index, text)
        else:
            super().setModelData(editor, model, index)
