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
            selected_row = self.currentRow()
            selected_column = self.currentColumn()

            if selected_row == -1 or selected_column == -1:
                return  # No valid selection

            clipboard: QClipboard = QApplication.clipboard()
            clipboard_data: str = clipboard.text()

            # Split clipboard data into individual rows
            rows: list[str] = clipboard_data.strip().split("\n")

            for r_offset, cell_data in enumerate(rows):
                target_row = selected_row + r_offset

                # Check bounds to avoid pasting outside the table
                if target_row < self.rowCount():
                    item = QTableWidgetItem(cell_data.strip())
                    item.setFlags(Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled)
                    self.setItem(target_row, selected_column, item)
