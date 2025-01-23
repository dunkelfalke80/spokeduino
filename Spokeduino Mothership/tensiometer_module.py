from typing import Any
from PySide6.QtCore import Qt
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import QAbstractItemModel
from PySide6.QtGui import QStandardItemModel
from PySide6.QtGui import QStandardItem
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QTableWidget
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtWidgets import QHeaderView
from setup_module import SetupModule
from helpers import Messagebox, Generics
from customtablewidget import CustomTableWidget
from sql_queries import SQLQueries
from unit_module import UnitEnum, UnitModule
from database_module import DatabaseModule

class TensiometerModule:

    def __init__(self,
                 main_window: QMainWindow,
                 ui: Any,
                 setup_module: SetupModule,
                 messagebox: Messagebox,
                 db: DatabaseModule) -> None:
        self.ui = ui
        self.main_window: QMainWindow = main_window
        self.setup_module: SetupModule = setup_module
        self.messagebox: Messagebox = messagebox
        self.db: DatabaseModule = db
        self.__multi_tensiometer_enabled: bool = False

    def get_multi_state(self) -> bool:
        return self.__multi_tensiometer_enabled

    def set_multi_state(self, state: bool) -> None:
        self.__multi_tensiometer_enabled = state

    def load_tensiometers(self) -> None:
        """
        Load all tensiometers from the database
        and populate comboBoxTensiometer.
        """
        tensiometers: list[Any] = self.db.execute_select(
            query=SQLQueries.GET_TENSIOMETERS, params=None)
        if not tensiometers:
            return

        self.ui.comboBoxTensiometer.clear()
        for tensiometer in tensiometers:
            self.ui.comboBoxTensiometer.addItem(tensiometer[1], tensiometer[0])

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

        if self.get_multi_state():
            # Ensure model is a QStandardItemModel
            if isinstance(model, QStandardItemModel):
                # Multi-tensiometer mode: return all checked tensiometers
                for row in range(model.rowCount()):
                    item: QStandardItem = model.item(row)  # Safely access item()
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

    def toggle_new_tensiometer_button(self) -> None:
        """
        Enable or disable pushButtonNewTensiometer based on the text in
        lineEditNewTensiometer.
        """
        is_filled = bool(self.ui.lineEditNewTensiometer.text())
        self.ui.pushButtonNewTensiometer.setEnabled(is_filled)

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

            for tensiometer in self.db.execute_select(
                query=SQLQueries.GET_TENSIOMETERS,
                params=None):
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
            self.load_tensiometers()

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
        self.load_tensiometers()

        index: int = self.ui.comboBoxTensiometer.findText(tensiometer_name)
        if index != -1:
            self.ui.comboBoxTensiometer.setCurrentIndex(index)

    def save_tensiometer(self) -> None:
        if self.multi_tensiometer_enabled: # Runtime only
            return

        current_index: int = self.ui.comboBoxTensiometer.currentIndex()
        if current_index != -1:
            tensiometer_id = self.ui.comboBoxTensiometer.itemData(current_index)
            self.setup_module.save_setting(
                key="tensiometer_id",
                value=str(tensiometer_id))
