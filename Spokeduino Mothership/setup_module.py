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
from ui import Ui_mainWindow


class SetupModule:

    def __init__(self,
                 main_window: QMainWindow,
                 ui: Ui_mainWindow,
                 current_path: str,
                 db: DatabaseModule) -> None:
        self.ui: Ui_mainWindow = ui
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
            query=SQLQueries.GET_SETTINGS, params=None)
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

        # Load Spokeduino enabled
        spokeduino_enabled: str = settings_dict.get("spokeduino_enabled", "0")
        self.ui.checkBoxSpokeduinoEnabled.setChecked(spokeduino_enabled == "1")

        # Load Tensiometer selection
        tensiometer_id: str | None = settings_dict.get("tensiometer_id")
        if tensiometer_id:
            index = self.ui.comboBoxTensiometer.findData(int(tensiometer_id))
            if index != -1:
                self.ui.comboBoxTensiometer.setCurrentIndex(index)

        # Load measurement units
        match settings_dict.get("unit", "Newton"):
            case "Newton":
                self.ui.radioButtonNewton.setChecked(True)
            case "kgF":
                self.ui.radioButtonKgF.setChecked(True)
            case "lbF":
                self.ui.radioButtonLbF.setChecked(True)

        # Load measurement type
        measurement_custom: str = settings_dict.get(
            "measaurement_custom", "0")
        self.ui.radioButtonMeasurementDefault.setChecked(
            measurement_custom == "0")
        self.ui.radioButtonMeasurementCustom.setChecked(
            measurement_custom == "1")
        self.ui.pushButtonMultipleTensiometers.setEnabled(
            self.ui.radioButtonMeasurementDefault.isChecked())

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
        match measurement_type:
            case "side_by_side":
                self.ui.radioButtonSideBySide.setChecked(True)
            case "left_right":
                self.ui.radioButtonLeftRight.setChecked(True)
            case "right_left":
                self.ui.radioButtonRightLeft.setChecked(True)

        # Load fit
        fit_type: str = settings_dict.get(
            "fit", "Quadratic")
        match fit_type:
            case "Quadratic":
                self.ui.radioButtonFitQuadratic.setChecked(True)
            case "Cubic":
                self.ui.radioButtonFitCubic.setChecked(True)
            case "Quartic":
                self.ui.radioButtonFitQuartic.setChecked(True)
            case "Spline":
                self.ui.radioButtonFitSpline.setChecked(True)
            case "Exponential":
                self.ui.radioButtonFitExponential.setChecked(True)
            case "Logarithmic":
                self.ui.radioButtonFitLogarithmic.setChecked(True)
            case "Power law":
                self.ui.radioButtonFitPowerLaw.setChecked(True)
            case _:
                self.ui.radioButtonFitLinear.setChecked(True)
