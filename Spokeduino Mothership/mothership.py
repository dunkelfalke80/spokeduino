import logging
import os
import serial
import serial.tools.list_ports
import sys
from serial.tools.list_ports_common import ListPortInfo
from database_manager import DatabaseManager
from sql_queries import SQLQueries
from typing import cast, Any, Tuple
from table_model import SpokeduinoTableModel
from PySide6.QtCore import Qt
from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import QTimer
from PySide6.QtCore import QTranslator
from PySide6.QtGui import QStandardItemModel
from PySide6.QtGui import QStandardItem
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QTableView
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QHeaderView
from PySide6.QtWidgets import QAbstractItemView
from mothership_ui import Ui_mainWindow


class SpokeduinoApp(QMainWindow):
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
        self.__db = DatabaseManager(self.db_path)
        self.__db.initialize_database(schema_file, data_file)

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

        self.translator = QTranslator()
        self.current_language = "en"
        self.setup_ui()
        self.setup_language()
        self.populate_language_combobox()
        self.load_available_com_ports()
        self.load_tensiometers()
        self.setup_signals_and_slots()
        self.load_settings()
        self.current_spokes: list[list[str]] = []
        self.load_manufacturers()

    def setup_ui(self):
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.align_filters_with_table()
        # Ugly hack
        QTimer.singleShot(100, self.align_filters_with_table)

    def setup_signals_and_slots(self) -> None:
        """
        Connect UI elements to their respective event handlers for both tabs.
        """
        # Create and Edit Spoke Buttons
        self.ui.pushButtonCreateSpoke.clicked.connect(self.create_new_spoke)
        self.ui.pushButtonCreateSpoke2.clicked.connect(
            self.create_new_spoke)
        self.ui.pushButtonEditSpoke.clicked.connect(self.modify_spoke)
        self.ui.pushButtonDeleteSpoke.clicked.connect(self.delete_spoke)

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
            self.sync_spoke_selection)
        self.ui.comboBoxSpoke2.currentIndexChanged.connect(
            self.sync_spoke_selection)
        self.ui.comboBoxSpoke.currentIndexChanged.connect(
            self.update_spoke_details)
        self.ui.comboBoxSpoke2.currentIndexChanged.connect(
            self.update_spoke_details)
        self.ui.comboBoxSpoke.currentIndexChanged.connect(
            self.select_spoke_row)
        self.ui.comboBoxSpoke2.currentIndexChanged.connect(
            self.select_spoke_row)
        self.ui.tableViewSpokesDatabase.clicked.connect(
            self.select_spoke_from_table)

        # Filters
        self.ui.tabWidget.currentChanged.connect(
            lambda: QTimer.singleShot(
                100,
                self.align_filters_with_table))
        self.ui.lineEditFilterName.textChanged.connect(self.filter_table)
        self.ui.comboBoxFilterType.currentTextChanged.connect(
            self.filter_table)
        self.ui.lineEditFilterGauge.textChanged.connect(self.filter_table)
        header = self.ui.tableViewSpokesDatabase.horizontalHeader()
        header.sectionResized.connect(self.align_filters_with_table)
        header.sectionMoved.connect(self.align_filters_with_table)

        # Manufacturer-related buttons and combo boxes
        self.ui.comboBoxManufacturer.\
            currentIndexChanged.connect(
                self.load_spokes_for_selected_manufacturer)
        self.ui.comboBoxManufacturer2.\
            currentIndexChanged.connect(
                self.load_spokes_for_selected_manufacturer)
        self.ui.comboBoxManufacturer2.\
            currentIndexChanged.connect(
                self.sync_manufacturer_selection)
        self.ui.comboBoxManufacturer.\
            currentIndexChanged.connect(
                self.sync_manufacturer_selection)

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

        # Measurement-related signals
        self.ui.pushButtonDeleteMeasurement.clicked.connect(
            self.delete_measurement)
        self.ui.pushButtonAddMeasurement.clicked.connect(
            lambda: self.ui.tabWidget.setCurrentIndex(
                self.ui.tabWidget.indexOf(self.ui.measurementTab)))
        self.ui.tableViewMeasurements.clicked.connect(
            self.select_measurement_row)

        # Use spokes
        self.ui.pushButtonUseLeft.clicked.connect(
            lambda: self.use_spoke(True))
        self.ui.pushButtonUseRight.clicked.connect(
            lambda: self.use_spoke(False))

        # Language selection
        self.ui.comboBoxSelectLanguage.currentTextChanged.connect(
            lambda language: self.save_setting("language", language))
        self.ui.comboBoxSelectLanguage.currentTextChanged.connect(
            lambda language: self.change_language(language.lower()))

        # Spokeduino port selection
        self.ui.comboBoxSpokeduinoPort.currentTextChanged.connect(
            lambda port: self.save_setting("spokeduino_port", port))

        # Tensiometer selection
        self.ui.comboBoxTensiometer.currentIndexChanged.connect(
            lambda index: self.save_setting(
                "tensiometer_id",
                str(self.ui.comboBoxTensiometer.itemData(index))))

        # Measurement units
        self.ui.radioButtonNewton.toggled.connect(
            lambda checked:
                self.save_setting("unit", "Newton") if checked else None)
        self.ui.radioButtonKgF.toggled.connect(
            lambda checked:
                self.save_setting("unit", "kgF") if checked else None)
        self.ui.radioButtonLbF.toggled.connect(
            lambda checked:
                self.save_setting("unit", "lbF") if checked else None)

        # Directional settings
        self.ui.radioButtonMeasurementDown.toggled.connect(
            lambda checked:
                self.save_setting(
                    "spoke_direction",
                    "down") if checked else None)
        self.ui.radioButtonMeasurementUp.toggled.connect(
            lambda checked:
                self.save_setting(
                    "spoke_direction",
                    "up") if checked else None)
        self.ui.radioButtonRotationClockwise.toggled.connect(
            lambda checked:
                self.save_setting(
                    "rotation_direction",
                    "clockwise") if checked else None)
        self.ui.radioButtonRotationAnticlockwise.toggled.connect(
            lambda checked:
                self.save_setting(
                    "rotation_direction",
                    "anticlockwise") if checked else None)
        self.ui.radioButtonSideBySide.toggled.connect(
            lambda checked:
                self.save_setting(
                    "measurement_type",
                    "side_by_side") if checked else None)
        self.ui.radioButtonLeftRight.toggled.connect(
            lambda checked:
                self.save_setting(
                    "measurement_type",
                    "left_right") if checked else None)
        self.ui.radioButtonRightLeft.toggled.connect(
            lambda checked:
                self.save_setting(
                    "measurement_type",
                    "right_left") if checked else None)

        # Unit converter
        self.ui.lineEditConverterNewton.textChanged.connect(
            lambda: self.convert_units_realtime("newton"))
        self.ui.lineEditConverterKgF.textChanged.connect(
            lambda: self.convert_units_realtime("kgf"))
        self.ui.lineEditConverterLbF.textChanged.connect(
            lambda: self.convert_units_realtime("lbf"))

        # Table sorting
        header: QHeaderView = \
            self.ui.tableViewSpokesDatabase.horizontalHeader()
        header.sectionClicked.connect(self.sort_by_column)

    def resizeEvent(self, event) -> None:
        """
        Handle window resize event for the main Window.
        Realigns filter fields with the table headers.
        """
        super().resizeEvent(event)
        self.align_filters_with_table()

    def closeEvent(self, event) -> None:
        """
        Handle the close event for the main window.
        Run VACUUM if the database has been modified.
        """
        if self.db_changed:
            self.__db.vacuum()
        event.accept()

    def setup_language(self) -> None:
        """
        Load initial translations based on current language settings
        """
        i18n_path: str = os.path.join(
            self.current_path, "i18n", f"{self.current_language}.qm")
        if self.translator.load(i18n_path):
            QCoreApplication.installTranslator(self.translator)

    def change_language(self, language_code: str | None = None) -> None:
        """
        Reload translations for new language settings.
        """
        if not language_code:
            language_code = self.ui.comboBoxSelectLanguage.currentData()

        if not language_code:
            logging.error("No language code selected or available.")
            return

        i18n_path: str = os.path.join(
            self.current_path, "i18n", f"{language_code}.qm")
        if self.translator.load(i18n_path):
            QCoreApplication.installTranslator(self.translator)
            self.ui.retranslateUi(self)
            self.save_setting("language", language_code)
            logging.info(f"Language changed to: {language_code}")
        else:
            logging.error(f"Failed to loopenad translation file: {i18n_path}")

    def load_available_com_ports(self) -> None:
        """
        Detect available COM ports and populate comboBoxSpokeduinoPort.
        """
        self.ui.comboBoxSpokeduinoPort.clear()
        ports: list[ListPortInfo] = serial.tools.list_ports.comports()
        for port in ports:
            self.ui.comboBoxSpokeduinoPort.addItem(port.device)

        # Load settings for selected port
        spokeduino_port: list[str] = self.__db.execute_select(
            query=SQLQueries.GET_SINGLE_SETTING,
            params=("spokeduino_port",),)
        if not spokeduino_port:
            return

        index: int = self.ui.comboBoxSpokeduinoPort.findText(
            spokeduino_port[0][0])
        if index != -1:
            self.ui.comboBoxSpokeduinoPort.setCurrentIndex(index)

    def save_setting(self, key: str, value: str) -> None:
        """
        Save a single setting in the database.
        If the setting already exists, update it; otherwise, insert it.
        """
        self.__db.execute_query(
            query=SQLQueries.UPSERT_SETTING,
            params=(key, value))

    def load_settings(self) -> None:
        """
        Load settings from the database and update the UI accordingly.
        """
        settings: list[Any] = self.__db.execute_select(
            query=SQLQueries.GET_SETTINGS)
        settings_dict: dict[str, str] = {
            key: value for key,
            value in settings}

        # Load language selection
        language: str = settings_dict.get("language", "en")
        index: int = self.ui.comboBoxSelectLanguage.findText(language)
        if index != -1:
            self.ui.comboBoxSelectLanguage.setCurrentIndex(index)
            self.change_language(language)

        # Load Spokeduino port
        spokeduino_port: str = settings_dict.get("spokeduino_port", "")
        index = self.ui.comboBoxSpokeduinoPort.findText(spokeduino_port)
        if index != -1:
            self.ui.comboBoxSpokeduinoPort.setCurrentIndex(index)

        # Load Tensiometer selection
        tensiometer_id: str | None = settings_dict.get("tensiometer_id")
        if tensiometer_id:
            index = self.ui.comboBoxTensiometer.findData(int(tensiometer_id))
            if index != -1:
                self.ui.comboBoxTensiometer.setCurrentIndex(index)

        # Load measurement units
        unit: str = settings_dict.get("unit", "Newton")
        if unit == "Newton":
            self.ui.radioButtonNewton.setChecked(True)
        elif unit == "kgF":
            self.ui.radioButtonKgF.setChecked(True)
        elif unit == "lbF":
            self.ui.radioButtonLbF.setChecked(True)

        # Load directional settings
        measurement_direction: str = settings_dict.get(
            "spoke_direction", "down")
        if measurement_direction == "down":
            self.ui.radioButtonMeasurementDown.setChecked(True)
        else:
            self.ui.radioButtonMeasurementUp.setChecked(True)

        rotation_direction: str = settings_dict.get(
            "rotation_direction", "clockwise")
        if rotation_direction == "clockwise":
            self.ui.radioButtonRotationClockwise.setChecked(True)
        else:
            self.ui.radioButtonRotationAnticlockwise.setChecked(True)

        measurement_type: str = settings_dict.get(
            "measurement_type", "side_by_side")
        if measurement_type == "side_by_side":
            self.ui.radioButtonSideBySide.setChecked(True)
        elif measurement_type == "left_right":
            self.ui.radioButtonLeftRight.setChecked(True)
        elif measurement_type == "right_left":
            self.ui.radioButtonRightLeft.setChecked(True)

    def populate_language_combobox(self) -> None:
        """
        Populate the language combobox dynamically
        from the available .qm files.
        """
        self.ui.comboBoxSelectLanguage.clear()
        i18n_path: str = os.path.join(self.current_path, "i18n")
        if not os.path.exists(i18n_path):
            logging.error(f"i18n directory not found at: {i18n_path}")
            return

        for filename in os.listdir(i18n_path):
            if filename.endswith(".qm"):
                language_code: str = os.path.splitext(filename)[0]
                self.ui.comboBoxSelectLanguage.addItem(language_code)

    def update_fields(self, spoke: list[str]) -> None:
        """
        Update the fields and comboboxes on both tabs
        with the provided spoke data.
        If no spoke is provided, clear the fields.
        """
        if spoke:
            self.ui.lineEditName.setText(str(spoke[0]))
            self.ui.lineEditName2.setText(str(spoke[0]))
            self.ui.comboBoxType.setCurrentText(str(spoke[1]))
            self.ui.comboBoxType2.setCurrentText(str(spoke[1]))
            self.ui.lineEditGauge.setText(str(spoke[2]))
            self.ui.lineEditGauge2.setText(str(spoke[2]))
            self.ui.lineEditWeight.setText(str(spoke[3]))
            self.ui.lineEditWeight2.setText(str(spoke[3]))
            self.ui.lineEditDimension.setText(str(spoke[4]))
            self.ui.lineEditDimension2.setText(str(spoke[4]))
            self.ui.lineEditSpokeComment.setText(str(spoke[5]))
            self.ui.lineEditSpokeComment2.setText(str(spoke[5]))
        else:
            self.clear_spoke_details()

    def clear_spoke_details(self) -> None:
        """
        Clear all spoke detail fields on both tabs.
        """
        for widget in [
            self.ui.lineEditName,
            self.ui.lineEditName2,
            self.ui.lineEditGauge,
            self.ui.lineEditGauge2,
            self.ui.lineEditWeight,
            self.ui.lineEditWeight2,
            self.ui.lineEditDimension,
            self.ui.lineEditDimension2,
            self.ui.lineEditSpokeComment,
            self.ui.lineEditSpokeComment2,
        ]:
            widget.clear()

        self.ui.comboBoxType.setCurrentIndex(-1)
        self.ui.comboBoxType2.setCurrentIndex(-1)

    def synchronize_comboboxes(self, combo_box, value) -> None:
        """
        Synchronize the value of combo boxes between the two tabs.
        """
        if combo_box == self.ui.comboBoxSpoke:
            self.ui.comboBoxSpoke2.setCurrentText(value)
        elif combo_box == self.ui.comboBoxSpoke2:
            self.ui.comboBoxSpoke.setCurrentText(value)

    def sync_spoke_selection(self) -> None:
        """
        Synchronize the spoke selection between the Database Tab and
        Measurement Tab while preventing circular calls.
        """
        if self.sender() == self.ui.comboBoxSpoke:
            # Sync comboBoxSpoke2 with comboBoxSpoke
            self.ui.comboBoxSpoke2.blockSignals(True)
            self.ui.comboBoxSpoke2.setCurrentIndex(
                self.ui.comboBoxSpoke.currentIndex()
            )
            self.ui.comboBoxSpoke2.blockSignals(False)
        elif self.sender() == self.ui.comboBoxSpoke2:
            # Sync comboBoxSpoke with comboBoxSpoke2
            self.ui.comboBoxSpoke.blockSignals(True)
            self.ui.comboBoxSpoke.setCurrentIndex(
                self.ui.comboBoxSpoke2.currentIndex()
            )
            self.ui.comboBoxSpoke.blockSignals(False)

        # Update the details for the currently selected spoke
        self.update_spoke_details()

    def sync_manufacturer_selection(self) -> None:
        """
        Synchronize the manufacturer selection between the
        Database Tab and Measurement Tab. Trigger loading
        of spokes for the selected manufacturer.
        """
        combo1: QComboBox = self.ui.comboBoxManufacturer
        combo2: QComboBox = self.ui.comboBoxManufacturer2
        sender: QComboBox = cast(QComboBox, self.sender())
        selected_manufacturer_id: int = sender.currentData()

        if combo1.currentData() != selected_manufacturer_id:
            combo1.blockSignals(True)
            combo1.setCurrentIndex(
                combo1.findData(selected_manufacturer_id)
            )
            combo1.blockSignals(False)

        if combo2.currentData() != selected_manufacturer_id:
            combo2.blockSignals(True)
            combo2.setCurrentIndex(
                combo2.findData(selected_manufacturer_id)
            )
            combo2.blockSignals(False)

        self.load_spokes_for_selected_manufacturer()

    def load_tensiometers(self) -> None:
        """
        Load all tensiometers from the database
        and populate comboBoxTensiometer.
        """
        tensiometers: list[Any] = self.__db.execute_select(
            query=SQLQueries.GET_TENSIOMETERS)
        if not tensiometers:
            return

        self.ui.comboBoxTensiometer.clear()
        for tensiometer in tensiometers:
            self.ui.comboBoxTensiometer.addItem(tensiometer[1], tensiometer[0])

    def load_manufacturers(self) -> None:
        """
        Load all manufacturer names from the database and populate the
        the dropdowns. Automatically loads spokes for the first manufacturer.
        """
        # Load manufacturers
        manufacturers: list[Any] = self.__db.execute_select(
            query=SQLQueries.GET_MANUFACTURERS)
        if not manufacturers:
            return

        self.ui.comboBoxManufacturer.clear()
        self.ui.comboBoxManufacturer2.clear()
        for manufacturer in manufacturers:
            self.ui.comboBoxManufacturer.addItem(
                manufacturer[1], manufacturer[0])
            self.ui.comboBoxManufacturer2.addItem(
                manufacturer[1], manufacturer[0]
            )

        # Load types
        spoke_types: list[Any] = self.__db.execute_select(
            query=SQLQueries.GET_TYPES)
        if not spoke_types:
            return

        self.ui.comboBoxType.clear()
        self.ui.comboBoxType2.clear()
        for spoke_type in spoke_types:
            self.ui.comboBoxType.addItem(
                spoke_type[1], spoke_type[0])
            self.ui.comboBoxType2.addItem(
                spoke_type[1], spoke_type[0])

        # Automatically load spokes for the first manufacturer
        if manufacturers:
            self.ui.comboBoxManufacturer.\
                setCurrentIndex(0)
            self.ui.comboBoxManufacturer2.\
                setCurrentIndex(0)
            self.load_spokes_for_selected_manufacturer()

    def load_spokes_for_selected_manufacturer(self) -> None:
        """
        Load all spokes for the currently selected manufacturer and populate
        the tableViewSpokesDatabase and comboBoxSpoke.
        """
        manufacturer_id: int | None = \
            self.ui.comboBoxManufacturer.currentData()

        if manufacturer_id is None:
            return
        manufacturer_id = int(manufacturer_id)

        spokes: list[Any] = self.__db.execute_select(
            query=SQLQueries.GET_SPOKES_BY_MANUFACTURER,
            params=(manufacturer_id,))
        if not spokes:
            return

        headers: list[str] = [
            "Name",
            "Type",
            "Gauge",
            "Weight",
            "Dimensions",
            "Comment"]

        # Exclude ID
        self.current_spokes = [(spoke[0], list(spoke[1:])) for spoke in spokes]
        model = SpokeduinoTableModel(self.current_spokes, headers)
        view: QTableView = self.ui.tableViewSpokesDatabase
        view.setModel(model)

        # Populate comboBoxSpoke
        self.ui.comboBoxSpoke.clear()
        self.ui.comboBoxSpoke2.clear()
        for spoke in spokes:
            # Name and ID
            self.ui.comboBoxSpoke.addItem(
                spoke[1], spoke[0])
            self.ui.comboBoxSpoke2.addItem(
                spoke[1], spoke[0])

        # Adjust column widths
        resize_mode = view.horizontalHeader().setSectionResizeMode
        resize_mode(0, self.__rm_stretch)  # Name
        resize_mode(1, self.__rm_stretch)  # Type
        resize_mode(2, self.__rm_shrink)   # Gauge
        resize_mode(3, self.__rm_shrink)   # Weight
        resize_mode(4, self.__rm_stretch)  # Dimensions
        resize_mode(5, self.__rm_stretch)  # Comment

        # Configure table behavior
        view.setSelectionBehavior(self.__select_rows)
        view.setSelectionMode(self.__select_single)
        self.populate_filter_type()

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

        measurements: list[Any] = self.__db.execute_select(
            query=SQLQueries.GET_MEASUREMENTS,
            params=(spoke_id, tensiometer_id))
        if not measurements:
            return

        headers: list[str] = [
            "300N", "400N", "500N", "600N", "700N", "800N", "900N",
            "1000N", "1100N", "1200N", "1300N", "1400N", "1500N"
        ]
        model = SpokeduinoTableModel(
            [list(measurement[:-1])
                for measurement in measurements], headers
        )
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

        model: SpokeduinoTableModel = cast(SpokeduinoTableModel, view.model())
        measurement_id: int = int(model.index(
            selected_index.row(),
            model.header_count()).data())

        _ = self.__db.execute_query(
                    query=SQLQueries.DELETE_MEASUREMENT,
                    params=(measurement_id,),
                )
        view.clearSelection()
        self.load_measurements_for_selected_spoke()

    def sort_by_column(self, column: int) -> None:
        """
        Sort the tableViewSpokesDatabase by the specified column.
        """
        self.current_spokes.sort(key=lambda x: x[1][column])
        self.ui.tableViewSpokesDatabase.model().layoutChanged.emit()

    def select_spoke_from_table(self, index: QModelIndex) -> None:
        """
        Select the corresponding spoke in comboBoxSpoke
        when a table row is clicked.
        """
        row = index.row()
        model: SpokeduinoTableModel = cast(
            SpokeduinoTableModel,
            self.ui.tableViewSpokesDatabase.model())
        spoke_id = model.get_id(row)

        if spoke_id is not None:
            combo_index = self.ui.comboBoxSpoke.findData(spoke_id)
            if combo_index != -1:
                self.ui.comboBoxSpoke.setCurrentIndex(combo_index)

    def select_spoke_row(self) -> None:
        """
        Select the corresponding row in tableViewSpokesDatabase
        based on the combobox.
        """
        spoke_id: int | None = self.ui.comboBoxSpoke.currentData()
        if spoke_id is None:
            self.ui.tableViewSpokesDatabase.clearSelection()
            return

        model: SpokeduinoTableModel = cast(
            SpokeduinoTableModel,
            self.ui.tableViewSpokesDatabase.model())

        for row in range(model.rowCount()):
            if model.get_id(row) == spoke_id:
                self.ui.tableViewSpokesDatabase.selectRow(row)
                break

    def update_spoke_details(self) -> None:
        """
        Update the spoke details fields when a spoke is
        selected in comboBoxSpoke.
        """
        sender: QComboBox = cast(QComboBox, self.sender())
        spoke_id: int | None = sender.currentData()

        if spoke_id is None:
            self.clear_spoke_details()
            return
        spoke_id = int(spoke_id)

        spokes: list[Any] = self.__db.execute_select(
            query=SQLQueries.GET_SPOKES_BY_ID,
            params=(spoke_id,))
        if not spokes:
            return

        self.update_fields(spokes[0][1:])

    def unselect_spoke(self) -> None:
        """
        Unselect the row in tableViewSpokesDatabase
        when pushButtonEditSpoke is clicked.
        """
        self.ui.tableViewSpokesDatabase.clearSelection()
        self.clear_spoke_details()

    def clear_spoke_selection(self) -> None:
        """
        Clear the row selection in tableViewSpokesDatabase
        and clear all spoke detail fields.
        """
        self.ui.tableViewSpokesDatabase.clearSelection()
        self.ui.comboBoxSpoke.setCurrentIndex(-1)
        self.clear_spoke_details()

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
            self.ui.comboBoxTensiometer.clear()
            self.ui.pushButtonMultipleTensiometers.setChecked(True)

            # Use a QStandardItemModel to allow checkboxes
            model = QStandardItemModel(self.ui.comboBoxTensiometer)
            for tensiometer in self.__db.execute_select(
                    SQLQueries.GET_TENSIOMETERS):
                item = QStandardItem(tensiometer[1])
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
                item.setData(Qt.Unchecked, Qt.CheckStateRole)
                # Store tensiometer ID
                item.setData(tensiometer[0], Qt.UserRole)
                model.appendRow(item)

            self.ui.comboBoxTensiometer.setModel(model)
            # Disable manual typing
            self.ui.comboBoxTensiometer.setEditable(False)
        else:
            # Disable multi-selection mode
            self.multi_tensiometer_enabled = False
            self.ui.pushButtonMultipleTensiometers.setChecked(False)
            self.selected_tensiometers = []

            # Restore single-selection mode
            self.ui.comboBoxTensiometer.clear()
            self.load_tensiometers()  # Reload from database

            # Restore the original tensiometer
            tensiometer_id: list[str] = self.__db.execute_select(
                query=SQLQueries.GET_SINGLE_SETTING,
                params=("tensiometer_id",),)
            if not tensiometer_id:
                return

            index: int = self.ui.comboBoxTensiometer.findData(
                tensiometer_id[0][0])
            if index != -1:
                self.ui.comboBoxTensiometer.setCurrentIndex(index)

    def get_selected_tensiometers(self) -> list[int]:
        """
        Retrieve the IDs of all tensiometers that are checked in the combobox.
        :return: List of selected tensiometer IDs.
        """
        model = self.ui.comboBoxTensiometer.model()
        selected_ids = []
        for row in range(model.rowCount()):
            item = model.item(row)
            if item.checkState() == Qt.Checked:
                # Retrieve stored ID
                selected_ids.append(item.data(Qt.UserRole))
        return selected_ids

    def create_new_tensiometer(self) -> None:
        """
        Insert a new tensiometer into the tensiometers table.
        """
        tensiometer_name: str = self.ui.lineEditNewTensiometer.text()
        if not tensiometer_name:
            return

        self.ui.lineEditNewTensiometer.clear()
        _ = self.__db.execute_query(
            query=SQLQueries.ADD_TENSIOMETER,
            params=(tensiometer_name,),
        )
        self.load_tensiometers()

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

        new_manufacturer_id: int | None = self.__db.execute_query(
            query=SQLQueries.ADD_MANUFACTURER,
            params=(manufacturer_name,),
        )

        self.ui.lineEditNewManufacturer.clear()
        self.ui.lineEditNewManufacturer2.clear()
        self.load_manufacturers()

        if new_manufacturer_id is None:
            return
        new_manufacturer_id = int(new_manufacturer_id)

        self.ui.comboBoxManufacturer.setCurrentIndex(
            self.ui.comboBoxManufacturer.findData(
                new_manufacturer_id))

    def get_database_spoke_data(
            self, from_database: bool
            ) -> Tuple[int, int, float, str, str, str]:
        """
        DRY helper
        """
        try:
            if from_database:
                return int(self.ui.comboBoxType.currentData()), \
                    int(self.ui.lineEditGauge.text() or 0), \
                    float(self.ui.lineEditWeight.text() or 0.0), \
                    self.ui.lineEditName.text() or "", \
                    self.ui.lineEditDimension.text() or "", \
                    self.ui.lineEditSpokeComment.text() or ""
            else:
                return int(self.ui.comboBoxType2.currentData()), \
                    int(self.ui.lineEditGauge2.text() or 0), \
                    float(self.ui.lineEditWeight2.text() or 0.0), \
                    self.ui.lineEditName2.text() or "", \
                    self.ui.lineEditDimension2.text() or "", \
                    self.ui.lineEditSpokeComment2.text() or ""

        except ValueError as e:
            logging.error(f"Invalid data provided: {e}")
            raise

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
            self.get_database_spoke_data(from_database)

        new_spoke_id: int | None = self.__db.execute_query(
            query=SQLQueries.ADD_SPOKE,
            params=(manufacturer_id, spoke_name,
                    type_id, gauge, weight, dimension, comment),
        )
        if new_spoke_id is None:
            return
        new_spoke_id = int(new_spoke_id)

        self.load_spokes_for_selected_manufacturer()
        self.ui.comboBoxSpoke.setCurrentIndex(
            self.ui.comboBoxSpoke.findData(new_spoke_id)
        )
        self.ui.comboBoxSpoke2.setCurrentIndex(
            self.ui.comboBoxSpoke2.findData(new_spoke_id)
        )

    def modify_spoke(self) -> None:
        """
        Update the selected spoke with new values from the detail fields.
        """
        spoke_id: int | None = self.ui.comboBoxSpoke.currentData()

        if spoke_id is None:
            return
        spoke_id = int(spoke_id)

        type_id, gauge, weight, \
            spoke_name, dimension, comment = \
            self.get_database_spoke_data(True)

        _ = self.__db.execute_query(
            query=SQLQueries.MODIFY_SPOKE,
            params=(spoke_name, type_id, gauge, weight,
                    dimension, comment, spoke_id),
        )
        self.load_spokes_for_selected_manufacturer()

    def delete_spoke(self) -> None:
        """
        Delete the currently selected spoke from the spokes table.
        """
        spoke_id: int | None = self.ui.comboBoxSpoke.currentData()
        if spoke_id is None:
            return
        spoke_id = int(spoke_id)

        _ = self.__db.execute_query(
            query=SQLQueries.DELETE_SPOKE,
            params=(spoke_id,)
        )
        self.load_spokes_for_selected_manufacturer()
        # Clear selection
        self.ui.comboBoxSpoke.setCurrentIndex(-1)
        self.ui.tableViewSpokesDatabase.clearSelection()

    def convert_units(
            self, value: float, source: str) -> Tuple[float, float, float]:
        """
        Convert units
        :param value: The value to be converted.
        :param source: The unit type that triggered the conversion.
        :return the values in newton, kgf and lbf.
        """
        if source == "newton":
            return (value,
                    value * 0.1019716213,
                    value * 0.2248089431)
        elif source == "kgf":
            return (value / 0.1019716213,
                    value,
                    value * 2.2046226218)
        elif source == "lbf":
            return (value / 0.2248089431,
                    value / 2.2046226218,
                    value)
        else:
            return 0.0, 0.0, 0.0

    def convert_units_realtime(self, source: str) -> None:
        """
        Convert units in real time
        :param source: The unit type that triggered the conversion.
        """
        try:
            # Read input values
            if source == "newton":
                value = float(self.ui.lineEditConverterNewton.text() or 0)
                newton, kgf, lbf = self.convert_units(value, source)
                self.ui.lineEditConverterKgF.blockSignals(True)
                self.ui.lineEditConverterLbF.blockSignals(True)

                self.ui.lineEditConverterKgF.setText(f"{kgf:.2f}")
                self.ui.lineEditConverterLbF.setText(f"{lbf:.2f}")

                self.ui.lineEditConverterKgF.blockSignals(False)
                self.ui.lineEditConverterLbF.blockSignals(False)
            elif source == "kgf":
                value = float(self.ui.lineEditConverterKgF.text() or 0)
                newton, kgf, lbf = self.convert_units(value, source)
                self.ui.lineEditConverterNewton.blockSignals(True)
                self.ui.lineEditConverterLbF.blockSignals(True)

                self.ui.lineEditConverterNewton.setText(f"{newton:.2f}")
                self.ui.lineEditConverterLbF.setText(f"{lbf:.2f}")

                self.ui.lineEditConverterNewton.blockSignals(False)
                self.ui.lineEditConverterLbF.blockSignals(False)
            elif source == "lbf":
                value = float(self.ui.lineEditConverterLbF.text() or 0)
                newton, kgf, lbf = self.convert_units(value, source)
                self.ui.lineEditConverterKgF.blockSignals(True)
                self.ui.lineEditConverterNewton.blockSignals(True)

                self.ui.lineEditConverterNewton.setText(f"{newton:.2f}")
                self.ui.lineEditConverterKgF.setText(f"{kgf:.2f}")

                self.ui.lineEditConverterKgF.blockSignals(False)
                self.ui.lineEditConverterNewton.blockSignals(False)
        except ValueError:
            # Clear the other textboxes if the input is invalid
            if source == "newton":
                self.ui.lineEditConverterKgF.clear()
                self.ui.lineEditConverterLbF.clear()
            elif source == "kgf":
                self.ui.lineEditConverterNewton.clear()
                self.ui.lineEditConverterLbF.clear()
            elif source == "lbf":
                self.ui.lineEditConverterNewton.clear()
                self.ui.lineEditConverterKgF.clear()

    def use_spoke(self, left: bool) -> None:
        """
        Write the selected spoke details to plainTextEditSelectedSpoke
        and save the formula for the spoke.
        """
        spoke_id = self.ui.comboBoxSpoke.currentData()
        if not spoke_id:
            return

        # Fetch spoke details and formula from the database
        spoke: list[Any] = self.__db.execute_select(
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

    def align_filters_with_table(self):
        """
        Align filter fields with tableViewSpokesDatabase columns.
        """
        if not self.ui.tableViewSpokesDatabase.isVisible():
            return

        header = self.ui.tableViewSpokesDatabase.horizontalHeader()

        # Get column positions and sizes
        offset_x = self.ui.tableViewSpokesDatabase.geometry().x() + \
            header.sectionPosition(0)
        name_pos = header.sectionPosition(0) + offset_x
        name_width = header.sectionSize(0)
        type_pos = header.sectionPosition(1) + offset_x
        type_width = header.sectionSize(1)
        gauge_pos = header.sectionPosition(2) + offset_x
        gauge_width = header.sectionSize(2)

        # Update filter field positions and sizes
        self.ui.lineEditFilterName.setGeometry(
            name_pos,
            self.ui.lineEditFilterName.y(),
            name_width,
            self.ui.lineEditFilterName.height())
        self.ui.comboBoxFilterType.setGeometry(
            type_pos,
            self.ui.comboBoxFilterType.y(),
            type_width,
            self.ui.comboBoxFilterType.height())
        self.ui.lineEditFilterGauge.setGeometry(
            gauge_pos,
            self.ui.lineEditFilterGauge.y(),
            gauge_width,
            self.ui.lineEditFilterGauge.height())

    def filter_table(self):
        """
        Filter tableViewSpokesDatabase based on filter inputs.
        """
        name_filter = self.ui.lineEditFilterName.text().lower()
        type_filter = self.ui.comboBoxFilterType.currentText().lower()
        gauge_filter = self.ui.lineEditFilterGauge.text().lower()

        # Apply filters to the data
        filtered_data = [
            spoke for spoke in self.current_spokes
            # Match Name
            if (name_filter in spoke[1][0].lower()) and
            # Match Type
            (type_filter in spoke[1][1].lower() if type_filter else True) and
            # Match Gauge
            (gauge_filter in str(spoke[1][2]).lower()
                if gauge_filter else True)
        ]

        # Update the table model with filtered data
        headers = ["Name", "Type", "Gauge", "Weight", "Dimensions", "Comment"]
        model = SpokeduinoTableModel(filtered_data, headers)
        self.ui.tableViewSpokesDatabase.setModel(model)

    def populate_filter_type(self):
        """
        Populate comboBoxFilterType with unique spoke types.
        """
        types = {spoke[1][1] for spoke in self.current_spokes}
        self.ui.comboBoxFilterType.clear()
        self.ui.comboBoxFilterType.addItem("")  # Empty means no filter is set
        self.ui.comboBoxFilterType.addItems(sorted(types))


def main() -> None:
    """
    Entry point for the Spokeduino Mothership application.

    Initializes the QApplication and the main application window.
    """
    app = QApplication(sys.argv)
    window = SpokeduinoApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
