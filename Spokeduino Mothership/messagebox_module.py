from typing import Any
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QMessageBox

class MessageboxModule:

    def __init__(self, main_window: QMainWindow) -> None:
        self.main_window = main_window

    def ok(self, text: str) -> None:
        QMessageBox.information(self.main_window, "Info", text)

    def err(self, text: str) -> None:
        QMessageBox.critical(self.main_window,
                            "Error",
                            text,
                            QMessageBox.StandardButton.Discard,
                            QMessageBox.StandardButton.Discard)
