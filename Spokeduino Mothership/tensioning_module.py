from typing import TYPE_CHECKING, cast
from PySide6.QtCore import Qt
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QTableWidget
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtWidgets import QHeaderView
from PySide6.QtWidgets import QLineEdit
from matplotlib.projections.polar import PolarAxes
from setup_module import SetupModule
from helpers import Messagebox
from customtablewidget import CustomTableWidget
from unit_module import UnitEnum, UnitModule
from database_module import DatabaseModule
from tensiometer_module import TensiometerModule
from helpers import TextChecker, Generics
from ui import Ui_mainWindow
from calculation_module import TensionDeflectionFitter
from visualisation_module import MatplotlibCanvas, VisualisationModule

if TYPE_CHECKING:
    from mothership import Spokeduino


class TensioningModule:

    def __init__(self,
                 main_window: "Spokeduino",
                 ui: Ui_mainWindow,
                 unit_module: UnitModule,
                 tensiometer_module: TensiometerModule,
                 messagebox: Messagebox,
                 db: DatabaseModule,
                 fitter: TensionDeflectionFitter,
                 canvas: MatplotlibCanvas) -> None:
        self.ui: Ui_mainWindow = ui
        self.unit_module: UnitModule = unit_module
        self.main_window: Spokeduino = main_window
        self.setup_module = SetupModule
        self.messagebox: Messagebox = messagebox
        self.tensiometer_module: TensiometerModule = tensiometer_module
        self.db: DatabaseModule = db
        self.fitter: TensionDeflectionFitter = fitter
        self.canvas = canvas
        self.__chart = VisualisationModule(fitter=self.fitter)
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
            if other_row == other_count -1:
                this_row = 0
            else:
                this_row = other_row + 1
            this_view = other_view
        elif self.ui.radioButtonSideBySide.isChecked():
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
        tension: float = self.calculate_tension_from_deflection(deflection)
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

        view: QTableWidget = self.ui.tableWidgetMeasurementList
        measurement_id: int = Generics.get_selected_row_id(view)
        if measurement_id == -1:
            return
        item: QTableWidgetItem | None = view.item(view.currentRow(), 0)
        if item is None:
            return

        spoke_name: str = (
            f"{self.ui.comboBoxManufacturer.currentText()} "
            f"{self.ui.lineEditName.text()}"
        )
        spoke_details: str = (
            f"{spoke_name}\n"
            f"{self.ui.lineEditSpokeComment.text()}\n"
            f"{item.text()}"
        )

        if is_left:
            self.ui.plainTextEditSelectedSpokeLeft.setPlainText(spoke_details)
            self.main_window.status_label_spoke_left.setText(f"<- {spoke_name} {self.ui.lineEditDimension.text()}")
            self.__measurement_left = measurement_id
        else:
            self.ui.plainTextEditSelectedSpokeRight.setPlainText(spoke_details)
            self.main_window.status_label_spoke_right.setText(f"{spoke_name} {self.ui.lineEditDimension.text()} ->")
            self.__measurement_right = measurement_id

    def calculate_tension_from_deflection(self, deflection: float) -> float:
        """
        Given the string from a cell containing deflection (mm),
        parse and compute tension. If invalid or empty, return 0.
        Replace the formula with your own as needed.
        """
        try:
            tension = deflection * 100.0  # Example formula
            # Return only nonnegative for safety
            return max(tension, 0.0)
        except (ValueError, TypeError):
            return 0.0

    def read_spoke_data(self, table_widget) -> list[tuple[int, float]]:
        """
        Reads the deflection from column 0 of each row, converts to tension,
        and returns a list of (spoke_index, tension).
        The row header is parsed as the spoke_index.
        """
        row_count = table_widget.rowCount()
        spoke_data = []

        for row in range(row_count):
            # Row header => spoke index
            header_item = table_widget.verticalHeaderItem(row)
            if header_item is None:
                continue  # Skip if missing
            try:
                spoke_index = int(header_item.text().strip())
            except ValueError:
                continue  # If it’s not an integer, skip

            # Deflection in column 0 => tension
            deflection_item = table_widget.item(row, 0)
            if not deflection_item:
                # No item => tension = 0
                tension = 0.0
            else:
                tension: float = self.calculate_tension_from_deflection(float(deflection_item.text().strip()))

            # Optionally: write tension back into column 1 if desired
            # tension_str = f"{tension:.2f}"
            # table_widget.setItem(row, 1, QTableWidgetItem(tension_str))

            spoke_data.append((spoke_index, tension))

        return spoke_data


    def plot_spoke_tensions(self):
        """
        Example slot: read data from tableWidgetTensioningLeft/right,
        then plot on a polar radar chart inside verticalLayoutMeasurementRight.
        """
        # 1) Gather spoke data for left side
        tensions_left = self.read_spoke_data(self.ui.tableWidgetTensioningLeft)
        left_spokes = self.ui.tableWidgetTensioningLeft.rowCount()

        # 2) Gather spoke data for right side
        tensions_right = self.read_spoke_data(self.ui.tableWidgetTensioningRight)
        right_spokes = self.ui.tableWidgetTensioningRight.rowCount()

        # If you only want one plot at a time, clear out the layout first:
        while self.ui.verticalLayoutMeasurementRight.count():
            item = self.ui.verticalLayoutMeasurementRight.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        # 4) Build a polar axes
        ax = self.canvas.figure.add_subplot(111, projection="polar")

        # 5) Plot with either the symmetric or asymmetric method
        # If the left side has the same number of spokes as the right side => symmetrical
        if left_spokes == right_spokes:
            # For demonstration, let's pass example target tensions
            # (Or None if you don't want to show target lines.)
            self.__chart.plot_spoke_tensions(
                ax=cast(PolarAxes, ax),
                spokes_per_side=left_spokes,
                tensions_left=tensions_left,
                tensions_right=tensions_right,
                target_left=110.0,
                target_right=130.0
            )
        else:
            self.__chart.plot_asymmetric_spoke_tensions(
                ax=cast(PolarAxes, ax),
                left_spokes=left_spokes,
                right_spokes=right_spokes,
                tensions_left=tensions_left,
                tensions_right=tensions_right,
                target_left=100.0,
                target_right=140.0
            )

        # 6) Redraw
        self.canvas.draw_figure()
