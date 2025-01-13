import logging
from PySide6.QtCore import Qt
from PySide6.QtGui import QClipboard
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QTableWidget
from PySide6.QtWidgets import QTableWidgetItem

class CustomTableWidget(QTableWidget):
    def __init__(self, move_next_callback, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.move_next_callback = move_next_callback

    def keyPressEvent(self, event) -> None:
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            super().keyPressEvent(event)
            self.move_next_callback()
        # Check for Ctrl+V or Shift+Insert
        if (event.key() == Qt.Key.Key_V and event.modifiers() & Qt.KeyboardModifier.ControlModifier) or \
           (event.key() == Qt.Key.Key_Insert and event.modifiers() & Qt.KeyboardModifier.ShiftModifier):
            logging.error("keypress")
            self.paste_row()
        else:
            super().keyPressEvent(event)

    def paste_row(self) -> None:
        """
        Paste data from the clipboard into the currently selected row.
        """
        selected_row: int = self.currentRow()
        if selected_row == -1:
            return

        clipboard: QClipboard = QApplication.clipboard()
        clipboard_data: str = clipboard.text()
        cells: list[str] = clipboard_data.strip().split("\n")

        # Ensure the number of cells matches the table's row count
        if len(cells) != self.rowCount():
            return

        # Populate the selected row with clipboard data
        for col, value in enumerate(cells):
            item = QTableWidgetItem(value)
            item.setFlags(Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled)
            self.setItem(selected_row, col, item)