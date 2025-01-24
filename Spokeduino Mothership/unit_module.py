from typing import Any
from enum import Enum
from ui import Ui_mainWindow

class UnitEnum(Enum):
    NEWTON  = "Newton"
    KGF = "kgF"
    LBF = "lbF"


class UnitModule:

    def __init__(self,
                 ui: Ui_mainWindow
                 ) -> None:
        self.ui: Ui_mainWindow = ui

    @staticmethod
    def convert_units(value: float, source: UnitEnum) -> tuple[float, float, float]:
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
                    value = float(self.ui.lineEditConverterNewton.text() or 0)
                    newton, kgf, lbf = self.convert_units(value, source)
                    self.ui.lineEditConverterKgF.blockSignals(True)
                    self.ui.lineEditConverterLbF.blockSignals(True)

                    self.ui.lineEditConverterKgF.setText(f"{kgf:.2f}")
                    self.ui.lineEditConverterLbF.setText(f"{lbf:.2f}")

                    self.ui.lineEditConverterKgF.blockSignals(False)
                    self.ui.lineEditConverterLbF.blockSignals(False)
                case UnitEnum.KGF:
                    value = float(self.ui.lineEditConverterKgF.text() or 0)
                    newton, kgf, lbf = self.convert_units(value, source)
                    self.ui.lineEditConverterNewton.blockSignals(True)
                    self.ui.lineEditConverterLbF.blockSignals(True)

                    self.ui.lineEditConverterNewton.setText(f"{newton:.2f}")
                    self.ui.lineEditConverterLbF.setText(f"{lbf:.2f}")

                    self.ui.lineEditConverterNewton.blockSignals(False)
                    self.ui.lineEditConverterLbF.blockSignals(False)
                case UnitEnum.LBF:
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
            match source:
                case UnitEnum.NEWTON:
                    self.ui.lineEditConverterKgF.clear()
                    self.ui.lineEditConverterLbF.clear()
                case UnitEnum.KGF:
                    self.ui.lineEditConverterNewton.clear()
                    self.ui.lineEditConverterLbF.clear()
                case UnitEnum.LBF:
                    self.ui.lineEditConverterNewton.clear()
                    self.ui.lineEditConverterKgF.clear()

    def get_unit(self) -> UnitEnum:
        """
        Returns the tension unit currently set, or Newton as default
        """
        if self.ui.radioButtonKgF.isChecked():
            return UnitEnum.KGF
        elif self.ui.radioButtonLbF.isChecked():
            return UnitEnum.LBF
        return UnitEnum.NEWTON
