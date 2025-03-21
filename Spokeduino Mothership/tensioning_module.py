import numpy as np
from typing import TYPE_CHECKING, Any
from PySide6.QtCore import Qt
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QTableWidget
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtWidgets import QHeaderView
from PySide6.QtWidgets import QLineEdit
from setup_module import SetupModule
from helpers import Messagebox
from customtablewidget import CustomTableWidget, NumericTableWidgetItem
from unit_module import UnitEnum, UnitModule
from database_module import DatabaseModule
from tensiometer_module import TensiometerModule
from measurement_module import MeasurementModule
from helpers import TextChecker, Generics
from ui import Ui_mainWindow
from calculation_module import TensionDeflectionFitter
from visualisation_module import PyQtGraphCanvas, VisualisationModule
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
                 chart: VisualisationModule,
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
        self.chart: VisualisationModule = chart
        self.canvas: PyQtGraphCanvas = canvas
        self.__spoke_amount_left: int = 0
        self.__spoke_amount_right: int = 0
        self.__tensions_left: np.ndarray
        self.__tensions_right: np.ndarray
        self.__target_left: float = 0.0
        self.__target_right: float = 0.0
        self.__fit_left: dict[Any, Any] | None = None
        self.__fit_right: dict[Any, Any] | None = None
        self.__unit: UnitEnum = UnitEnum.NEWTON
        self.ui.tableWidgetTensioningLeft.setEnabled(False)
        self.ui.tableWidgetTensioningRight.setEnabled(False)
        self.__cell_changed_signal_connected = False
        self.__clockwise: bool = True
        self.__left_right: bool = False
        self.__is_left: bool = False

    def setup_table(self, is_left: bool) -> None:
        """
        Set up tableWidgetTensionsLeft or tableWidgetTensionsRight
        based on spoke amount and target tension.
        Populate the table manually for QTableWidget.
        """
        self.__unit = self.unit_module.get_unit()
        # Select the appropriate UI elements
        if is_left:
            line_edit_spoke_amount: QLineEdit = \
                self.ui.lineEditSpokeAmountLeft
            view: CustomTableWidget = self.ui.tableWidgetTensioningLeft
        else:
            line_edit_spoke_amount = self.ui.lineEditSpokeAmountRight
            view = self.ui.tableWidgetTensioningRight

        # Get spoke amount and target tension
        try:
            spoke_amount = int(line_edit_spoke_amount.text())
        except ValueError:
            spoke_amount = 0

        if is_left:
            self.__tensions_left = np.zeros(spoke_amount)
            self.__spoke_amount_left = spoke_amount
        else:
            self.__tensions_right = np.zeros(spoke_amount)
            self.__spoke_amount_right = spoke_amount
        # Define headers
        headers: list[str] = ["mm", self.unit_module.get_unit().value]

        # Clear and set up the table
        view.clear()
        view.setRowCount(spoke_amount)
        view.setColumnCount(2)
        view.setHorizontalHeaderLabels(headers)
        self.__clockwise = self.ui.radioButtonRotationClockwise.isChecked()
        if self.__clockwise:
            view.setVerticalHeaderLabels(
                    [f"{value}" for value in range(1, spoke_amount, 1)])
        else:
            view.setVerticalHeaderLabels(
                    [f"{value}" for value in range(spoke_amount, 0, -1)])

        # Populate rows
        for row in range(spoke_amount):
            # Create editable cell for "mm" column
            mm_item = NumericTableWidgetItem("")
            mm_item.setFlags(
                Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled)
            view.setItem(row, 0, mm_item)

            # Create non-editable cell for tension column
            tension_item = NumericTableWidgetItem("")
            tension_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            view.setItem(row, 1, tension_item)

        # Resize columns to fit within the table
        view.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)
        view.resize_table_font()
        view_enabled: bool = (
            self.__spoke_amount_left > 0 and
            self.__spoke_amount_right > 0)
        self.set_tension(is_left)

        self.chart.init_radar_plot(
            plot_widget=self.canvas.plot_widget, clockwise=True)
        if view_enabled:
            # Draw the empty radar plot
            self.chart.draw_radar_plot(
                plot_widget=self.canvas.plot_widget,
                left_spokes=self.__spoke_amount_left,
                right_spokes=self.__spoke_amount_left,
                target_tension_left=self.__target_left,
                target_tension_right=self.__target_right
            )
            self.plot_spoke_tensions()
            self.__left_right = (
                self.ui.radioButtonLeftRight.isChecked() or
                self.ui.radioButtonRightLeft.isChecked())

            # Connect the signal for realtime tension and chart update
            if not self.__cell_changed_signal_connected:
                self.__cell_changed_signal_connected = True
                self.ui.tableWidgetTensioningLeft.onCellChanged.connect(
                    lambda row, column, value: self.on_cell_changing(
                        is_left=True, row=row, column=column, value=value))
                self.ui.tableWidgetTensioningRight.onCellChanged.connect(
                    lambda row, column, value: self.on_cell_changing(
                        is_left=False, row=row, column=column, value=value))
        else:
            if self.__cell_changed_signal_connected:
                self.__cell_changed_signal_connected = False
                self.ui.tableWidgetTensioningLeft.onCellChanged.disconnect(
                    lambda row, column, value: self.on_cell_changing(
                        is_left=True, row=row, column=column, value=value))
                self.ui.tableWidgetTensioningRight.onCellChanged.disconnect(
                    lambda row, column, value: self.on_cell_changing(
                        is_left=False, row=row, column=column, value=value))

    def set_tension(self, is_left: bool) -> None:
        line_edit: QLineEdit
        if is_left:
            line_edit = self.ui.lineEditTargetTensionLeft
        else:
            line_edit = self.ui.lineEditTargetTensionRight

        try:
            target: float = float(line_edit.text())
        except ValueError:
            target = 0.0

        newton, _, _ = self.unit_module.convert_units(
            value=target,
            source=self.__unit)

        if is_left:
            self.__target_left = newton
        else:
            self.__target_right = newton

    def start_tensioning(self) -> None:
        if self.ui.tableWidgetTensioningLeft.isEnabled() and \
         self.ui.tableWidgetTensioningLeft.isEnabled():
            self.ui.pushButtonStartTensioning.setText("Start")
            self.ui.tableWidgetTensioningLeft.setEnabled(False)
            self.ui.tableWidgetTensioningRight.setEnabled(False)
            return

        self.ui.pushButtonStartTensioning.setText("Stop")
        self.ui.tableWidgetTensioningLeft.setEnabled(True)
        self.ui.tableWidgetTensioningRight.setEnabled(True)

        if self.ui.radioButtonLeftRight.isChecked():
            self.__is_left = True
            QTimer.singleShot(
                50,
                lambda: self.ui.tableWidgetTensioningLeft.move_to_cell(
                    row=0,
                    column=0))
        # Starting on the left
        elif self.ui.radioButtonRightLeft.isChecked():
            self.__is_left = False
            QTimer.singleShot(
                50,
                lambda: self.ui.tableWidgetTensioningRight.move_to_cell(
                    row=0,
                    column=0))
        else:  # Starting and staying on the right until the side is finished
            self.__is_left = False
            QTimer.singleShot(
                50,
                lambda: self.ui.tableWidgetTensioningRight.move_to_cell(
                    row=0,
                    column=0))

    def next_cell(self, no_delay: bool) -> None:
        this_view: CustomTableWidget
        other_view: CustomTableWidget
        if self.__is_left:
            this_view = self.ui.tableWidgetTensioningLeft
            other_view = self.ui.tableWidgetTensioningRight
        else:
            this_view = self.ui.tableWidgetTensioningRight
            other_view = self.ui.tableWidgetTensioningLeft

        this_row: int = this_view.currentRow()
        other_row: int = other_view.currentRow()
        this_count: int = this_view.rowCount()
        other_count: int = other_view.rowCount()

        if self.__left_right:
            if other_row == other_count - 1:
                this_row = 0
            else:
                this_row = other_row + 1
            this_view = other_view
        else:
            if this_row == this_count - 1:
                this_view = other_view
                this_row = 0
            else:
                other_view = this_view
                this_row += 1

        self.__is_left = other_view == self.ui.tableWidgetTensioningLeft
        if self.__is_left:
            print("going left")
        else:
            print("going right")

        QTimer.singleShot(
            50,
            lambda: other_view.move_to_cell(
                row=this_row,
                column=0))

    def previous_cell(self) -> None:
        if self.__is_left:
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
        view: CustomTableWidget = (self.ui.tableWidgetTensioningLeft
                                   if is_left
                                   else self.ui.tableWidgetTensioningRight)
        if value != "":
            value = value.replace(",", ".")
            deflection: float = float(value)
        else:
            deflection = 0.0

        if is_left:
            tension: float = self.calculate_tension(
                fit_model=self.__fit_left,
                deflection=deflection)
        else:
            tension = self.calculate_tension(
                fit_model=self.__fit_right,
                deflection=deflection)

        _, kgf, lbf = self.unit_module.convert_units(
            value=tension,
            source=UnitEnum.NEWTON)

        tension_converted: float = tension

        if self.__unit == UnitEnum.KGF:
            tension_converted = kgf
        elif self.__unit == UnitEnum.LBF:
            tension_converted = lbf

        value = (f"{tension_converted:.0f}"
                 if self.__unit == UnitEnum.NEWTON
                 else f"{tension_converted:.1f}")
        item = NumericTableWidgetItem(value)
        item.setFlags(Qt.ItemFlag.ItemIsEnabled)
        view.setItem(row, 1, item)
        if is_left:
            spoke_no: int = (
                row + 1 if self.__clockwise
                else self.__spoke_amount_left - row)
            self.__tensions_left[spoke_no - 1] = tension
        else:
            spoke_no = (
                row + 1 if self.__clockwise
                else self.__spoke_amount_right - row)
            self.__tensions_right[spoke_no - 1] = tension
        self.plot_spoke_tensions()

    def use_spoke(self, is_left: bool) -> None:
        """
        Write the selected spoke details to plainTextEditSelectedSpoke
        and save the formula for the spoke based
        on the selected or first measurement.
        """
        view: QTableWidget = self.ui.tableWidgetSpokeSelection
        spoke_id: int = Generics.get_selected_row_id(view)
        if spoke_id < 0:
            return

        view = self.ui.tableWidgetSpokeMeasurements
        measurement_id: int = Generics.get_selected_row_id(view)
        if measurement_id == -1:
            return
        item: QTableWidgetItem | None = view.item(view.currentRow(), 0)
        if item is None:
            return

        spoke_name: str = (
            f"{self.ui.comboBoxSpokeManufacturer.currentText()} "
            f"{self.ui.lineEditSpokeName.text()}"
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
            self.main_window.status_label_spoke_left.setText(
                f"<- {spoke_name} {self.ui.lineEditSpokeDimension.text()}")
            self.__fit_left = fit_model
        else:
            self.ui.plainTextEditSelectedSpokeRight.setPlainText(spoke_details)
            self.main_window.status_label_spoke_right.setText(
                f"{spoke_name} {self.ui.lineEditSpokeDimension.text()} ->")
            self.__fit_right = fit_model

        if self.__fit_left is not None and self.__fit_right is not None:
            self.ui.tensioningTab.setEnabled(True)

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
        self.chart.update_radar_plot(
            plot_widget=self.canvas.plot_widget,
            left_spokes=left_spokes,
            right_spokes=right_spokes,
            tensions_left=self.__tensions_left,
            tensions_right=self.__tensions_right
        )
