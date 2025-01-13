from typing import Any
from PySide6.QtWidgets import QMessageBox

class MessageboxModule:

    def __init__(self, ui: Any) -> None:
        self.ui = ui

    def ok(self, text: str) -> None:
        QMessageBox.information(self.ui, "Info", text)

    def err(self, text: str) -> None:
        QMessageBox.critical(self.ui,
                            "Error",
                            text,
                            QMessageBox.StandardButton.Discard,
                            QMessageBox.StandardButton.Discard)
