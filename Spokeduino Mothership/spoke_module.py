from typing import Any, cast
from PySide6.QtCore import QTranslator
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QHeaderView
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QModelIndex
from PySide6.QtWidgets import QTableView
from database_module import DatabaseModule
from sql_queries import SQLQueries
from table_helpers import SpokeTableModel

class SpokeModule:

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

        # Reducing verbosity
        self.__rm_stretch: QHeaderView.ResizeMode = \
            QHeaderView.ResizeMode.Stretch
        self.__rm_shrink: QHeaderView.ResizeMode =\
            QHeaderView.ResizeMode.ResizeToContents
        self.__select_rows: QAbstractItemView.SelectionBehavior = \
            QAbstractItemView.SelectionBehavior.SelectRows
        self.__select_single: QAbstractItemView.SelectionMode = \
            QAbstractItemView.SelectionMode.SingleSelection


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

    def sync_comboboxes(self, combo_box, value) -> None:
        """
        Synchronize the value of combo boxes between the two tabs.
        """
        if combo_box == self.ui.comboBoxSpoke:
            self.ui.comboBoxSpoke2.setCurrentText(value)
        elif combo_box == self.ui.comboBoxSpoke2:
            self.ui.comboBoxSpoke.setCurrentText(value)

    def sync_spoke_selection(self, sender: QComboBox) -> None:
        """
        Synchronize the spoke selection between the Database Tab and
        Measurement Tab while preventing circular calls.
        """
        if sender == self.ui.comboBoxSpoke:
            # Sync comboBoxSpoke2 with comboBoxSpoke
            self.ui.comboBoxSpoke2.blockSignals(True)
            self.ui.comboBoxSpoke2.setCurrentIndex(
                self.ui.comboBoxSpoke.currentIndex()
            )
            self.ui.comboBoxSpoke2.blockSignals(False)
        elif sender == self.ui.comboBoxSpoke2:
            # Sync comboBoxSpoke with comboBoxSpoke2
            self.ui.comboBoxSpoke.blockSignals(True)
            self.ui.comboBoxSpoke.setCurrentIndex(
                self.ui.comboBoxSpoke2.currentIndex()
            )
            self.ui.comboBoxSpoke.blockSignals(False)

        # Update the details for the currently selected spoke
        self.update_spoke_details(sender)

    def sync_manufacturer_selection(self, sender: QComboBox, index: int) -> None:
        """
        Synchronize the manufacturer selection between the
        Database Tab and Measurement Tab. Trigger loading
        of spokes for the selected manufacturer.
        """
        combo1: QComboBox = self.ui.comboBoxManufacturer
        combo2: QComboBox = self.ui.comboBoxManufacturer2
        selected_manufacturer_id: int = sender.itemData(index)

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

        self.load_spokes()

    def update_spoke_details(self, sender: QComboBox) -> None:
        """
        Update the spoke details fields when a spoke is
        selected in comboBoxSpoke.
        """
        spoke_id: int | None = sender.currentData()

        if spoke_id is None:
            self.clear_spoke_details()
            return
        spoke_id = int(spoke_id)

        spokes: list[Any] = self.db.execute_select(
            query=SQLQueries.GET_SPOKES_BY_ID,
            params=(spoke_id,))
        if not spokes:
            return

        self.update_fields(spokes[0][1:])

    def load_manufacturers(self) -> None:
        """
        Load all manufacturer names from the database and populate the
        the dropdowns. Automatically loads spokes for the first manufacturer.
        """
        # Load manufacturers
        manufacturers: list[Any] = self.db.execute_select(
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
        spoke_types: list[Any] = self.db.execute_select(
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
            self.load_spokes()

    def load_spokes(self) -> None:
        """
        Load all spokes for the currently selected manufacturer and populate
        the tableViewSpokesDatabase and comboBoxSpoke.
        """
        manufacturer_id: int | None = \
            self.ui.comboBoxManufacturer.currentData()

        if manufacturer_id is None:
            return
        manufacturer_id = int(manufacturer_id)

        spokes: list[Any] = self.db.execute_select(
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
        self.current_spokes: list[tuple[Any, list[Any]]] = [
            (spoke[0], list(spoke[1:]))
            for spoke in spokes]
        model = SpokeTableModel(self.current_spokes, headers)
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

    def populate_filter_type(self):
        """
        Populate comboBoxFilterType with unique spoke types.
        """
        types = {spoke[1][1] for spoke in self.current_spokes}
        self.ui.comboBoxFilterType.clear()
        self.ui.comboBoxFilterType.addItem("")  # Empty means no filter is set
        self.ui.comboBoxFilterType.addItems(sorted(types))

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
        model: SpokeTableModel = cast(
            SpokeTableModel,
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

        model: SpokeTableModel = cast(
            SpokeTableModel,
            self.ui.tableViewSpokesDatabase.model())

        for row in range(model.rowCount()):
            if model.get_id(row) == spoke_id:
                self.ui.tableViewSpokesDatabase.selectRow(row)
                break

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
