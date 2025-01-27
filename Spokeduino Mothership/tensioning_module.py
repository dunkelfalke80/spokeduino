import numpy as np
import inspect
from typing import TYPE_CHECKING, cast, Any
from PySide6.QtCore import Qt
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QTableWidget, QWidget
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
from measurement_module import MeasurementModule
from helpers import TextChecker, Generics
from ui import Ui_mainWindow
from calculation_module import TensionDeflectionFitter
from fast_visualisation_module import PyQtGraphCanvas, VisualisationModule
from sql_queries import SQLQueries

if TYPE_CHECKING:
    from mothership import Spokeduino


class TensioningModule:

    def __init__(self,
                 main_window: "Spokeduino",
                 ui: Ui_mainWindow,
                 unit_module: UnitModule,
                 tensiometer_module: TensiometerModule,
                 messagebox: Messagebox,
                 measurement_module: MeasurementModule,
                 db: DatabaseModule,
                 fitter: TensionDeflectionFitter,
                 canvas: PyQtGraphCanvas) -> None:
        self.ui: Ui_mainWindow = ui
        self.unit_module: UnitModule = unit_module
        self.main_window: Spokeduino = main_window
        self.setup_module = SetupModule
        self.messagebox: Messagebox = messagebox
        self.tensiometer_module: TensiometerModule = tensiometer_module
        self.measurement_mnodule: MeasurementModule = measurement_module
        self.db: DatabaseModule = db
        self.fitter: TensionDeflectionFitter = fitter
        self.canvas: PyQtGraphCanvas = canvas
        self.__chart = VisualisationModule(fitter=self.fitter)
        self.__tensions_left: np.ndarray
        self.__tensions_right: np.ndarray
        self.__target_left: float = 0.0
        self.__target_right: float = 0.0
        self.__fit_left: dict[Any, Any] | None = None
        self.__fit_right: dict[Any, Any] | None = None
        self.__unit: UnitEnum = UnitEnum.NEWTON
        self.ui.tableWidgetTensioningLeft.setEnabled(False)
        self.ui.tableWidgetTensioningRight.setEnabled(False)

    def setup_table(self, is_left: bool) -> None:
        """
        Set up tableWidgetTensionsLeft or tableWidgetTensionsRight
        based on spoke amount and target tension.
        Populate the table manually for QTableWidget.
        """
        self.__unit = self.unit_module.get_unit()
        # Select the appropriate UI elements
        if is_left:
            line_edit_spoke_amount: QLineEdit = self.ui.lineEditSpokeAmountLeft
            view: CustomTableWidget = self.ui.tableWidgetTensioningLeft
            other_view: CustomTableWidget = self.ui.tableWidgetTensioningRight
        else:
            line_edit_spoke_amount: QLineEdit = self.ui.lineEditSpokeAmountRight
            view: CustomTableWidget = self.ui.tableWidgetTensioningRight
            other_view: CustomTableWidget = self.ui.tableWidgetTensioningLeft

        # Get spoke amount and target tension
        try:
            spoke_amount = int(line_edit_spoke_amount.text())
        except ValueError:
            spoke_amount = 0

        if is_left:
            self.__tensions_left = np.zeros(spoke_amount)
        else:
            self.__tensions_right = np.zeros(spoke_amount)
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
        view.setEnabled(spoke_amount > 0 and other_view.rowCount() > 0)
        other_view.setEnabled(spoke_amount > 0 and other_view.rowCount() > 0)
        self.set_tension(is_left)

    def set_tension(self, is_left: bool) -> None:
        if is_left:
            try:
                self.__target_left = float(self.ui.lineEditTargetTensionLeft.text())
            except ValueError:
                self.__target_left = 0.0
        else:
            try:
                self.__target_right = float(self.ui.lineEditTargetTensionRight.text())
            except ValueError:
                self.__target_right = 0.0
        self.__chart.draw_static_elements(
            plot_widget=self.canvas.plot_widget,
            left_spokes=self.ui.tableWidgetTensioningLeft.rowCount(),
            right_spokes=self.ui.tableWidgetTensioningRight.rowCount(),
            target_tension_left=self.__target_left,
            target_tension_right=self.__target_right
        )

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
        if column == 1:
            return

        value = TextChecker.check_text(value, True)
        if value == "":
            return

        view: CustomTableWidget = (self.ui.tableWidgetTensioningLeft
                                   if is_left
                                   else self.ui.tableWidgetTensioningRight)
        header: str | None = view.get_row_header_text(row)
        if header is None:
            return

        spoke_no: int = int(header)
        value = value.replace(",", ".")
        deflection: float = float(value)

        if is_left:
            tension: float = self.calculate_tension(fit_model=self.__fit_left, deflection=deflection)
        else:
            tension: float = self.calculate_tension(fit_model=self.__fit_right, deflection=deflection)

        _, kgf, lbf = self.unit_module.convert_units(
            value=tension,
            source=UnitEnum.NEWTON)
        # Newton is the base unit for this applicaiton
        tension_converted: float = tension

        if self.__unit == UnitEnum.KGF:
            tension_converted = kgf
        elif self.__unit == UnitEnum.LBF:
            tension_converted = lbf

        value = (f"{tension_converted:.0f}"
                 if self.__unit == UnitEnum.NEWTON
                 else f"{tension_converted:.1f}")
        item = QTableWidgetItem(value)
        item.setFlags(Qt.ItemFlag.ItemIsEnabled)
        view.setItem(row, 1, item)
        if is_left:
            self.__tensions_left[spoke_no] = tension
        else:
            self.__tensions_right[spoke_no] = tension
        self.plot_spoke_tensions()

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

        fit_type, header = self.measurement_mnodule.get_fit()
        measurements: list[tuple[float, float]] = self.db.execute_select(
            query=SQLQueries.GET_MEASUREMENTS_BY_ID,
            params=(measurement_id,))

        fit_model = self.fitter.fit_data(measurements, fit_type)

        if is_left:
            self.ui.plainTextEditSelectedSpokeLeft.setPlainText(spoke_details)
            self.main_window.status_label_spoke_left.setText(f"<- {spoke_name} {self.ui.lineEditDimension.text()}")
            self.__fit_left = fit_model
        else:
            self.ui.plainTextEditSelectedSpokeRight.setPlainText(spoke_details)
            self.main_window.status_label_spoke_right.setText(f"{spoke_name} {self.ui.lineEditDimension.text()} ->")
            self.__fit_right = fit_model

    def calculate_tension(self, fit_model, deflection: float) -> float:
        """
        Given the string from a cell containing deflection (mm),
        parse and compute tension. If invalid or empty, return 0.
        Replace the formula with your own as needed.
        """
        try:
            tension = self.fitter.calculate_tension(fit_model, deflection)
            if tension is None:
                return 0.0
            return tension
        except (ValueError, TypeError):
            return 0.0

    def plot_spoke_tensions(self) -> None:
        """
        Update the polar radar chart inside verticalLayoutMeasurementRight
        using the PyQtGraph-based VisualisationModule.
        """
        left_spokes: int = self.ui.tableWidgetTensioningLeft.rowCount()
        right_spokes: int = self.ui.tableWidgetTensioningRight.rowCount()

        # Call the radar chart plotting function from the VisualisationModule
        self.__chart.plot_dynamic_tensions(
            plot_widget=self.canvas.plot_widget,
            left_spokes=left_spokes,
            right_spokes=right_spokes,
            tensions_left=self.__tensions_left,
            tensions_right=self.__tensions_right
        )
