from typing import Any
from PySide6.QtCore import Qt
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QTableWidget
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtWidgets import QHeaderView
from PySide6.QtWidgets import QLineEdit
from setup_module import SetupModule
from helpers import Messagebox
from customtablewidget import CustomTableWidget
from sql_queries import SQLQueries
from unit_module import UnitEnum, UnitModule
from database_module import DatabaseModule
from unit_module import UnitModule
from tensiometer_module import TensiometerModule
from helpers import TextChecker, Generics
from ui import Ui_mainWindow

class TensioningModule:

    def __init__(self,
                 main_window: QMainWindow,
                 ui: Ui_mainWindow,
                 unit_module: UnitModule,
                 tensiometer_module: TensiometerModule,
                 messagebox: Messagebox,
                 db: DatabaseModule) -> None:
        self.ui: Ui_mainWindow = ui
        self.unit_module: UnitModule = unit_module
        self.main_window: QMainWindow = main_window
        self.setup_module = SetupModule
        self.messagebox: Messagebox = messagebox
        self.tensiometer_module: TensiometerModule = tensiometer_module
        self.db: DatabaseModule = db
        self.__tensions_left: list[tuple[float, float]] = []
        self.__tensions_right: list[tuple[float, float]] = []
        self.__measurement_left: int = -1
        self.__measurement_right: int = -1

    def setup_table(self, is_left: bool) -> None:
        """
        Set up tableWidgetTensionsLeft or tableWidgetTensionsRight
        based on spoke amount and target tension.
        Populate the table manually for QTableWidget.
        """
        # Select the appropriate UI elements
        if is_left:
            line_edit_spoke_amount: QLineEdit = self.ui.lineEditSpokeAmountLeft
            view: CustomTableWidget = self.ui.tableWidgetTensioningLeft
        else:
            line_edit_spoke_amount: QLineEdit = self.ui.lineEditSpokeAmountRight
            view: CustomTableWidget = self.ui.tableWidgetTensioningRight

        # Get spoke amount and target tension
        try:
            spoke_amount = int(line_edit_spoke_amount.text())
        except ValueError:
            spoke_amount = 0

        if is_left:
            self.__tensions_left = [(0.0, 0.0)] * spoke_amount
        else:
            self.__tensions_right = [(0.0, 0.0)] * spoke_amount
        # Define headers
        headers: list[str] = ["mm", self.unit_module.get_unit().value]

        # Clear and set up the table
        view.clear()
        view.setRowCount(spoke_amount)
        view.setColumnCount(2)
        view.setHorizontalHeaderLabels(headers)
        if self.ui.radioButtonRotationClockwise.isChecked():
            view.setVerticalHeaderLabels(
                    [f"{value}" for value in range(1, spoke_amount, 1)])
        elif self.ui.radioButtonRotationAnticlockwise.isChecked():
            view.setVerticalHeaderLabels(
                    [f"{value}" for value in range(spoke_amount, 0, -1)])

        # Populate rows
        for row in range(spoke_amount):
            # Create editable cell for "mm" column
            mm_item = QTableWidgetItem("")
            mm_item.setFlags(Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled)
            view.setItem(row, 0, mm_item)

            # Create non-editable cell for tension column
            tension_item = QTableWidgetItem("")
            tension_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            view.setItem(row, 1, tension_item)

        # Resize columns to fit within the table
        view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        view.resize_table_font()

    def start_tensioning(self) -> None:
        pass

    def next_cell_callback_left(self, no_delay: bool = False) -> None:
        self.next_cell_callback(True)

    def next_cell_callback_right(self, no_delay: bool = False) -> None:
        self.next_cell_callback(False)

    def next_cell_callback(self, is_left: bool) -> None:
        this_view: CustomTableWidget
        other_view: CustomTableWidget
        if is_left:
            this_view = self.ui.tableWidgetTensioningLeft
            other_view = self.ui.tableWidgetTensioningRight
        else:
            this_view = self.ui.tableWidgetTensioningRight
            other_view = self.ui.tableWidgetTensioningLeft

        this_row: int = this_view.currentRow()
        other_row: int = other_view.currentRow()
        this_count: int = this_view.rowCount()
        other_count: int = other_view.rowCount()

        if self.ui.radioButtonLeftRight.isChecked() \
            or self.ui.radioButtonRightLeft.isChecked():
            print(f"This row: {this_row}")
            print(f"Other row: {other_row}")
            if other_row == other_count -1:
                this_row = 0
            else:
                this_row = other_row + 1
            this_view = other_view
        elif self.ui.radioButtonSideBySide.isChecked():
            print(f"This row: {this_row}")
            print(f"Other row: {other_row}")
            if this_row == this_count - 1:
                this_view = other_view
                this_row = 0
            else:
                this_row += 1

        QTimer.singleShot(50,
            lambda: this_view.move_to_specific_cell(
                row=this_row,
                column=0))

    def previous_cell_callback_left(self) -> None:
        self.previous_cell_callback(is_left=True)

    def previous_cell_callback_right(self) -> None:
        self.previous_cell_callback(is_left=False)

    def previous_cell_callback(self, is_left: bool) -> None:
        if is_left:
            print("Previous cell left")
        else:
            print("Previous cell right")

    def on_cell_changed(
            self,
            is_left: bool,
            row: int,
            column: int) -> None:
        """
        Handle updates when a cell's text has changed.

        :param is_left: Left or right side of the wheel
        :param row: The row index of the changed cell.
        :param column: The column index of the changed cell.
        """
        # Get the new value
        view: CustomTableWidget = (self.ui.tableWidgetTensioningLeft
                                   if is_left
                                   else self.ui.tableWidgetTensioningRight)
        item: QTableWidgetItem | None = view.item(row, column)
        if item is None:
            return
        value: str = item.text()
        if value == "":
            return

        header: str | None = view.get_row_header_text(row)
        if header is None:
            return

        spoke_no: int = int(header)
        value = value.replace(",", ".")
        deflection: float = float(value)
        tension: float = 0.0
        try:
            # tension = PiecewiseQuarticFit.evaluate(formula, deflection)
            pass
        except Exception as ex:
            print(ex)
            return

        if tension == 0.0:
            return

        _, kgf, lbf = self.unit_module.convert_units(
            value=deflection,
            source=UnitEnum.NEWTON)
        # Newton is the base unit for this applicaiton
        tension_converted: float = tension
        unit: UnitEnum = self.unit_module.get_unit()
        match unit:
            case UnitEnum.KGF:
                tension_converted = kgf
            case UnitEnum.LBF:
                tension_converted = lbf

        if tension_converted == 0.0:
            return

        value = (f"{tension:.0f}"
                 if unit == UnitEnum.NEWTON
                 else f"{tension:.1f}")
        item = QTableWidgetItem(value)
        item.setFlags(Qt.ItemFlag.ItemIsEnabled)
        view.setItem(row, 1, item)

    def on_cell_changing(
            self,
            is_left: bool,
            row: int,
            column: int,
            value: str) -> None:
        """
        Handle updates when a cell's text is changed in real time.

        :param is_left: Left or right side of the wheel
        :param row: The row index.
        :param column: The column index.
        :param value: The current value.
        """
        value = TextChecker.check_text(value, True)
        if value == "":
            return
        self.on_cell_changed(is_left=is_left, row=row, column=column)

    def use_spoke(self, is_left: bool) -> None:
        """
        Write the selected spoke details to plainTextEditSelectedSpoke
        and save the formula for the spoke based on the selected or first measurement.
        """
        view: QTableWidget = self.ui.tableWidgetSpokesDatabase
        spoke_id: int = Generics.get_selected_row_id(view)
        if spoke_id < 0:
            return

        spoke_details: str = (
            f"{self.ui.comboBoxManufacturer.currentText} "
            f"{self.ui.lineEditName.text()} {self.ui.lineEditGauge.text()}G\n"
            f"{self.ui.lineEditDimension.text()}\n"
            f"{self.ui.lineEditSpokeComment.text()}"
        )

        measurement_id: int = Generics.get_selected_row_id(self.ui.tableWidgetMeasurementList)

        if is_left:
            self.ui.plainTextEditSelectedSpokeLeft.setPlainText(spoke_details)
            self.__measurement_left = measurement_id
        else:
            self.ui.plainTextEditSelectedSpokeRight.setPlainText(spoke_details)
            self.__measurement_right = measurement_id