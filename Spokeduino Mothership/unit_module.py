from enum import Enum
from ui import Ui_mainWindow


class UnitEnum(Enum):
    NEWTON = "Newton"
    KGF = "kgF"
    LBF = "lbF"


class UnitModule:

    def __init__(self,
                 ui: Ui_mainWindow
                 ) -> None:
        self.__ui: Ui_mainWindow = ui

    @staticmethod
    def convert_units(
            value: float,
            source: UnitEnum) -> tuple[float, float, float]:
        """
        Convert units
        :param value: The value to be converted.
        :param source: The unit type that triggered the conversion.
        :return the values in newton, kgf and lbf.
        """
        match source:
            case UnitEnum.NEWTON:
                return (value,
                        value * 0.1019716213,
                        value * 0.2248089431)
            case UnitEnum.KGF:
                return (value / 0.1019716213,
                        value,
                        value * 2.2046226218)
            case UnitEnum.LBF:
                return (value / 0.2248089431,
                        value / 2.2046226218,
                        value)
        return 0.0, 0.0, 0.0

    def convert_units_realtime(self, source: UnitEnum) -> None:
        """
        Convert units in real time
        :param source: The unit type that triggered the conversion.
        """
        try:
            # Read input values
            match source:
                case UnitEnum.NEWTON:
                    value = float(self.__ui.lineEditConverterNewton.text() or 0)
                    newton, kgf, lbf = self.convert_units(value, source)
                    self.__ui.lineEditConverterKgF.blockSignals(True)
                    self.__ui.lineEditConverterLbF.blockSignals(True)

                    self.__ui.lineEditConverterKgF.setText(f"{kgf:.2f}")
                    self.__ui.lineEditConverterLbF.setText(f"{lbf:.2f}")

                    self.__ui.lineEditConverterKgF.blockSignals(False)
                    self.__ui.lineEditConverterLbF.blockSignals(False)
                case UnitEnum.KGF:
                    value = float(self.__ui.lineEditConverterKgF.text() or 0)
                    newton, kgf, lbf = self.convert_units(value, source)
                    self.__ui.lineEditConverterNewton.blockSignals(True)
                    self.__ui.lineEditConverterLbF.blockSignals(True)

                    self.__ui.lineEditConverterNewton.setText(f"{newton:.2f}")
                    self.__ui.lineEditConverterLbF.setText(f"{lbf:.2f}")

                    self.__ui.lineEditConverterNewton.blockSignals(False)
                    self.__ui.lineEditConverterLbF.blockSignals(False)
                case UnitEnum.LBF:
                    value = float(self.__ui.lineEditConverterLbF.text() or 0)
                    newton, kgf, lbf = self.convert_units(value, source)
                    self.__ui.lineEditConverterKgF.blockSignals(True)
                    self.__ui.lineEditConverterNewton.blockSignals(True)

                    self.__ui.lineEditConverterNewton.setText(f"{newton:.2f}")
                    self.__ui.lineEditConverterKgF.setText(f"{kgf:.2f}")

                    self.__ui.lineEditConverterKgF.blockSignals(False)
                    self.__ui.lineEditConverterNewton.blockSignals(False)
        except ValueError:
            # Clear the other textboxes if the input is invalid
            match source:
                case UnitEnum.NEWTON:
                    self.__ui.lineEditConverterKgF.clear()
                    self.__ui.lineEditConverterLbF.clear()
                case UnitEnum.KGF:
                    self.__ui.lineEditConverterNewton.clear()
                    self.__ui.lineEditConverterLbF.clear()
                case UnitEnum.LBF:
                    self.__ui.lineEditConverterNewton.clear()
                    self.__ui.lineEditConverterKgF.clear()

    def get_unit(self) -> UnitEnum:
        """
        Returns the tension unit currently set, or Newton as default
        """
        if self.__ui.radioButtonKgF.isChecked():
            return UnitEnum.KGF
        elif self.__ui.radioButtonLbF.isChecked():
            return UnitEnum.LBF
        return UnitEnum.NEWTON
