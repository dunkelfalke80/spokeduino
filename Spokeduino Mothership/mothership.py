import os
import sys
import threading
from typing import cast, override
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QStatusBar
from PySide6.QtWidgets import QLayout
from PySide6.QtWidgets import QGroupBox
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QHeaderView
from PySide6.QtWidgets import QLabel
from ui import Ui_mainWindow
from spokeduino_module import SpokeduinoState
from spokeduino_module import SpokeduinoModule
from database_module import DatabaseModule
from setup_module import SetupModule
from spoke_module import SpokeModule
from tensiometer_module import TensiometerModule
from tensioning_module import TensioningModule
from measurement_module import MeasurementModule, MeasurementModeEnum
from unit_module import UnitModule
from unit_module import UnitEnum
from customtablewidget import CustomTableWidget
from helpers import Messagebox
from calculation_module import TensionDeflectionFitter
from visualisation_module import PyQtGraphCanvas, VisualisationModule


class Spokeduino(QMainWindow):
    """
    Main application class for Spokeduino Mothership.

    This class initializes the UI, connects signals and slots,
    and interacts with the SQLite database to populate and
    manage data displayed in the application.
    """
    def __init__(self) -> None:
        """
        Initialize the main application window.
        """
        super().__init__()
        self.current_path: str = os.path.dirname(os.path.realpath(sys.argv[0]))
        self.db_path: str = f"{self.current_path}/spokeduino.sqlite"

        # Initialize database
        schema_file: str = os.path.join(
            self.current_path, "sql", "init_schema.sql")
        data_file: str = os.path.join(
            self.current_path, "sql", "spoke_data.sql")
        self.db = DatabaseModule(self.db_path)
        self.db.initialize_database(schema_file, data_file)

        # For vacuuming on exit
        self.db_changed: bool = False

        self.serial_port = None
        self.waiting_event = threading.Event()
        self.fitter = TensionDeflectionFitter()
        self.chart = VisualisationModule(self.fitter)

        self.ui = Ui_mainWindow()
        self.ui.setupUi(mainWindow=self)
        # Visualisation
        self.measurement_canvas = PyQtGraphCanvas()
        self.tensioning_canvas = PyQtGraphCanvas()
        self.ui.verticalLayoutMeasurementRight.addWidget(
            self.measurement_canvas)
        self.ui.verticalLayoutWheelDiagram.addWidget(
            self.tensioning_canvas)

        self.unit_module = UnitModule(self.ui)
        self.setup_module = SetupModule(
            main_window=self,
            ui=self.ui,
            current_path=self.current_path,
            db=self.db)
        self.messagebox = Messagebox(self, self.ui)
        self.tensiometer_module = TensiometerModule(
            main_window=self,
            ui=self.ui,
            messagebox=self.messagebox,
            setup_module=self.setup_module,
            db=self.db)
        self.measurement_module = MeasurementModule(
            main_window=self,
            ui=self.ui,
            unit_module=self.unit_module,
            tensiometer_module=self.tensiometer_module,
            messagebox=self.messagebox,
            db=self.db,
            fitter=self.fitter,
            chart=self.chart,
            canvas=self.measurement_canvas)
        self.spokeduino_module = SpokeduinoModule(
            ui=self.ui,
            db=self.db,
            setup_module=self.setup_module,
            messagebox=self.messagebox)
        self.spoke_module = SpokeModule(
            main_window=self,
            ui=self.ui,
            measurement_module=self.measurement_module,
            messagebox=self.messagebox,
            db=self.db,
            current_path=self.current_path)
        self.tensioning_module = TensioningModule(
            main_window=self,
            ui=self.ui,
            unit_module=self.unit_module,
            tensiometer_module=self.tensiometer_module,
            messagebox=self.messagebox,
            measurement_module=self.measurement_module,
            db=self.db,
            fitter=self.fitter,
            chart=self.chart,
            canvas=self.tensioning_canvas)

        # Replace the tableWidgetMeasurements with the custom widget
        custom_table = CustomTableWidget(
            parent=self,
            move_to_next_cell_callback=self.measurement_module.next_cell)

        # Set the same object name so the rest of the code works seamlessly
        custom_table.setObjectName("tableWidgetMeasurements")

        # Replace the widget in the layout
        layout: QLayout | None = cast(
            QGroupBox,
            self.ui.tableWidgetMeasurements.parent()).layout()
        if layout:
            layout.replaceWidget(
                self.ui.tableWidgetMeasurements,
                custom_table)

        self.ui.tableWidgetMeasurements.deleteLater()
        self.ui.tableWidgetMeasurements = custom_table

        # Replace the tableWidgetTensionsLeft with the custom widget
        custom_tension_table_left = CustomTableWidget(
            self,
            self.tensioning_module.next_cell_callback_left,
            self.tensioning_module.previous_cell_callback_left)

        # Set the same object name so the rest of the code works seamlessly
        custom_tension_table_left.setObjectName("tableWidgetTensionsLeft")

        # Replace the widget in the layout
        layout: QLayout | None = cast(
            QGroupBox,
            self.ui.tableWidgetTensioningLeft.parent()).layout()
        if layout:
            layout.replaceWidget(
                self.ui.tableWidgetTensioningLeft,
                custom_tension_table_left)

        self.ui.tableWidgetTensioningLeft.deleteLater()
        self.ui.tableWidgetTensioningLeft = custom_tension_table_left

        # Replace the tableWidgetTensionsRight with the custom widget
        custom_tension_table_right = CustomTableWidget(
            self,
            self.tensioning_module.next_cell_callback_right,
            self.tensioning_module.previous_cell_callback_right)

        # Set the same object name so the rest of the code works seamlessly
        custom_tension_table_right.setObjectName("tableWidgetTensionsRight")

        # Replace the widget in the layout
        layout: QLayout | None = cast(
            QGroupBox,
            self.ui.tableWidgetTensioningRight.parent()).layout()
        if layout:
            layout.replaceWidget(
                self.ui.tableWidgetTensioningRight,
                custom_tension_table_right)

        self.ui.tableWidgetTensioningRight.deleteLater()
        self.ui.tableWidgetTensioningRight = custom_tension_table_right

        # Set up the status bar
        self.status_bar: QStatusBar = self.statusBar()

        # Create labels for different information
        self.status_label_spoke = QLabel("Spoke: None")
        self.status_label_spoke_left = QLabel("")
        self.status_label_spoke_right = QLabel("")
        self.status_label_unit = QLabel("Unit: Newton")
        self.status_label_tensiometer = QLabel("Tensiometer: None")
        self.status_label_port = QLabel("Spokeduino: Not Connected")
        self.status_label_fit = QLabel("Fit: linear")

        # Add the labels to the status bar
        self.status_bar.addWidget(self.status_label_spoke_left)
        self.status_bar.addWidget(self.status_label_spoke_right)
        self.status_bar.addWidget(self.status_label_spoke)
        self.status_bar.addPermanentWidget(self.status_label_fit)
        self.status_bar.addPermanentWidget(self.status_label_unit)
        self.status_bar.addPermanentWidget(self.status_label_tensiometer)
        self.status_bar.addPermanentWidget(self.status_label_port)
        self.status_label_spoke.setStyleSheet("font-weight: bold;")

        self.setup_module.setup_language()
        self.setup_module.populate_language_combobox()
        self.setup_module.load_available_com_ports()
        self.tensiometer_module.load_tensiometers()
        self.setup_module.load_settings()
        self.spoke_module.load_manufacturers()
        self.setup_signals_and_slots()
        self.update_statusbar_unit()
        self.update_statusbar_tensiometer()
        self.update_statusbar_spokeduino()
        self.update_statusbar_fit()
        self.measurement_module.set_mode(MeasurementModeEnum.DEFAULT)
        self.ui.tensioningTab.setEnabled(False)

    def setup_signals_and_slots(self) -> None:
        """
        Connect UI elements to their respective event handlers for both tabs.
        """
        # Application wide elements
        self.ui.tabWidget.currentChanged.connect(self.tab_index_changed)

        # Spoke buttons
        self.ui.pushButtonUpdateSpoke.clicked.connect(
            self.spoke_module.update_spoke)
        self.ui.pushButtonDeleteSpoke.clicked.connect(
            self.spoke_module.delete_spoke)
        self.ui.pushButtonClearSpoke.clicked.connect(
            self.spoke_module.clear_spoke_details)
        self.ui.pushButtonSaveAsSpoke.clicked.connect(
            self.spoke_module.save_as_spoke)

        # Synchronize spoke fields and spoke buttons
        self.ui.lineEditName.textChanged.connect(
            self.spoke_module.toggle_spoke_related_buttons)
        self.ui.comboBoxType.currentIndexChanged.connect(
            self.spoke_module.toggle_spoke_related_buttons)
        self.ui.lineEditGauge.textChanged.connect(
            self.spoke_module.toggle_spoke_related_buttons)
        self.ui.lineEditWeight.textChanged.connect(
            self.spoke_module.toggle_spoke_related_buttons)
        self.ui.lineEditDimension.textChanged.connect(
            self.spoke_module.toggle_spoke_related_buttons)

        # Spoke table-related signals
        self.ui.tableWidgetSpokesDatabase.currentCellChanged.connect(
            self.spoke_module.load_spoke_details)
        self.ui.tableWidgetSpokesDatabase.currentCellChanged.connect(
            self.spoke_module.toggle_spoke_related_buttons)

        # Spoke table filters
        self.ui.lineEditFilterName.textChanged.connect(
            self.spoke_module.filter_spoke_table)
        self.ui.comboBoxFilterType.currentTextChanged.connect(
            self.spoke_module.filter_spoke_table)
        self.ui.lineEditFilterGauge.textChanged.connect(
            self.spoke_module.filter_spoke_table)
        header = self.ui.tableWidgetSpokesDatabase.horizontalHeader()
        header.sectionResized.connect(
            self.spoke_module.align_filters_with_table)
        header.sectionMoved.connect(
            self.spoke_module.align_filters_with_table)
        header: QHeaderView = \
            self.ui.tableWidgetSpokesDatabase.horizontalHeader()
        header.sectionClicked.connect(self.spoke_module.sort_by_column)

        # Manufacturer-related buttons and combo boxes
        self.ui.lineEditNewManufacturer.textChanged.connect(
            self.spoke_module.toggle_spoke_related_buttons)
        self.ui.pushButtonSaveAsManufacturer.clicked.connect(
            self.spoke_module.create_new_manufacturer)
        self.ui.comboBoxManufacturer.\
            currentIndexChanged.connect(
                self.spoke_module.load_spokes)

        # Tensiometer-related signals
        self.ui.lineEditNewTensiometer.textChanged.connect(
            self.tensiometer_module.toggle_new_tensiometer_button)
        self.ui.pushButtonNewTensiometer.clicked.connect(
            self.tensiometer_module.create_new_tensiometer)
        self.ui.pushButtonMultipleTensiometers.clicked.connect(
            self.tensiometer_module.toggle_multi_tensiometer_mode)
        self.ui.pushButtonMultipleTensiometers.setCheckable(True)
        self.ui.comboBoxTensiometer.currentIndexChanged.connect(
            self.tensiometer_module.save_tensiometer)
        self.ui.comboBoxTensiometer.currentIndexChanged.connect(
           lambda: self.measurement_module.load_measurements(
               None, None, False))
        self.ui.comboBoxTensiometer.currentIndexChanged.connect(
            self.update_statusbar_tensiometer)

        # Measurement-related signals
        self.ui.tableWidgetMeasurementList.clicked.connect(
            self.measurement_module.select_measurement_row)
        self.ui.tableWidgetMeasurementList.clicked.connect(
            self.spoke_module.toggle_spoke_related_buttons)
        self.ui.pushButtonDeleteMeasurement.clicked.connect(
            self.measurement_module.delete_measurement)
        self.ui.pushButtonNewMeasurement.clicked.connect(
            lambda: self.measurement_module.set_mode(
                MeasurementModeEnum.DEFAULT))
        self.ui.pushButtonNewMeasurement.clicked.connect(
            lambda: self.ui.tabWidget.setCurrentIndex(
                self.ui.tabWidget.indexOf(self.ui.measurementTab)))
        self.ui.pushButtonEditMeasurement.clicked.connect(
            lambda: self.measurement_module.set_mode(
                MeasurementModeEnum.EDIT))
        self.ui.pushButtonEditMeasurement.clicked.connect(
            lambda: self.ui.tabWidget.setCurrentIndex(
                self.ui.tabWidget.indexOf(self.ui.measurementTab)))
        self.ui.tableWidgetMeasurements.itemChanged.connect(
            self.measurement_module.update_measurement_button_states)
        self.ui.tableWidgetMeasurements.currentCellChanged.connect(
            self.measurement_module.update_measurement_button_states)
        self.ui.pushButtonPreviousMeasurement.clicked.connect(
            self.ui.tableWidgetMeasurements.move_to_previous_cell)
        self.ui.pushButtonNextMeasurement.clicked.connect(
            lambda: self.ui.tableWidgetMeasurements.move_to_next_cell(False))
        self.ui.pushButtonSaveMeasurement.clicked.connect(
            lambda: self.spokeduino_module.set_state(
                SpokeduinoState.WAITING))
        self.ui.pushButtonSaveMeasurement.clicked.connect(
            self.measurement_module.save_measurements)
        self.ui.tableWidgetMeasurements.onCellChanged.connect(
            lambda row, column,
            value: self.measurement_module.on_cell_changing(
                row=row, column=column, value=value))

        # Language selection
        self.ui.comboBoxSelectLanguage.currentTextChanged.connect(
            lambda language: self.setup_module.save_setting(
                "language", language))
        self.ui.comboBoxSelectLanguage.currentTextChanged.connect(
            lambda language: self.setup_module.change_language(
                language.lower()))

        # Spokeduino port selection
        self.ui.comboBoxSpokeduinoPort.currentTextChanged.connect(
            lambda port: self.setup_module.save_setting(
                "spokeduino_port", port))
        self.ui.comboBoxSpokeduinoPort.currentTextChanged.connect(
            self.spokeduino_module.restart_spokeduino_port)
        self.ui.checkBoxSpokeduinoEnabled.checkStateChanged.connect(
            self.spokeduino_module.restart_spokeduino_port)
        self.ui.checkBoxSpokeduinoEnabled.checkStateChanged.connect(
            self.update_statusbar_spokeduino)

        # Spokeduino
        self.spokeduino_state: SpokeduinoState = SpokeduinoState.WAITING

        # Measurement units
        self.ui.radioButtonNewton.toggled.connect(
                self.update_statusbar_unit)
        self.ui.radioButtonKgF.toggled.connect(
                self.update_statusbar_unit)
        self.ui.radioButtonLbF.toggled.connect(
                self.update_statusbar_unit)

        self.ui.radioButtonMeasurementDefault.toggled.connect(
            self.measurement_custom)

        # Fit settings
        self.ui.radioButtonFitLinear.toggled.connect(
                self.update_statusbar_fit)
        self.ui.radioButtonFitQuadratic.toggled.connect(
                self.update_statusbar_fit)
        self.ui.radioButtonFitCubic.toggled.connect(
                self.update_statusbar_fit)
        self.ui.radioButtonFitQuartic.toggled.connect(
                self.update_statusbar_fit)
        self.ui.radioButtonFitSpline.toggled.connect(
                self.update_statusbar_fit)
        self.ui.radioButtonFitExponential.toggled.connect(
                self.update_statusbar_fit)
        self.ui.radioButtonFitLogarithmic.toggled.connect(
                self.update_statusbar_fit)
        self.ui.radioButtonFitPowerLaw.toggled.connect(
                self.update_statusbar_fit)

        # Directional settings
        self.ui.radioButtonMeasurementDown.toggled.connect(
            lambda checked:
                self.setup_module.save_setting(
                    "spoke_direction",
                    "down") if checked else None)
        self.ui.radioButtonMeasurementUp.toggled.connect(
            lambda checked:
                self.setup_module.save_setting(
                    "spoke_direction",
                    "up") if checked else None)
        self.ui.radioButtonRotationClockwise.toggled.connect(
            lambda checked:
                self.setup_module.save_setting(
                    "rotation_direction",
                    "clockwise") if checked else None)
        self.ui.radioButtonRotationAnticlockwise.toggled.connect(
            lambda checked:
                self.setup_module.save_setting(
                    "rotation_direction",
                    "anticlockwise") if checked else None)
        self.ui.radioButtonSideBySide.toggled.connect(
            lambda checked:
                self.setup_module.save_setting(
                    "measurement_type",
                    "side_by_side") if checked else None)
        self.ui.radioButtonLeftRight.toggled.connect(
            lambda checked:
                self.setup_module.save_setting(
                    "measurement_type",
                    "left_right") if checked else None)
        self.ui.radioButtonRightLeft.toggled.connect(
            lambda checked:
                self.setup_module.save_setting(
                    "measurement_type",
                    "right_left") if checked else None)

        # Unit converter
        self.ui.lineEditConverterNewton.textChanged.connect(
            lambda: self.unit_module.convert_units_realtime(UnitEnum.NEWTON))
        self.ui.lineEditConverterKgF.textChanged.connect(
            lambda: self.unit_module.convert_units_realtime(UnitEnum.KGF))
        self.ui.lineEditConverterLbF.textChanged.connect(
            lambda: self.unit_module.convert_units_realtime(UnitEnum.LBF))

        # Tensioning related signals
        self.ui.pushButtonStartTensioning.clicked.connect(
            self.tensioning_module.start_tensioning)

        # Left tensioning table
        self.ui.pushButtonUseLeft.clicked.connect(
            lambda: self.tensioning_module.use_spoke(True))
        self.ui.lineEditSpokeAmountLeft.textChanged.connect(
            lambda: self.tensioning_module.setup_table(is_left=True))
        self.ui.lineEditTargetTensionLeft.textChanged.connect(
            lambda: self.tensioning_module.setup_table(True))

        # Right tensioning table
        self.ui.pushButtonUseRight.clicked.connect(
            lambda: self.tensioning_module.use_spoke(False))
        self.ui.lineEditSpokeAmountRight.textChanged.connect(
            lambda: self.tensioning_module.setup_table(is_left=False))
        self.ui.lineEditTargetTensionRight.textChanged.connect(
            lambda: self.tensioning_module.setup_table(False))

    @override
    def resizeEvent(self, event) -> None:
        """
        Handle window resize event for the main Window.
        Realigns filter fields with the table headers.
        """
        super().resizeEvent(event)
        self.spoke_module.align_filters_with_table()

    @override
    def closeEvent(self, event) -> None:
        """
        Handle the close event for the main window.
        Run VACUUM if the database has been modified.
        """
        self.spokeduino_module.close_serial_port()
        if self.db_changed:
            self.db.vacuum()
        event.accept()

    def tab_index_changed(self) -> None:
        match self.ui.tabWidget.currentWidget():
            case self.ui.measurementTab:
                self.measurement_module.setup_measurements_table()
                self.ui.tableWidgetMeasurements.stop_sorting()
            case self.ui.tensioningTab:
                self.chart.clear_fit_plot(self.measurement_canvas.plot_widget)
                self.measurement_module.set_mode(
                    MeasurementModeEnum.DEFAULT)
                self.ui.pushButtonStartTensioning.setText("Start")
                self.ui.tableWidgetTensioningLeft.setEnabled(False)
                self.ui.tableWidgetTensioningRight.setEnabled(False)
                self.tensioning_module.setup_table(True)
                self.tensioning_module.setup_table(False)
            case self.ui.databaseTab:
                self.chart.clear_fit_plot(self.measurement_canvas.plot_widget)
                self.measurement_module.set_mode(
                    MeasurementModeEnum.DEFAULT)
                self.spoke_module.load_spoke_details()
                QTimer.singleShot(
                    50,
                    self.spoke_module.align_filters_with_table)
            case self.ui.setupTab:
                self.chart.clear_fit_plot(self.measurement_canvas.plot_widget)
                self.measurement_module.set_mode(
                    MeasurementModeEnum.DEFAULT)

    def measurement_custom(self) -> None:
        if self.ui.radioButtonMeasurementCustom.isChecked():
            self.ui.pushButtonMultipleTensiometers.setEnabled(False)
            self.setup_module.save_setting(
                "measaurement_custom",
                "1")
            self.measurement_module.set_mode(
                MeasurementModeEnum.CUSTOM)
        else:
            self.ui.pushButtonMultipleTensiometers.setEnabled(True)
            self.setup_module.save_setting(
                "measaurement_custom",
                "0")
            self.measurement_module.set_mode(
                MeasurementModeEnum.DEFAULT)

    def update_statusbar_unit(self) -> None:
        self.status_label_unit.setText(
            f"Unit: {self.unit_module.get_unit().value}")
        self.setup_module.save_setting(
            "unit",
            self.unit_module.get_unit().value)

    def update_statusbar_fit(self) -> None:
        _, description = self.measurement_module.get_fit()
        self.status_label_fit.setText(
            f"Fit: {description}")
        self.setup_module.save_setting("fit", description)

    def update_statusbar_tensiometer(self) -> None:
        self.status_label_tensiometer.setText(
            f"Tensiometer: {self.ui.comboBoxTensiometer.currentText()}")

    def update_statusbar_spokeduino(self) -> None:
        spokeduino_status: str = (
            self.ui.comboBoxSpokeduinoPort.currentText()
            if self.ui.checkBoxSpokeduinoEnabled.isChecked()
            else "Not connected")
        self.status_label_port.setText(
            f"Spokeduino: {spokeduino_status}")


def trace_calls(frame, event, arg):
    if event == "call":
        print(f"Calling {frame.f_code.co_name} at "
              f"{frame.f_lineno} in {frame.f_code.co_filename}")
    return trace_calls


def main() -> None:
    """
    Entry point for the Spokeduino Mothership application.

    Initializes the QApplication and the main application window.
    """
    # sys.settrace(trace_calls)

    app = QApplication(sys.argv)
    window = Spokeduino()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
