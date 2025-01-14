import threading
import serial
import time
from enum import Enum
from typing import Any
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidgetItem
from database_module import DatabaseModule
from setup_module import SetupModule
from messagebox_module import MessageboxModule
from sql_queries import SQLQueries


class SpokeduinoState(Enum):
    WAITING  = 1
    MEASURING = 2
    TENSIONING = 3


class SpokeduinoModule:
    def __init__(
            self,
            ui: Any,
            db: DatabaseModule,
            setup_module: SetupModule,
            messagebox: MessageboxModule) -> None:
        """
        Initialize the Spokeduino communication module.
        :param ui: The main UI object for accessing GUI elements.
        :param db: Database module for interacting
        with the application database.
        :param setup_module: Module for managing application setup tasks.
        :param messagebox: MessageBox module
        for displaying error/info messages.
        """
        self.ui = ui
        self.db: DatabaseModule = db
        self.setup_module: SetupModule = setup_module
        self.messagebox: MessageboxModule = messagebox
        self.spokeduino_state: SpokeduinoState = SpokeduinoState.WAITING
        self.waiting_event = threading.Event()
        self.th_spokeduino = None
        self.serial_port = serial.Serial()
        self.first_start: bool = True

    def restart_spokeduino_port(self) -> None:
        """
        Restart the Spokeduino serial port based on the settings.
        """
        try:
            if self.get_spokeduino_enabled():
                self.close_serial_port()
                self.update_spokeduino_state(self.first_start, self.first_start)
                if self.first_start:
                    self.first_start = False
                self.reinitialize_serial_port()
                return

            self.update_spokeduino_state(True, False)
            self.reinitialize_serial_port()
        except Exception as ex:
            print(f"Error restarting Spokeduino port: {ex}")

    def set_state(self, state: SpokeduinoState) -> None:
        """
        Update the Spokeduino state and control the waiting_event.
        """
        self.spokeduino_state = state
        print(f"State machine switched to {self.spokeduino_state}")

        if state == SpokeduinoState.WAITING:
            self.waiting_event.clear()  # Block the thread
        else:
            self.waiting_event.set()  # Allow the thread to proceed

    def get_spokeduino_enabled(self) -> bool:
        """
        Fetch the current Spokeduino enabled setting from the database.
        If not set, initialize it to disabled.
        """
        # Fetch the current spokeduino enabled setting
        setting: list[Any] = self.db.execute_select(
            query=SQLQueries.GET_SINGLE_SETTING,
            params=("spokeduino_enabled",)
        )
        if not setting:
            self.setup_module.save_setting("spokeduino_enabled", "0")
            return False
        return setting[0][0] == "1"

    def update_spokeduino_state(self,
                                current_state: bool,
                                force: bool) -> bool:
        """
        Update the Spokeduino state if it has changed.
        Returns the new state.
        """
        new_state = self.ui.checkBoxSpokeduinoEnabled.isChecked()
        if force or current_state != new_state:
                self.setup_module.save_setting(
                    key="spokeduino_enabled",
                    value="1" if new_state
                    else "0"
                )
        return new_state

    def reinitialize_serial_port(self) -> None:
        """
        Reinitialize the serial port and start the handler thread.
        """
        if self.serial_port.is_open:
            self.close_serial_port()

        self.serial_port.baudrate = 9600
        self.serial_port.port = self.ui.comboBoxSpokeduinoPort.currentText()

        try:
            self.serial_port.open()
            self.serial_port.flush()
            self.start_spokeduino_thread()
        except Exception as ex:
            raise RuntimeError(f"Unable to open serial port: {ex}")

    def close_serial_port(self) -> None:
        """
        Close the serial port and stop the handler thread if running.
        """
        try:
            self.serial_port.close()
            self.waiting_event.clear()
            if self.th_spokeduino and self.th_spokeduino.is_alive():
                self.th_spokeduino.join()
        except Exception as ex:
            raise RuntimeError(f"Unable to close serial port: {ex}")

    def start_spokeduino_thread(self) -> None:
        """
        Start the Spokeduino handler thread.
        """
        self.th_spokeduino = threading.Thread(
            target=self.spokeduino_thread, daemon=True
        )
        self.th_spokeduino.start()

    def spokeduino_thread(self) -> None:
        """
        Thread for handling Spokeduino serial communication.
        """
        if not self.serial_port:
            return

        return

        gauge_handlers = {
            0: self.process_tension_gauge,
            1: self.process_lateral_gauge,
            2: self.process_radial_gauge,
            6: self.process_pedal,
        }

        while self.serial_port.is_open:
            self.waiting_event.wait()

            try:
                if not self.serial_port.in_waiting:
                    time.sleep(0.01)
                    continue

                data: str = self.serial_port.readline().decode("ascii").strip()
                if data[1] != ":":
                    continue
                gauge_no: int = int(data[0])
                val: float = float(data[2:])
                handler = gauge_handlers.get(gauge_no)
                if handler:
                    handler(val)

            except serial.SerialException as ex:
                print(f"Serial exception: {ex}")
                break
            except UnicodeDecodeError as ex:
                print(f"Data decode error: {ex}")
                continue

    def process_tension_gauge(self, data: float) -> None:
        """
        Process serial data for the tension gauge.
        """
        match self.spokeduino_state:
            case SpokeduinoState.MEASURING:
                try:
                    table = self.ui.tableWidgetMeasurements
                    item = QTableWidgetItem(str(data))
                    item.setFlags(Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled)
                    table.setItem(table.currentRow(), table.currentColumn(), item)
                except ValueError:
                    print(f"Invalid measurement data: {data}")
            case SpokeduinoState.TENSIONING:
                print("TBD")

    def process_lateral_gauge(self, data: float) -> None:
        """
        Process serial data for the tension gauge.
        """
        match self.spokeduino_state:
            case SpokeduinoState.MEASURING:
                print("TBD")
            case SpokeduinoState.TENSIONING:
                print("TBD")

    def process_radial_gauge(self, data: float) -> None:
        """
        Process serial data for the tension gauge.
        """
        match self.spokeduino_state:
            case SpokeduinoState.MEASURING:
                print("TBD")
            case SpokeduinoState.TENSIONING:
                print("TBD")

    def process_pedal(self, data: int) -> None:
        """
        Process serial data for the tension gauge.
        """
        match self.spokeduino_state:
            case SpokeduinoState.MEASURING:
                print("TBD")
            case SpokeduinoState.TENSIONING:
                print("TBD")