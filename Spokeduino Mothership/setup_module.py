import logging
import os
import serial
import serial.tools.list_ports
from typing import Any
from serial.tools.list_ports_common import ListPortInfo
from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QTranslator
from PySide6.QtWidgets import QMainWindow
from database_module import DatabaseModule
from sql_queries import SQLQueries


class SetupModule:

    def __init__(self,
                 main_window: QMainWindow,
                 ui: Any,
                 current_path: str,
                 db: DatabaseModule) -> None:
        self.ui = ui
        self.main_window: QMainWindow = main_window
        self.current_path: str = current_path
        self.translator = QTranslator()
        self.current_language = "en"
        self.db: DatabaseModule = db

    def setup_language(self) -> None:
        """
        Load initial translations based on current language settings
        """
        i18n_path: str = os.path.join(
            self.current_path, "i18n", f"{self.current_language}.qm")
        if self.translator.load(i18n_path):
            QCoreApplication.installTranslator(self.translator)

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
            self.ui.retranslateUi(self.main_window)
            self.save_setting("language", language_code)
            logging.info(f"Language changed to: {language_code}")
        else:
            logging.error(f"Failed to loopenad translation file: {i18n_path}")

    def load_tensiometers(self) -> None:
        """
        Load all tensiometers from the database
        and populate comboBoxTensiometer.
        """
        tensiometers: list[Any] = self.db.execute_select(
            query=SQLQueries.GET_TENSIOMETERS)
        if not tensiometers:
            return

        self.ui.comboBoxTensiometer.clear()
        for tensiometer in tensiometers:
            self.ui.comboBoxTensiometer.addItem(tensiometer[1], tensiometer[0])

    def load_available_com_ports(self) -> None:
        """
        Detect available COM ports and populate comboBoxSpokeduinoPort.
        """
        self.ui.comboBoxSpokeduinoPort.clear()
        ports: list[ListPortInfo] = serial.tools.list_ports.comports()
        for port in ports:
            self.ui.comboBoxSpokeduinoPort.addItem(port.device)

        # Load settings for selected port
        spokeduino_port: list[str] = self.db.execute_select(
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
        self.db.execute_query(
            query=SQLQueries.UPSERT_SETTING,
            params=(key, value))

    def load_settings(self) -> None:
        """
        Load settings from the database and update the UI accordingly.
        """
        settings: list[Any] = self.db.execute_select(
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