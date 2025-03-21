import threading
import serial
import inspect
from enum import Enum
from typing import Any
from PySide6.QtCore import Qt
from customtablewidget import CustomTableWidget, NumericTableWidgetItem
from database_module import DatabaseModule
from setup_module import SetupModule
from helpers import TextChecker
from sql_queries import SQLQueries
from unit_module import UnitEnum, UnitModule
from ui import Ui_mainWindow


class SpokeduinoState(Enum):
    WAITING = 1
    MEASURING = 2
    TENSIONING = 3


class MeasurementMode(Enum):
    DEFAULT = 0
    EDIT = 1
    CUSTOM = 2


class SpokeduinoModule:
    def __init__(
            self,
            ui: Ui_mainWindow,
            db: DatabaseModule,
            setup_module: SetupModule,
            unit_module: UnitModule) -> None:
        """
        Initialize the Spokeduino communication module.
        :param ui: The main UI object for accessing GUI elements.
        :param db: Database module for interacting
        with the application database.
        :param setup_module: Module for managing application setup tasks.
        :param unit_module: Module for converting units.
        :param measurement_module: Measurement module for checking the mode
        :param messagebox: MessageBox module
        for displaying error/info messages.
        """
        self.__ui: Ui_mainWindow = ui
        self.__db: DatabaseModule = db
        self.__setup: SetupModule = setup_module
        self.__unit_module: UnitModule = unit_module
        self.__evt: threading.Event = threading.Event()
        self.__th_spokeduino: threading.Thread
        self.__serial = serial.Serial()
        self.__first_start: bool = True
        self.__spokeduino_state: SpokeduinoState = SpokeduinoState.WAITING
        self.__mode: MeasurementMode = MeasurementMode.DEFAULT

    def set_mode(self, mode: MeasurementMode) -> None:
        if mode == MeasurementMode.DEFAULT:
            if self.__ui.radioButtonMeasurementCustom.isChecked():
                mode = MeasurementMode.CUSTOM
        self.__mode = mode
        stack = inspect.stack()
        caller_frame = stack[1]
        print(f"This function was called by: {caller_frame.function}")

    def get_mode(self) -> MeasurementMode:
        return self.__mode

    def restart_spokeduino_port(self) -> None:
        """
        Restart the Spokeduino serial port based on the settings.
        """
        try:
            if self.get_spokeduino_enabled():
                self.__evt.set()
                self.close_serial_port()
                self.update_spokeduino_enabled(
                    self.__first_start, self.__first_start)
                if self.__first_start:
                    self.__first_start = False
                self.reinitialize_serial_port()
                return

            self.update_spokeduino_enabled(True, False)
            self.reinitialize_serial_port()
        except Exception as ex:
            print(f"Error restarting Spokeduino port: {ex}")

    def set_state(self, state: SpokeduinoState) -> None:
        """
        Update the Spokeduino state and control the waiting_event.
        """
        self.__spokeduino_state = state
        print(f"State machine switched to {self.get_state()}")

        if state == SpokeduinoState.WAITING:
            self.__evt.clear()  # Block the thread
        else:
            self.__evt.set()  # Allow the thread to proceed

    def get_state(self) -> SpokeduinoState:
        return self.__spokeduino_state

    def get_spokeduino_enabled(self) -> bool:
        """
        Fetch the current Spokeduino enabled setting from the database.
        If not set, initialize it to disabled.
        """
        # Fetch the current spokeduino enabled setting
        setting: list[Any] = self.__db.execute_select(
            query=SQLQueries.GET_SINGLE_SETTING,
            params=("spokeduino_enabled",)
        )
        if not setting:
            self.__setup.save_setting("spokeduino_enabled", "0")
            return False
        return setting[0][0] == "1"

    def update_spokeduino_enabled(self,
                                current_state: bool,
                                force: bool) -> bool:
        """
        Update the Spokeduino state if it has changed.
        Returns the new state.
        """
        new_state: bool = self.__ui.checkBoxSpokeduinoEnabled.isChecked()
        if force or current_state != new_state:
            self.__setup.save_setting(
                    key="spokeduino_enabled",
                    value="1" if new_state
                    else "0"
                )
        return new_state

    def reinitialize_serial_port(self) -> None:
        """
        Reinitialize the serial port and start the handler thread.
        """
        self.close_serial_port()
        self.__serial.baudrate = 115200
        self.__serial.port = self.__ui.comboBoxSpokeduinoPort.currentText()
        self.__serial.timeout = 1

        try:
            self.__serial.open()
            self.__serial.flush()
            self.start_spokeduino_thread()
        except Exception as ex:
            raise RuntimeError(f"Unable to open serial port: {ex}")

    def close_serial_port(self) -> None:
        """
        Close the serial port and stop the handler thread if running.
        """
        if not self.__serial.is_open:
            return
        try:
            self.__serial.close()
            self.__evt.set()
            if self.__th_spokeduino and self.__th_spokeduino.is_alive():
                self.__th_spokeduino.join()
        except Exception as ex:
            raise RuntimeError(f"Unable to close serial port: {ex}")

    def start_spokeduino_thread(self) -> None:
        """
        Start the Spokeduino handler thread.
        """
        self.__th_spokeduino = threading.Thread(
            target=self.spokeduino_thread, daemon=True)
        self.__th_spokeduino.start()

    def spokeduino_thread(self) -> None:
        """
        Thread for handling Spokeduino serial communication
        """
        if not self.__serial:
            return

        gauge_handlers = {
            0: self.process_tension_gauge,
            1: self.process_lateral_gauge,
            2: self.process_radial_gauge,
            6: self.process_pedal,
            9: self.process_scale,
        }

        while self.__serial.is_open:
            self.__evt.wait()

            try:
                data_bytes: bytes = self.__serial.readline()
                if not data_bytes:
                    continue  # timeout

                data_str = data_bytes.decode("ascii", errors="ignore").strip()
                if len(data_str) < 2 or data_str[1] != ":":
                    continue

                gauge_no = int(data_str[0])
                val = float(data_str[2:])
                handler = gauge_handlers.get(gauge_no)
                if handler:
                    handler(val)

            except serial.SerialException as ex:
                if not self.__serial.is_open:
                    break  # serial port was closed elsewhere
                print(f"Serial exception: {ex}")
                break
            except UnicodeDecodeError as ex:
                print(f"Data decode error: {ex}")
                continue
            except AttributeError:
                break  # serial port was closed elsewhere
            except TypeError:
                break  # serial port was closed elsewhere

    def insert_measurement(
            self, data: float, role: float, target: int) -> None:
        if self.get_state() == SpokeduinoState.WAITING:
            print("we are waiting")
            return
        try:
            table: CustomTableWidget = self.__ui.tableWidgetMeasurements
            column: int = table.currentColumn()
            if column != target:
                return
            item = NumericTableWidgetItem(
                TextChecker.check_text(str(data)))
            item.setFlags(
                Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled)
            item.setData(
                Qt.ItemDataRole.UserRole, role)
            table.setItem(
                table.currentRow(), column, item)
        except ValueError:
            print(f"Invalid measurement data: {data}")

    def process_tension_gauge(self, data: float) -> None:
        """
        Process serial data for the tension gauge.
        """

        match self.get_state():
            case SpokeduinoState.MEASURING:
                if self.get_mode() == MeasurementMode.DEFAULT:
                    self.insert_measurement(data, data, 0)
                else:
                    self.insert_measurement(data, data, 1)
            case SpokeduinoState.TENSIONING:
                print("TBD")

    def process_lateral_gauge(self, data: float) -> None:
        """
        Process serial data for the tension gauge.
        """
        match self.get_state():
            case SpokeduinoState.MEASURING:
                print("TBD")
            case SpokeduinoState.TENSIONING:
                print("TBD")

    def process_radial_gauge(self, data: float) -> None:
        """
        Process serial data for the tension gauge.
        """
        match self.get_state():
            case SpokeduinoState.MEASURING:
                print("TBD")
            case SpokeduinoState.TENSIONING:
                print("TBD")

    def process_pedal(self, data: float) -> None:
        """
        Process serial data for the tension gauge.
        """
        match self.get_state():
            case SpokeduinoState.MEASURING:
                self.__ui.pushButtonNextMeasurement.click()
            case SpokeduinoState.TENSIONING:
                print("TBD")

    def process_scale(self, data: float) -> None:
        """
        Process serial data for the tension gauge.
        """
        unit: UnitEnum = self.__unit_module.get_unit()
        if self.get_state() is not SpokeduinoState.MEASURING:
            return
        if self.get_mode() == MeasurementMode.DEFAULT:
            return
        converted_tensions: tuple[float, float, float] = \
            self.__unit_module.convert_units(
                    value=data, source=UnitEnum.KGF)
        tension_converted: float = round({
            UnitEnum.NEWTON: converted_tensions[0],
            UnitEnum.KGF: converted_tensions[1],
            UnitEnum.LBF: converted_tensions[2]}[unit], 2)
        self.insert_measurement(tension_converted, converted_tensions[0], 0)
