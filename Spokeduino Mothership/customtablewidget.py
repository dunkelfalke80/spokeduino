from PySide6.QtWidgets import QTableWidget
from PySide6.QtCore import Qt

class CustomTableWidget(QTableWidget):
    def __init__(self, move_next_callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move_next_callback = move_next_callback

    def keyPressEvent(self, event) -> None:
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            # Call the move_to_next_cell method when Enter is pressed
            self.move_next_callback()
        else:
            # Call the base class's keyPressEvent for other keys
            super().keyPressEvent(event)