import os
import sys
import threading
from typing import cast, Any, override
from PySide6.QtCore import Qt
from PySide6.QtCore import QAbstractItemModel
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import QTimer
from PySide6.QtGui import QStandardItemModel
from PySide6.QtGui import QStandardItem
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QLayout
from PySide6.QtWidgets import QGroupBox
from PySide6.QtWidgets import QTableView
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QHeaderView
from PySide6.QtWidgets import QTableWidgetItem
from ui import Ui_mainWindow
from sql_queries import SQLQueries
from helpers import SpokeTableModel
from helpers import TextChecker
from spokeduino_module import SpokeduinoState
from spokeduino_module import SpokeduinoModule
from database_module import DatabaseModule
from setup_module import SetupModule
from spoke_module import SpokeModule
from measurement_module import MeasurementModule
from unit_converter import UnitConverter
from unit_converter import UnitEnum
from customtablewidget import CustomTableWidget
from helpers import Messagebox

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
        schema_file: str = os.path.join(self.current_path, "sql", "init_schema.sql")
        data_file: str = os.path.join(self.current_path, "sql", "default_data.sql")
        self.db = DatabaseModule(self.db_path)
        self.db.initialize_database(schema_file, data_file)
        self.serial_port = None
        self.waiting_event = threading.Event()

        # For vacuuming on exit
        self.db_changed: bool = False

        self.multi_tensiometer_enabled: bool = False

        self.ui = Ui_mainWindow()
        self.ui.setupUi(mainWindow=self)
        self.setup_module = SetupModule(
            main_window=self,
            ui=self.ui,
            current_path=self.current_path,
            db=self.db)
        self.spoke_module = SpokeModule(
            main_window=self,
            ui=self.ui,
            current_path=self.current_path,
            db=self.db)
        self.measurement_module = MeasurementModule(
            main_window=self,
            ui=self.ui)
        self.messagebox = Messagebox(self)
        self.spokeduino_module = SpokeduinoModule(
            ui=self.ui,
            db=self.db,
            setup_module=self.setup_module,
            messagebox=self.messagebox)

        # Replace the tableWidgetMeasurements with the custom widget
        custom_table = CustomTableWidget(parent=self)

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

        # Replace the tableViewTensionsLeft with the custom widget
        custom_tension_table_left = CustomTableWidget(
            parent=self,
            move_to_next_cell_callback=self.next_cell_tensioning_callback_left,
            move_to_previous_cell_callback=self.previous_cell_tensioning_callback_left)

        # Set the same object name so the rest of the code works seamlessly
        custom_tension_table_left.setObjectName("tableViewTensionsLeft")

        # Replace the widget in the layout
        layout: QLayout | None = cast(
            QGroupBox,
            self.ui.tableViewTensioningLeft.parent()).layout()
        if layout:
            layout.replaceWidget(
                self.ui.tableViewTensioningLeft,
                custom_tension_table_left)

        self.ui.tableViewTensioningLeft.deleteLater()
        self.ui.tableViewTensioningLeft = custom_tension_table_left

        # Replace the tableViewTensionsRight with the custom widget
        custom_tension_table_right = CustomTableWidget(
            parent=self,
            move_to_next_cell_callback=self.next_cell_tensioning_callback_right,
            move_to_previous_cell_callback=self.previous_cell_tensioning_callback_right)

        # Set the same object name so the rest of the code works seamlessly
        custom_tension_table_right.setObjectName("tableViewTensionsRight")

        # Replace the widget in the layout
        layout: QLayout | None = cast(
            QGroupBox,
            self.ui.tableViewTensioningRight.parent()).layout()
        if layout:
            layout.replaceWidget(
                self.ui.tableViewTensioningRight,
                custom_tension_table_right)

        self.ui.tableViewTensioningRight.deleteLater()
        self.ui.tableViewTensioningRight = custom_tension_table_right

        self.unit_converter = UnitConverter(self.ui)
        self.setup_module.setup_language()
        self.setup_module.populate_language_combobox()
        self.setup_module.load_available_com_ports()
        self.setup_module.load_tensiometers()
        self.setup_signals_and_slots()
        self.setup_module.load_settings()
        self.spoke_module.load_manufacturers()
        self.toggle_new_manufacturer_button()
        # Delay to ensure Qt's focus/selection state is updated
        QTimer.singleShot(100,
            self.spoke_module.align_filters_with_table)

        # Tensioning related entries
        self.spoke_tensions_left: list[tuple[float, float]] = []
        self.spoke_tensions_right: list[tuple[float, float]] = []
        self.left_spoke_formula: str = ""
        self.right_spoke_formula: str = ""
        self.unit: UnitEnum = self.get_unit()

    def setup_signals_and_slots(self) -> None:
        """
        Connect UI elements to their respective event handlers for both tabs.
        """
        # Create and Edit Spoke Buttons
        self.ui.pushButtonCreateSpoke.clicked.connect(self.create_new_spoke)
        self.ui.pushButtonCreateSpoke2.clicked.connect(
            self.create_new_spoke)
        self.ui.pushButtonEditSpoke.clicked.connect(
            self.spoke_module.modify_spoke)
        self.ui.pushButtonDeleteSpoke.clicked.connect(
            self.spoke_module.delete_spoke)

        # Synchronize fields and buttons
        self.ui.lineEditName.textChanged.connect(
            self.toggle_spoke_buttons)
        self.ui.lineEditName2.textChanged.connect(
            self.toggle_spoke_buttons)

        self.ui.comboBoxType.currentIndexChanged.connect(
            self.toggle_spoke_buttons)
        self.ui.comboBoxType2.currentIndexChanged.connect(
            self.toggle_spoke_buttons)

        self.ui.lineEditGauge.textChanged.connect(
            self.toggle_spoke_buttons)
        self.ui.lineEditGauge2.textChanged.connect(
            self.toggle_spoke_buttons)

        self.ui.lineEditWeight.textChanged.connect(
            self.toggle_spoke_buttons)
        self.ui.lineEditWeight2.textChanged.connect(
            self.toggle_spoke_buttons)

        self.ui.lineEditDimension.textChanged.connect(
            self.toggle_spoke_buttons)
        self.ui.lineEditDimension2.textChanged.connect(
            self.toggle_spoke_buttons)

        # Synchronize combobox and table for spokes
        self.ui.comboBoxSpoke.currentIndexChanged.connect(
            lambda: self.spoke_module.sync_spoke_selection(
                self.ui.comboBoxSpoke))
        self.ui.comboBoxSpoke2.currentIndexChanged.connect(
            lambda: self.spoke_module.sync_spoke_selection(
                self.ui.comboBoxSpoke2))
        self.ui.comboBoxSpoke.currentIndexChanged.connect(
            lambda: self.spoke_module.update_spoke_details(
                self.ui.comboBoxSpoke))
        self.ui.comboBoxSpoke2.currentIndexChanged.connect(
            lambda: self.spoke_module.update_spoke_details(
                self.ui.comboBoxSpoke2))
        self.ui.comboBoxSpoke.currentIndexChanged.connect(
            self.spoke_module.select_spoke_row)
        self.ui.comboBoxSpoke2.currentIndexChanged.connect(
            self.spoke_module.select_spoke_row)
        self.ui.tableViewSpokesDatabase.clicked.connect(
            self.spoke_module.select_spoke_from_table)

        # Filters
        self.ui.tabWidget.currentChanged.connect(
        # Delay to ensure Qt's focus/selection state is updated
        QTimer.singleShot(100,
            self.spoke_module.align_filters_with_table))
        self.ui.lineEditFilterName.textChanged.connect(
            self.spoke_module.filter_spoke_table)
        self.ui.comboBoxFilterType.currentTextChanged.connect(
            self.spoke_module.filter_spoke_table)
        self.ui.lineEditFilterGauge.textChanged.connect(
            self.spoke_module.filter_spoke_table)
        header = self.ui.tableViewSpokesDatabase.horizontalHeader()
        header.sectionResized.connect(
            self.spoke_module.align_filters_with_table)
        header.sectionMoved.connect(
            self.spoke_module.align_filters_with_table)

        # Manufacturer-related buttons and combo boxes
        self.ui.lineEditNewManufacturer.textChanged.connect(
            self.toggle_new_manufacturer_button)
        self.ui.lineEditNewManufacturer2.textChanged.connect(
            self.toggle_new_manufacturer_button)
        self.ui.pushButtonNewManufacturer.clicked.connect(
            self.create_new_manufacturer)
        self.ui.pushButtonNewManufacturer2.clicked.connect(
            self.create_new_manufacturer)
        self.ui.comboBoxManufacturer.\
            currentIndexChanged.connect(
                self.spoke_module.load_spokes)
        self.ui.comboBoxManufacturer2.\
            currentIndexChanged.connect(
                self.spoke_module.load_spokes)
        self.ui.comboBoxManufacturer.currentIndexChanged.connect(
            lambda index: self.spoke_module.sync_manufacturer_selection(
                self.ui.comboBoxManufacturer, index))
        self.ui.comboBoxManufacturer2.currentIndexChanged.connect(
            lambda index: self.spoke_module.sync_manufacturer_selection(
                self.ui.comboBoxManufacturer, index))

        # Tensiometer-related signals
        self.ui.comboBoxTensiometer.currentIndexChanged.connect(
            self.spoke_module.load_spoke_measurements)
        self.ui.lineEditNewTensiometer.textChanged.connect(
            self.toggle_new_tensiometer_button)
        self.ui.pushButtonNewTensiometer.clicked.connect(
            self.create_new_tensiometer)
        self.ui.pushButtonMultipleTensiometers.clicked.connect(
            self.toggle_multi_tensiometer_mode)
        self.ui.pushButtonMultipleTensiometers.setCheckable(True)

        # Measurement-related signals
        self.ui.tabWidget.currentChanged.connect(self.tab_index_changed)
        self.ui.pushButtonDeleteMeasurement.clicked.connect(
            self.delete_measurement)
        self.ui.pushButtonAddMeasurement.clicked.connect(
            lambda: self.ui.tabWidget.setCurrentIndex(
                self.ui.tabWidget.indexOf(self.ui.measurementTab)))
        self.ui.tableViewMeasurements.clicked.connect(
            self.select_measurement_row)
        self.ui.tableWidgetMeasurements.itemChanged.connect(
            self.measurement_module.update_measurement_button_states)
        self.ui.tableWidgetMeasurements.currentCellChanged.connect(
            self.measurement_module.update_measurement_button_states)
        self.ui.pushButtonCalculateFormula.clicked.connect(
            self.measurement_module.toggle_calculate_button)
        self.ui.pushButtonMeasureSpoke.clicked.connect(
            lambda: self.spokeduino_module.set_state(
                SpokeduinoState.MEASURING))
        self.ui.pushButtonPreviousMeasurement.clicked.connect(
        self.ui.tableWidgetMeasurements.move_to_previous_cell)
        self.ui.pushButtonNextMeasurement.clicked.connect(
            lambda: self.ui.tableWidgetMeasurements.move_to_next_cell(False))
        self.ui.pushButtonSaveMeasurement.clicked.connect(
        lambda: self.spokeduino_module.set_state(
            SpokeduinoState.WAITING))
        self.ui.pushButtonSaveMeasurement.clicked.connect(
            self.save_measurements)

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

        # Tensiometer selection
        self.ui.comboBoxTensiometer.currentIndexChanged.connect(self.save_tensiometer)

        # Measurement units
        self.ui.radioButtonNewton.toggled.connect(
            lambda checked:
                self.setup_module.save_setting(
                    "unit", "Newton")
                if checked else None)
        self.ui.radioButtonKgF.toggled.connect(
            lambda checked:
                self.setup_module.save_setting(
                    "unit", "kgF")
                if checked else None)
        self.ui.radioButtonLbF.toggled.connect(
            lambda checked:
                self.setup_module.save_setting(
                    "unit", "lbF")
                if checked else None)
        self.ui.radioButtonNewton.toggled.connect(
            lambda checked:
                self.set_unit(
                    UnitEnum.NEWTON)
                if checked else None)
        self.ui.radioButtonKgF.toggled.connect(
            lambda checked:
                self.set_unit(
                    UnitEnum.KGF)
                if checked else None)
        self.ui.radioButtonLbF.toggled.connect(
            lambda checked:
                self.set_unit(
                    UnitEnum.LBF)
                if checked else None)

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
            lambda: self.unit_converter.convert_units_realtime(UnitEnum.NEWTON))
        self.ui.lineEditConverterKgF.textChanged.connect(
            lambda: self.unit_converter.convert_units_realtime(UnitEnum.KGF))
        self.ui.lineEditConverterLbF.textChanged.connect(
            lambda: self.unit_converter.convert_units_realtime(UnitEnum.LBF))

        # Table sorting
        header: QHeaderView = \
            self.ui.tableViewSpokesDatabase.horizontalHeader()
        header.sectionClicked.connect(self.spoke_module.sort_by_column)

        # Tensioning related signals
        self.ui.pushButtonStartTensioning.clicked.connect(
            self.start_tensioning)

        # Left tensioning table
        self.ui.pushButtonUseLeft.clicked.connect(
            lambda: self.use_spoke(True))
        self.ui.lineEditSpokeAmountLeft.textChanged.connect(
            lambda: self.setup_tensioning_table(is_left=True))
        self.ui.lineEditTargetTensionLeft.textChanged.connect(
            lambda: self.setup_tensioning_table(is_left=True))
        self.ui.tableViewTensioningLeft.cellChanged.connect(
            lambda row, column: self.on_tensioning_cell_changed(
                is_left=True, row=row, column=column))
        self.ui.tableViewTensioningLeft.onCellDataChanging.connect(
            lambda row, column, value: self.on_tensioning_cell_changing(
                is_left=True, row=row, column=column, value=value))

        # Right tensioning table
        self.ui.pushButtonUseRight.clicked.connect(
            lambda: self.use_spoke(False))
        self.ui.lineEditSpokeAmountRight.textChanged.connect(
            lambda: self.setup_tensioning_table(is_left=False))
        self.ui.lineEditTargetTensionRight.textChanged.connect(
            lambda: self.setup_tensioning_table(is_left=False))
        self.ui.tableViewTensioningRight.cellChanged.connect(
            lambda row, column: self.on_tensioning_cell_changed(
                is_left=False, row=row, column=column))
        self.ui.tableViewTensioningRight.onCellDataChanging.connect(
            lambda row, column, value: self.on_tensioning_cell_changing(
                is_left=True, row=row, column=column, value=value))

        # Spokeduino
        self.spokeduino_state: SpokeduinoState = SpokeduinoState.WAITING

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
                self.setup_measurements_table()
            case self.ui.tensioningTab:
                self.setup_tensioning_table(True)
                self.setup_tensioning_table(False)

    def delete_measurement(self) -> None:
        """
        Delete the currently selected measurement from the measurements table.
        Deletes only if there is one measurement or a measurement row is selected.
        """
        view: QTableView = self.ui.tableViewMeasurements
        model: SpokeTableModel = cast(SpokeTableModel, view.model())

        if model is None or model.rowCount() == 0:
            self.messagebox.err("No measurements available to delete.")
            return

        # If there is only one measurement, delete it directly
        if model.rowCount() == 1:
            # Use the first row's ID
            measurement_id: int | None = model.get_id(0)
            if measurement_id is None:
                self.messagebox.err("No measurement found.")
                return
            measurement_id = int(measurement_id)
        else:
            # If a measurement row is selected, delete the selected measurement
            selected_index: QModelIndex = view.currentIndex()
            if not selected_index.isValid():
                self.messagebox.err("No measurement row selected for deletion.")
                return

            # Use the selected row's ID
            measurement_id = model.get_id(selected_index.row())
            if measurement_id is None:
                self.messagebox.err("No measurement found.")
                return
            measurement_id = int(measurement_id)

        # Execute the deletion query
        self.db.execute_query(
            query=SQLQueries.DELETE_MEASUREMENT,
            params=(measurement_id,),
        )

        # Clear selection and reload the measurements
        view.clearSelection()
        self.spoke_module.load_spoke_measurements()

    def select_measurement_row(self, index: QModelIndex) -> None:
        """
        Handle row selection in tableViewMeasurements
        This function ensures that the correct measurement row is highlighted.
        """
        if not index.isValid():
            return

        row: int = index.row()
        self.ui.tableViewMeasurements.selectRow(row)

    def toggle_new_tensiometer_button(self) -> None:
        """
        Enable or disable pushButtonNewTensiometer based on the text in
        lineEditNewTensiometer.
        """
        is_filled = bool(self.ui.lineEditNewTensiometer.text())
        self.ui.pushButtonNewTensiometer.setEnabled(is_filled)

    def toggle_new_manufacturer_button(self) -> None:
        """
        Enable or disable pushButtonNewManufacturer
        based on lineEditNewManufacturer.
        """
        self.ui.pushButtonNewManufacturer.setEnabled(
            len(self.ui.lineEditNewManufacturer.text()) > 0)
        self.ui.pushButtonNewManufacturer2.setEnabled(
            len(self.ui.lineEditNewManufacturer2.text()) > 0
        )

    def toggle_spoke_buttons(self) -> None:
        """
        Enable or disable pushButtonCreateSpoke
        and pushButtonEditSpoke based on spoke detail fields.
        """
        required_fields_filled: bool = all([
            self.ui.lineEditName.text(),
            self.ui.comboBoxType.currentIndex() >= 0,
            self.ui.lineEditGauge.text(),
            self.ui.lineEditWeight.text(),
            self.ui.lineEditDimension.text()
        ])
        self.ui.pushButtonCreateSpoke.setEnabled(required_fields_filled)
        self.ui.pushButtonEditSpoke.setEnabled(
            required_fields_filled and
            self.ui.comboBoxSpoke.currentIndex() >= 0)

    def toggle_multi_tensiometer_mode(self) -> None:
        """
        Enable or disable multi-selection mode for comboBoxTensiometer.
        """
        if not self.multi_tensiometer_enabled:
            # Enable multi-selection mode
            self.multi_tensiometer_enabled = True
            self.ui.pushButtonMultipleTensiometers.setChecked(True)

            # Use a QStandardItemModel to allow checkboxes
            model = QStandardItemModel(self.ui.comboBoxTensiometer)
            self.ui.comboBoxTensiometer.setModel(model)  # Set the model early

            for tensiometer in self.db.execute_select(SQLQueries.GET_TENSIOMETERS):
                item = QStandardItem(tensiometer[1])
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable)
                item.setCheckState(Qt.CheckState.Unchecked)
                item.setData(tensiometer[0], Qt.ItemDataRole.UserRole)
                model.appendRow(item)

            # Disable manual typing
            self.ui.comboBoxTensiometer.setEditable(False)

        else:
            # Disable multi-selection mode
            self.multi_tensiometer_enabled = False
            self.ui.pushButtonMultipleTensiometers.setChecked(False)

            # Restore single-selection mode
            self.ui.comboBoxTensiometer.clear()
            self.setup_module.load_tensiometers()

            # Restore the original tensiometer selection
            selected_tensiometers: list[tuple[int, str]] = self.get_selected_tensiometers()
            if selected_tensiometers:
                tensiometer_id, _ = selected_tensiometers[0]
                index = self.ui.comboBoxTensiometer.findData(tensiometer_id)
                if index != -1:
                    self.ui.comboBoxTensiometer.setCurrentIndex(index)

    def create_new_tensiometer(self) -> None:
        """
        Insert a new tensiometer into the tensiometers table.
        """
        tensiometer_name: str = self.ui.lineEditNewTensiometer.text()
        if not tensiometer_name:
            return

        self.ui.lineEditNewTensiometer.clear()
        _ = self.db.execute_query(
            query=SQLQueries.ADD_TENSIOMETER,
            params=(tensiometer_name,),
        )
        self.setup_module.load_tensiometers()

        index: int = self.ui.comboBoxTensiometer.findText(tensiometer_name)
        if index != -1:
            self.ui.comboBoxTensiometer.setCurrentIndex(index)

    def create_new_manufacturer(self) -> None:
        """
        Insert a new manufacturer into the manufacturers table and select it.
        """
        manufacturer_name: str = (
            self.ui.lineEditNewManufacturer.text()
            if self.sender() == self.ui.pushButtonNewManufacturer
            else self.ui.lineEditNewManufacturer2.text()
        )
        if not manufacturer_name:
            return

        new_manufacturer_id: int | None = self.db.execute_query(
            query=SQLQueries.ADD_MANUFACTURER,
            params=(manufacturer_name,),
        )

        self.ui.lineEditNewManufacturer.clear()
        self.ui.lineEditNewManufacturer2.clear()
        self.spoke_module.load_manufacturers()

        if new_manufacturer_id is None:
            return
        new_manufacturer_id = int(new_manufacturer_id)

        self.ui.comboBoxManufacturer.setCurrentIndex(
            self.ui.comboBoxManufacturer.findData(
                new_manufacturer_id))

    def create_new_spoke(self) -> None:
        """
        Insert a new spoke into the spokes table for the selected manufacturer.
        """
        from_database: bool = self.sender() == self.ui.pushButtonCreateSpoke
        manufacturer_id: int | None = (
            self.ui.comboBoxManufacturer.currentData()
            if from_database
            else self.ui.comboBoxManufacturer2.currentData())

        if manufacturer_id is None:
            return
        manufacturer_id = int(manufacturer_id)

        type_id, gauge, weight, \
            spoke_name, dimension, comment = \
            self.spoke_module.get_database_spoke_data(from_database)

        new_spoke_id: int | None = self.db.execute_query(
            query=SQLQueries.ADD_SPOKE,
            params=(manufacturer_id, spoke_name,
                    type_id, gauge, weight, dimension, comment),
        )
        if new_spoke_id is None:
            return
        new_spoke_id = int(new_spoke_id)

        self.spoke_module.load_spokes()
        self.ui.comboBoxSpoke.setCurrentIndex(
            self.ui.comboBoxSpoke.findData(new_spoke_id)
        )
        self.ui.comboBoxSpoke2.setCurrentIndex(
            self.ui.comboBoxSpoke2.findData(new_spoke_id)
        )

    def use_spoke(self, left: bool) -> None:
        """
        Write the selected spoke details to plainTextEditSelectedSpoke
        and save the formula for the spoke based on the selected or first measurement.
        """
        res, spoke_id = self.spoke_module.get_selected_spoke_id()
        if not res:
            return

        # Fetch spoke details from the database
        spoke: list[Any] = self.db.execute_select(
            SQLQueries.GET_SPOKES_BY_ID,
            params=(spoke_id,)
        )
        if not spoke:
            self.messagebox.err("Spoke not found in the database.")
            return

        # Fetch the current tensiometer ID
        tensiometer_id: int | None = self.ui.comboBoxTensiometer.currentData()
        if tensiometer_id is None:
            self.messagebox.err("A single tensiometer must be selected first.")
            return
        tensiometer_id = int(tensiometer_id)

        # Fetch measurements for the selected spoke and tensiometer
        measurements: list[Any] = self.db.execute_select(
            query=SQLQueries.GET_MEASUREMENTS,
            params=(spoke_id, tensiometer_id)
        )
        if not measurements:
            self.messagebox.err("No measurements found for the selected spoke.")
            return

        # Determine which measurement to use
        selected_index: QModelIndex = self.ui.tableViewMeasurements.currentIndex()
        if selected_index.isValid():
            # Use the selected measurement
            selected_row = selected_index.row()
            formula = measurements[selected_row][-2]  # Assuming formula is the second-to-last field
        else:
            # Use the first measurement
            formula = measurements[0][-2]

        # Extract and format spoke details
        _, name, _, gauge, _, dimensions, comment, *_ = spoke[0]
        spoke_details = (
            f"Name: {name}\n"
            f"Gauge: {gauge}\n"
            f"Dimensions: {dimensions}\n"
            f"Comment: {comment}"
        )

        # Set the details and save the formula
        if left:
            self.ui.plainTextEditSelectedSpokeLeft.setPlainText(spoke_details)
            self.left_spoke_formula = formula
        else:
            self.ui.plainTextEditSelectedSpokeRight.setPlainText(spoke_details)
            self.right_spoke_formula = formula

    def get_unit(self) -> UnitEnum:
        """
        Returns the tension unit currently set, or Newton as default
        """
        if self.ui.radioButtonKgF.isChecked():
            return UnitEnum.KGF
        elif self.ui.radioButtonLbF.isChecked():
            return UnitEnum.LBF
        return UnitEnum.NEWTON

    def set_unit(self, unit: UnitEnum) -> None:
        self.unit = unit

    def get_selected_tensiometers(self) -> list[tuple[int, str]]:
        """
        Retrieve the IDs and names of selected tensiometers based on the mode.
        :return: List of tuples with (ID, Name) for selected tensiometers.
        """
        model: QAbstractItemModel = self.ui.comboBoxTensiometer.model()
        selected_tensiometers: list[Any] = []

        # Fetch the primary tensiometer ID from settings
        primary_tensiometer: list[Any] = self.db.execute_select(
            query=SQLQueries.GET_SINGLE_SETTING,
            params=("tensiometer_id",)
        )

        if primary_tensiometer is None or not primary_tensiometer:
            return []
        primary_tensiometer_id: int = int(primary_tensiometer[0][0])

        if self.multi_tensiometer_enabled:
            # Ensure model is a QStandardItemModel
            if isinstance(model, QStandardItemModel):
                # Multi-tensiometer mode: return all checked tensiometers
                for row in range(model.rowCount()):
                    item = model.item(row)  # Safely access item()
                    if item and item.checkState() == Qt.CheckState.Checked:
                        tensiometer_id = item.data(Qt.ItemDataRole.UserRole)
                        tensiometer_name = item.text()
                        selected_tensiometers.append((tensiometer_id, tensiometer_name))
            else:
                self.messagebox.err("Model is not a QStandardItemModel; cannot retrieve selected items.")
        else:
            # Single-tensiometer mode: return the currently selected one
            current_index: int = self.ui.comboBoxTensiometer.currentIndex()
            if current_index != -1:
                tensiometer_id = self.ui.comboBoxTensiometer.itemData(current_index)
                tensiometer_name: str = self.ui.comboBoxTensiometer.currentText()
                selected_tensiometers.append((tensiometer_id, tensiometer_name))

        # Reorder tensiometers to place the primary one first
        selected_tensiometers.sort(key=lambda x: x[0] != primary_tensiometer_id)

        return selected_tensiometers

    def setup_measurements_table(self) -> None:
        """
        Set up the tableWidgetMeasurements with
        editable fields for tension values
        and selected tensiometers.
        """
        # Clear all cells, rows, and columns
        view: CustomTableWidget = self.ui.tableWidgetMeasurements
        view.clearContents()
        view.setRowCount(0)
        view.setColumnCount(0)

        # Handle the measurement direction
        if self.ui.radioButtonMeasurementDown.isChecked():
            tensions_newton = list(range(1600, 200, -100))
        else:
            tensions_newton = list(range(300, 1700, 100))

        # Handle the measurement units
        unit_index_map: dict[UnitEnum, int] = {
            UnitEnum.NEWTON: 0,
            UnitEnum.KGF: 1,
            UnitEnum.LBF: 2,
        }
        unit_index: int = unit_index_map[self.unit]

        tensions_converted: list[float] = [
            self.unit_converter.convert_units(
                value=value,
                source=UnitEnum.NEWTON)[unit_index]
            for value in tensions_newton]

        # Populate row headers with converted force values
        view.setRowCount(len(tensions_converted))
        if self.unit == UnitEnum.NEWTON:
            view.setVerticalHeaderLabels(
                [f"{value} {self.unit.value}" for value in tensions_converted]
            )
        else:
            view.setVerticalHeaderLabels(
                [f"{value:.1f} {self.unit.value}" for value in tensions_converted]
            )

        # Get selected tensiometers and populate column headers
        tensiometers: list[tuple[int, str]] = self.get_selected_tensiometers()
        view.setColumnCount(len(tensiometers))
        for col, (tensiometer_id, tensiometer_name) in enumerate(tensiometers):
            item = QTableWidgetItem(tensiometer_name)
            item.setData(Qt.ItemDataRole.UserRole, tensiometer_id)
            view.setHorizontalHeaderItem(col, item)

        # Make all cells editable
        for row in range(len(tensions_converted)):
            for col in range(len(tensiometers)):
                item = QTableWidgetItem()
                item.setFlags(Qt.ItemFlag.ItemIsEditable |
                              Qt.ItemFlag.ItemIsEnabled)
                view.setItem(row, col, item)
        view.move_to_specific_cell(0, 0)

    def save_tensiometer(self) -> None:
        if self.multi_tensiometer_enabled: # Runtime only
            return

        current_index: int = self.ui.comboBoxTensiometer.currentIndex()
        if current_index != -1:
            tensiometer_id = self.ui.comboBoxTensiometer.itemData(current_index)
            self.setup_module.save_setting(
                key="tensiometer_id",
                value=str(tensiometer_id))

    def save_measurements(self) -> None:
        """
        Save measurement data for all columns in tableWidgetMeasurements.
        """
        table: CustomTableWidget = self.ui.tableWidgetMeasurements
        db: DatabaseModule = self.db  # Reference to the database module

        # Ensure a valid spoke ID is selected
        res, spoke_id = self.spoke_module.get_selected_spoke_id()
        if not res:
            self.messagebox.err("No spoke selected")
            return

        # Get the comment
        comment: str = self.ui.lineEditMeasurementComment.text().strip()

        # Iterate over each column in the table
        for column in range(table.columnCount()):
            try:
                # Get measurements and formula for the column
                measurements, formula = \
                    self.measurement_module.calculate_formula(column)
            except ValueError as e:
                self.messagebox.err(f"Column {column + 1}: {str(e)}")
                return

            # Fetch the tensiometer ID for the column
            current_column: QTableWidgetItem | None = table.horizontalHeaderItem(column)
            if current_column is None:
                self.messagebox.err(f"Column {column + 1}: No current column")
                return

            header_item: QTableWidgetItem | None = table.horizontalHeaderItem(column)
            if header_item is None:
                self.messagebox.err(f"Column {column + 1}: No header item")
                return

            tensiometer_id = header_item.data(Qt.ItemDataRole.UserRole)
            if tensiometer_id is None:
                self.messagebox.err(
                    f"Column {column + 1}: No tensiometer ID "
                    f"found in the header {header_item}")
                return

            # Extract tension values in the correct order
            tension_values: list[float] = [value for _, value in measurements]

            # Prepare query parameters
            params = (
                spoke_id,
                tensiometer_id,
                *tension_values,
                formula,
                comment,
            )

            # Execute the query
            try:
                db.execute_query(query=SQLQueries.ADD_MEASUREMENT, params=params)
            except Exception as ex:
                self.messagebox.err(f"Failed to save measurement for "
                                    f"column {column + 1}: {str(ex)}")
                return

        # Notify the user
        self.messagebox.ok("Measurements saved successfully")
        for row in range(table.rowCount()):
            for col in range(table.columnCount()):
                item: QTableWidgetItem | None = table.item(row, col)
                if item:
                    item.setText("")
        self.spoke_module.load_spoke_measurements()

    def setup_tensioning_table(self, is_left: bool) -> None:
        """
        Set up tableViewTensionsLeft or tableViewTensionsRight
        based on spoke amount and target tension.
        Populate the table manually for QTableWidget.
        """
        # Select the appropriate UI elements
        if is_left:
            line_edit_spoke_amount: QLineEdit = self.ui.lineEditSpokeAmountLeft
            view: CustomTableWidget = self.ui.tableViewTensioningLeft
        else:
            line_edit_spoke_amount: QLineEdit = self.ui.lineEditSpokeAmountRight
            view: CustomTableWidget = self.ui.tableViewTensioningRight

        # Get spoke amount and target tension
        try:
            spoke_amount = int(line_edit_spoke_amount.text())
        except ValueError:
            spoke_amount = 0

        if is_left:
            self.spoke_tensions_left = [(0.0, 0.0)] * spoke_amount
        else:
            self.spoke_tensions_right = [(0.0, 0.0)] * spoke_amount
        # Define headers
        headers: list[str] = ["mm", self.unit.value]

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

    def next_cell_tensioning_callback_left(self, no_delay: bool = False) -> None:
        self.next_cell_tensioning_callback(True)

    def next_cell_tensioning_callback_right(self, no_delay: bool = False) -> None:
        self.next_cell_tensioning_callback(False)

    def next_cell_tensioning_callback(self, is_left: bool) -> None:
        this_view: CustomTableWidget
        other_view: CustomTableWidget
        if is_left:
            this_view = self.ui.tableViewTensioningLeft
            other_view = self.ui.tableViewTensioningRight
        else:
            this_view = self.ui.tableViewTensioningRight
            other_view = self.ui.tableViewTensioningLeft

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

    def previous_cell_tensioning_callback_left(self) -> None:
        self.previous_cell_tensioning_callback(is_left=True)

    def previous_cell_tensioning_callback_right(self) -> None:
        self.previous_cell_tensioning_callback(is_left=False)

    def previous_cell_tensioning_callback(self, is_left: bool) -> None:
        if is_left:
            print("Previous cell left")
        else:
            print("Previous cell right")

    def on_tensioning_cell_changed(
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
        view: CustomTableWidget = (self.ui.tableViewTensioningLeft
                                   if is_left
                                   else self.ui.tableViewTensioningRight)
        item: QTableWidgetItem | None = view.item(row, column)
        if item is None:
            return
        value: str = item.text()
        header: str | None = view.get_row_header_text(row)
        if header is None:
            return

        spoke_no: int = int(header)
        if value == "":
            return

        print(f"Spoke {spoke_no} {value}")

    def on_tensioning_cell_changing(
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
        print(value)


def main() -> None:
    """
    Entry point for the Spokeduino Mothership application.

    Initializes the QApplication and the main application window.
    """
    app = QApplication(sys.argv)
    window = Spokeduino()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
