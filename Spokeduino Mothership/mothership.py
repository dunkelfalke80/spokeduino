import logging
import os
import sys
from typing import cast, Any
from PySide6.QtCore import Qt
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import QTimer
from PySide6.QtGui import QStandardItemModel
from PySide6.QtGui import QStandardItem
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QTableView
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QHeaderView
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtWidgets import QTableWidgetItem
from mothership_ui import Ui_mainWindow
from sql_queries import SQLQueries
from table_helpers import SpokeTableModel
from table_helpers import FloatValidatorDelegate
from database_module import DatabaseModule
from setup_module import SetupModule
from spoke_module import SpokeModule
from measurement_module import MeasurementModule
from unit_converter import UnitConverter

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
        schema_file = os.path.join(self.current_path, "sql", "init_schema.sql")
        data_file = os.path.join(self.current_path, "sql", "default_data.sql")
        self.db = DatabaseModule(self.db_path)
        self.db.initialize_database(schema_file, data_file)

        # For vacuuming on exit
        self.db_changed: bool = False

        # Reducing verbosity
        self.__rm_stretch: QHeaderView.ResizeMode = \
            QHeaderView.ResizeMode.Stretch
        self.__rm_shrink: QHeaderView.ResizeMode =\
            QHeaderView.ResizeMode.ResizeToContents
        self.__select_rows: QAbstractItemView.SelectionBehavior = \
            QAbstractItemView.SelectionBehavior.SelectRows
        self.__select_single: QAbstractItemView.SelectionMode = \
            QAbstractItemView.SelectionMode.SingleSelection

        self.multi_tensiometer_enabled: bool = False
        self.left_spoke_formula: str = ""
        self.right_spoke_formula: str = ""

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
        self.unit_converter = UnitConverter(self.ui)
        self.setup_module.setup_language()
        self.setup_module.populate_language_combobox()
        self.setup_module.load_available_com_ports()
        self.setup_module.load_tensiometers()
        self.setup_signals_and_slots()
        self.setup_module.load_settings()
        self.current_spokes: list[tuple[int, list[str]]] = []
        self.spoke_module.load_manufacturers()
        self.setup_table_widget_measurements()
        # Ugly hack
        QTimer.singleShot(
            msec=100,
            functor=self.spoke_module.align_filters_with_table)

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

        # Manufacturer-related buttons
        self.ui.lineEditNewManufacturer.textChanged.connect(
            self.toggle_new_manufacturer_button)
        self.ui.lineEditNewManufacturer2.textChanged.connect(
            self.toggle_new_manufacturer_button)
        self.ui.pushButtonNewManufacturer.clicked.connect(
            self.create_new_manufacturer)
        self.ui.pushButtonNewManufacturer2.clicked.connect(
            self.create_new_manufacturer)

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
            lambda: self.spoke_module.sync_spoke_selection(
                self.ui.comboBoxSpoke))
        self.ui.comboBoxSpoke2.currentIndexChanged.connect(
            lambda: self.spoke_module.sync_spoke_selection(
                self.ui.comboBoxSpoke2))
        self.ui.comboBoxSpoke.currentIndexChanged.connect(
            lambda: self.spoke_module.sync_spoke_selection(
                self.ui.comboBoxSpoke))
        self.ui.comboBoxSpoke2.currentIndexChanged.connect(
            lambda: self.spoke_module.sync_spoke_selection(
                self.ui.comboBoxSpoke2))
        self.ui.tableViewSpokesDatabase.clicked.connect(
            self.spoke_module.select_spoke_from_table)

        # Filters
        self.ui.tabWidget.currentChanged.connect(
        QTimer.singleShot(
            msec=100,
            functor=self.spoke_module.align_filters_with_table))
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
            self.load_measurements_for_selected_spoke)
        self.ui.lineEditNewTensiometer.textChanged.connect(
            self.toggle_new_tensiometer_button)
        self.ui.pushButtonNewTensiometer.clicked.connect(
            self.create_new_tensiometer)
        self.ui.pushButtonMultipleTensiometers.clicked.connect(
            self.toggle_multi_tensiometer_mode)
        self.ui.pushButtonMultipleTensiometers.setCheckable(True)
        self.ui.comboBoxTensiometer.currentIndexChanged.connect(
            self.setup_table_widget_measurements)

        # Measurement-related signals
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
            self.measurement_module.calculate_formula)
        self.ui.pushButtonMeasureSpoke.clicked.connect(
            self.setup_table_widget_measurements)
        self.ui.pushButtonPreviousMeasurement.clicked.connect(
            self.measurement_module.move_to_previous_cell)
        self.ui.pushButtonNextMeasurement.clicked.connect(
            self.measurement_module.move_to_next_cell)

        # Use spokes
        self.ui.pushButtonUseLeft.clicked.connect(
            lambda: self.use_spoke(True))
        self.ui.pushButtonUseRight.clicked.connect(
            lambda: self.use_spoke(False))

        # Language selection
        self.ui.comboBoxSelectLanguage.currentTextChanged.connect(
            lambda language: self.setup_module.save_setting("language", language))
        self.ui.comboBoxSelectLanguage.currentTextChanged.connect(
            lambda language: self.setup_module.change_language(language.lower()))

        # Spokeduino port selection
        self.ui.comboBoxSpokeduinoPort.currentTextChanged.connect(
            lambda port: self.setup_module.save_setting("spokeduino_port", port))

        # Tensiometer selection
        self.ui.comboBoxTensiometer.currentIndexChanged.connect(
            lambda index: self.setup_module.save_setting(
                "tensiometer_id",
                str(self.ui.comboBoxTensiometer.itemData(index))))

        # Measurement units
        self.ui.radioButtonNewton.toggled.connect(
            lambda checked:
                self.setup_module.save_setting("unit", "Newton") if checked else None)
        self.ui.radioButtonNewton.toggled.connect(
            self.setup_table_widget_measurements)
        self.ui.radioButtonKgF.toggled.connect(
            lambda checked:
                self.setup_module.save_setting("unit", "kgF") if checked else None)
        self.ui.radioButtonKgF.toggled.connect(
            self.setup_table_widget_measurements)
        self.ui.radioButtonLbF.toggled.connect(
            lambda checked:
                self.setup_module.save_setting("unit", "lbF") if checked else None)
        self.ui.radioButtonLbF.toggled.connect(
            self.setup_table_widget_measurements)

        # Directional settings
        self.ui.radioButtonMeasurementDown.toggled.connect(
            lambda checked:
                self.setup_module.save_setting(
                    "spoke_direction",
                    "down") if checked else None)
        self.ui.radioButtonMeasurementDown.toggled.connect(
            self.setup_table_widget_measurements)
        self.ui.radioButtonMeasurementUp.toggled.connect(
            lambda checked:
                self.setup_module.save_setting(
                    "spoke_direction",
                    "up") if checked else None)
        self.ui.radioButtonMeasurementDown.toggled.connect(
            self.setup_table_widget_measurements)
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
            lambda: self.unit_converter.convert_units_realtime("newton"))
        self.ui.lineEditConverterKgF.textChanged.connect(
            lambda: self.unit_converter.convert_units_realtime("kgf"))
        self.ui.lineEditConverterLbF.textChanged.connect(
            lambda: self.unit_converter.convert_units_realtime("lbf"))

        # Table sorting
        header: QHeaderView = \
            self.ui.tableViewSpokesDatabase.horizontalHeader()
        header.sectionClicked.connect(self.spoke_module.sort_by_column)

    def resizeEvent(self, event) -> None:
        """
        Handle window resize event for the main Window.
        Realigns filter fields with the table headers.
        """
        super().resizeEvent(event)
        self.spoke_module.align_filters_with_table()

    def closeEvent(self, event) -> None:
        """
        Handle the close event for the main window.
        Run VACUUM if the database has been modified.
        """
        if self.db_changed:
            self.db.vacuum()
        event.accept()

    def load_measurements_for_selected_spoke(self) -> None:
        """
        Load all measurements for the selected spoke and tensiometer
        and populate tableViewMeasurements.
        """
        spoke_id: int | None = self.ui.comboBoxSpoke.currentData()
        tensiometer_id: int | None = self.ui.comboBoxTensiometer.currentData()
        view: QTableView = self.ui.tableViewMeasurements

        if spoke_id is None or tensiometer_id is None:
            view.setModel(None)
            return
        spoke_id = int(spoke_id)
        tensiometer_id = int(tensiometer_id)

        measurements: list[Any] = self.db.execute_select(
            query=SQLQueries.GET_MEASUREMENTS,
            params=(spoke_id, tensiometer_id))
        if not measurements:
            return

        headers: list[str] = [
            "300N", "400N", "500N", "600N", "700N", "800N", "900N",
            "1000N", "1100N", "1200N", "1300N", "1400N", "1500N"
        ]

        # Convert measurements to list[tuple[int, list[str]]]
        data: list[tuple[Any, list[str]]] = [
            (measurement[0],
             list(map(str, measurement[1:-1])))
             for measurement in measurements]

        model = SpokeTableModel(data, headers)
        view.setModel(model)

        # Configure table behavior
        view.setSelectionBehavior(self.__select_rows)
        view.setSelectionMode(self.__select_single)

        # Set column headers
        view.horizontalHeader().\
            setSectionResizeMode(
            self.__rm_shrink
        )
        view.horizontalHeader().\
            setStretchLastSection(True)

    def delete_measurement(self) -> None:
        """
        Delete the currently selected measurement from the measurements table.
        """
        view: QTableView = self.ui.tableViewMeasurements
        selected_index: QModelIndex = view.currentIndex()
        if not selected_index.isValid():
            return

        model: SpokeTableModel = cast(SpokeTableModel, view.model())
        measurement_id: int = int(model.index(
            selected_index.row(),
            model.columnCount() - 1
        ).data())

        _ = self.db.execute_query(
            query=SQLQueries.DELETE_MEASUREMENT,
            params=(measurement_id,),
        )
        view.clearSelection()
        self.load_measurements_for_selected_spoke()

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
        is_measurement_filled = bool(
            self.ui.lineEditNewManufacturer.text())
        is_database_filled = bool(
            self.ui.lineEditNewManufacturer2.text())

        self.ui.pushButtonNewManufacturer.setEnabled(
            is_database_filled)
        self.ui.pushButtonNewManufacturer2.setEnabled(
            is_measurement_filled
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

            # Connect itemChanged signal for multi-tensiometer mode
            model.itemChanged.connect(
                self.setup_table_widget_measurements)

            # Disable manual typing
            self.ui.comboBoxTensiometer.setEditable(False)

        else:
            # Disable multi-selection mode
            self.multi_tensiometer_enabled = False
            self.ui.pushButtonMultipleTensiometers.setChecked(False)

            # Disconnect itemChanged signal to avoid unnecessary updates
            model = self.ui.comboBoxTensiometer.model()
            if isinstance(model, QStandardItemModel):
                model.itemChanged.disconnect(
                    self.setup_table_widget_measurements)

            # Restore single-selection mode
            self.ui.comboBoxTensiometer.clear()
            self.setup_module.load_tensiometers()

            # Restore the original tensiometer selection
            selected_tensiometers = self.get_selected_tensiometers()
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
        and save the formula for the spoke.
        """
        spoke_id = self.ui.comboBoxSpoke.currentData()
        if not spoke_id:
            return

        # Fetch spoke details and formula from the database
        spoke: list[Any] = self.db.execute_select(
            SQLQueries.GET_SPOKES_BY_ID,
            params=(spoke_id,)
        )

        tensiometer_id: int | None = self.ui.comboBoxTensiometer.currentData()
        if tensiometer_id is None:
            return
        tensiometer_id = int(tensiometer_id)

        # measurements: list[Any] = self.__db.execute_select(
        #    query=SQLQueries.GET_MEASUREMENTS,
        #    params=(spoke_id, tensiometer_id))
        # if not measurements:
        #    return

        # Extract and format details
        _, name, _, gauge, _, dimensions, comment, *_ = spoke[0]

        spoke_details = (
            f"Name: {name}\n"
            f"Gauge: {gauge}\n"
            f"Dimensions: {dimensions}\n"
            f"Comment: {comment}"
        )

        if left:
            self.ui.plainTextEditSelectedSpokeLeft.setPlainText(spoke_details)
            # self.left_spoke_formula = formula
        else:
            self.ui.plainTextEditSelectedSpokeRight.setPlainText(spoke_details)
            # self.right_spoke_formula = formula

    def get_selected_tensiometers(self) -> list[tuple[int, str]]:
        """
        Retrieve the IDs and names of selected tensiometers based on the mode.
        :return: List of tuples with (ID, Name) for selected tensiometers.
        """
        model = self.ui.comboBoxTensiometer.model()
        selected_tensiometers = []

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
                print("Model is not a QStandardItemModel; cannot retrieve selected items.")
        else:
            # Single-tensiometer mode: return the currently selected one
            current_index = self.ui.comboBoxTensiometer.currentIndex()
            if current_index != -1:
                tensiometer_id = self.ui.comboBoxTensiometer.itemData(current_index)
                tensiometer_name = self.ui.comboBoxTensiometer.currentText()
                selected_tensiometers.append((tensiometer_id, tensiometer_name))

        return selected_tensiometers

    def setup_table_widget_measurements(self) -> None:
        """
        Set up the tableWidgetMeasurements with
        editable fields for tension values
        and selected tensiometers.
        """
        # Clear all cells, rows, and columns
        self.ui.tableWidgetMeasurements.clearContents()
        self.ui.tableWidgetMeasurements.setRowCount(0)
        self.ui.tableWidgetMeasurements.setColumnCount(0)

        # Handle the measurement direction
        if self.ui.radioButtonMeasurementDown.isChecked():
            tensions_newton = list(range(1600, 200, -100))
        else:
            tensions_newton = list(range(300, 1700, 100))

        # Handle the measurement units
        unit: str = "Newton"
        if self.ui.radioButtonKgF.isChecked():
            unit = "kgF"
        elif self.ui.radioButtonLbF.isChecked():
            unit = "lbF"
        tensions_converted: list[float] = [
            self.unit_converter.convert_units(value, "newton")[{
                "Newton": 0,
                "kgF": 1,
                "lbF": 2}[unit]]
            for value in tensions_newton
        ]

        # Populate row headers with converted force values
        self.ui.tableWidgetMeasurements.setRowCount(len(tensions_converted))
        if unit == "Newton":
            self.ui.tableWidgetMeasurements.setVerticalHeaderLabels(
                [f"{value} {unit}" for value in tensions_converted]
            )
        else:
            self.ui.tableWidgetMeasurements.setVerticalHeaderLabels(
                [f"{value:.1f} {unit}" for value in tensions_converted]
            )

        # Get selected tensiometers and populate column headers
        tensiometers: list[tuple[int, str]] = self.get_selected_tensiometers()
        self.ui.tableWidgetMeasurements.setColumnCount(len(tensiometers))
        self.ui.tableWidgetMeasurements.setHorizontalHeaderLabels(
            [tensiometer[1] for tensiometer in tensiometers]
        )

        delegate = FloatValidatorDelegate(self.ui.tableWidgetMeasurements)
        self.ui.tableWidgetMeasurements.setItemDelegate(delegate)

        # Make all cells editable
        for row in range(len(tensions_converted)):
            for col in range(len(tensiometers)):
                item = QTableWidgetItem()
                item.setFlags(Qt.ItemFlag.ItemIsEditable |
                              Qt.ItemFlag.ItemIsEnabled)
                self.ui.tableWidgetMeasurements.setItem(row, col, item)

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
