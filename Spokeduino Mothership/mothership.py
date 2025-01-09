import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from mothership_main_ui import Ui_mainWindow


class SpokeduinoApp(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.setup_signals_and_slots()

    def setup_signals_and_slots(self) -> None:
        self.ui.pushButtonCreateNewSpoke.clicked.connect(self.button_create_new_spoke_onclick)

    def button_create_new_spoke_onclick(self) -> None:
        print("Create New Spoke button")


def main():
    app = QApplication(sys.argv)
    window = SpokeduinoApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
