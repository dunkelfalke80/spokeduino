from typing import Any, Optional
import numpy as np
from matplotlib.projections.polar import PolarAxes
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from calculation_module import FitType, TensionDeflectionFitter


class MatplotlibCanvas(QWidget):
    """
    A QWidget that contains a Matplotlib Figure and Canvas for
    embedding plots into a PySide6 application.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        # Create a new Matplotlib Figure and attach it to a FigureCanvas
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)

        # Layout: place the canvas widget inside this QWidget
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def clear_figure(self) -> None:
        """
        Clears the figure's axes so you can redraw a fresh plot.
        """
        self.figure.clear()

    def draw_figure(self) -> None:
        """
        Convenience method to refresh the canvas after plotting.
        """
        self.canvas.draw()


class VisualisationModule:
    """
    A module for visualizing fitted curves and spoke tensions.
    """

    def __init__(self, fitter: TensionDeflectionFitter) -> None:
        """
        Store or instantiate a TensionDeflectionFitter here.
        """
        self.fitter: TensionDeflectionFitter = fitter

    @staticmethod
    def __validate_array_size(array: np.ndarray, expected_size: int, name: str) -> None:
        """
        Validates that an array matches an expected size.
        """
        if array.shape[0] != expected_size:
            raise ValueError(f"{name} array must have {expected_size} elements, "
                             f"but has {array.shape[0]}.")

    @staticmethod
    def __prepare_radar_data(spokes: int, tensions: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """
        Prepares angles and closes the radar chart data for plotting.
        """
        angles = np.linspace(0, 2 * np.pi, spokes, endpoint=False)
        tensions_closed = np.append(tensions, tensions[0])  # Close the loop
        angles_closed = np.append(angles, angles[0])  # Close the loop
        return angles_closed, tensions_closed

    def __predict_deflection(
        self,
        fit_type: FitType,
        model: Any,
        tensions: np.ndarray,
        fit_model: dict
    ) -> np.ndarray:
        """
        Compute deflection values from a range of tension values,
        using the given fit type and model.

        :param fit_type: The FitType used (e.g., FitType.LINEAR).
        :type fit_type: FitType
        :param model: The fitted model (coeffs, spline object, etc.).
        :type model: Any
        :param tensions: Array of tension values (N).
        :type tensions: np.ndarray
        :param fit_model: The complete dictionary with scaling_params (if needed).
        :type fit_model: dict
        :return: An array of deflection values corresponding to `tensions`.
        :rtype: np.ndarray
        """
        # We'll handle each FitType. This is basically the inverse of "calculate_tension".
        if fit_type in (FitType.LINEAR, FitType.QUADRATIC, FitType.CUBIC, FitType.QUARTIC):
            # model is np.polyfit coefficients
            poly = np.poly1d(model)
            return poly(tensions)

        elif fit_type == FitType.SPLINE:
            # model is a CubicSpline object
            spline = model
            return spline(tensions)

        elif fit_type == FitType.EXPONENTIAL:
            # model = (a, b), y = a * exp(b * x)
            a, b = model
            # For deflection: d = a * exp(b * tension)
            return a * np.exp(b * tensions)

        elif fit_type == FitType.LOGARITHMIC:
            # model = (a, b), d = a + b * ln(tension)
            # Watch out for tension <= 0 inside ln()
            a, b = model
            # We'll do a safe log. Negative or zero tensions will produce NaN
            safe_tensions = np.where(tensions <= 0, np.nan, tensions)
            return a + b * np.log(safe_tensions)

        elif fit_type == FitType.POWER_LAW:
            # model = (a, b), d = a * tension^b
            a, b = model
            # If tension < 0, that yields an invalid deflection => produce NaN
            safe_tensions = np.where(tensions < 0, np.nan, tensions)
            return a * (safe_tensions ** b)

        elif fit_type == FitType.CHEBYSHEV:
            # model = poly coefficients in ascending order
            # Also check scaling_params for domain transformation
            coefs = model
            scaling_params = fit_model.get("scaling_params", None)
            if not scaling_params:
                # If missing, just interpret coefs as standard poly
                poly = np.poly1d(coefs)
                return poly(tensions)
            else:
                t_min, t_max = scaling_params
                # We want to transform tensions -> normalized in [-1, 1]
                # normalized_t = 2*(t - t_min)/(t_max - t_min) - 1
                denom = (t_max - t_min) if (t_max - t_min) != 0 else 1
                normalized_t = 2.0 * (tensions - t_min) / denom - 1.0
                poly = np.poly1d(coefs)  # coefs are in ascending order
                return poly(normalized_t)

        else:
            # Unsupported or unknown fit type => return all zeros or NaNs
            return np.full_like(tensions, np.nan)

    def plot_fit_with_deviation(
        self,
        ax: Axes,
        fit_model: dict,
        data: list[tuple[float, float]],
        step: float = 100.0,
        deviation_range: tuple[float, float] = (-50, 50),
        header: str = ""
    ) -> None:
        """
        Generates a chart showing the fitted deflection curve and deviation of
        measured data points (in tension) from the fitted model.
        """
        # Clear existing plots
        ax.cla()
        ax2 = ax.twinx()
        ax2.cla()

        # Extract metadata
        t_min, t_max = fit_model["t_min"], fit_model["t_max"]
        fit_type, model = fit_model["fit_type"], fit_model["model"]

        # Generate tension values and deflections
        tensions = np.arange(t_min, t_max + step, step)
        deflections = self.__predict_deflection(fit_type, model, tensions, fit_model)

        # Compute deviations
        measured_tensions, measured_deflections = zip(*data)
        calculated_tensions = [
            self.fitter.calculate_tension(fit_model, d_meas)
            for d_meas in measured_deflections
        ]
        deviations = [
            (t_calc - t_meas) if t_calc is not None else np.nan
            for t_calc, t_meas in zip(calculated_tensions, measured_tensions)
        ]

        # Plot the fitted curve
        ax.plot(tensions, deflections, label="Fitted Curve", color="blue")
        ax.scatter(measured_tensions, measured_deflections, label="Measured Points", color="red")
        ax.set_xlabel("Tension (N)")
        ax.set_ylabel("Deflection (mm)", color="blue")
        ax.tick_params(axis="y", labelcolor="blue")
        ax.legend(loc="upper left")
        ax.grid(True)

        # Plot deviations
        ax2.scatter(measured_tensions, deviations, color="orange", marker="x", label="Deviation")
        ax2.set_ylabel("Deviation in Tension (N)", color="orange")
        ax2.yaxis.set_label_position("right")
        ax2.yaxis.set_ticks_position("right")
        ax2.tick_params(axis="y", labelcolor="orange")
        ax2.set_ylim(deviation_range)
        ax2.axhline(0, color="gray", linestyle="--", linewidth=1)

        ax.set_title(header)

    def plot_spoke_tensions(
        self,
        ax: PolarAxes,
        left_spokes: int,
        right_spokes: int,
        tensions_left: np.ndarray,
        tensions_right: np.ndarray,
        target_left: Optional[float] = None,
        target_right: Optional[float] = None
    ) -> None:
        """
        Plots a radar chart of spoke tensions for both sides of a wheel.
        """
        # Clear the polar Axes
        ax.cla()

        # Validate input arrays
        self.__validate_array_size(tensions_left, left_spokes, "Left tensions")
        self.__validate_array_size(tensions_right, right_spokes, "Right tensions")

        # Prepare radar data
        angles_left, tensions_left = self.__prepare_radar_data(left_spokes, tensions_left)
        angles_right, tensions_right = self.__prepare_radar_data(right_spokes, tensions_right)

        # Plot left side
        ax.plot(angles_left, tensions_left, label="Left Tensions", color="blue")
        ax.fill(angles_left, tensions_left, color="blue", alpha=0.25)

        # Plot right side
        ax.plot(angles_right, tensions_right, label="Right Tensions", color="red")
        ax.fill(angles_right, tensions_right, color="red", alpha=0.25)

        # Plot target tensions
        if target_left:
            target_left_array = np.full(left_spokes, target_left)
            _, target_left_array = self.__prepare_radar_data(left_spokes, target_left_array)
            ax.plot(angles_left, target_left_array, label="Left Target", color="blue", linestyle="--")

        if target_right:
            target_right_array = np.full(right_spokes, target_right)
            _, target_right_array = self.__prepare_radar_data(right_spokes, target_right_array)
            ax.plot(angles_right, target_right_array, label="Right Target", color="red", linestyle="--")

        # Polar adjustments
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        if not ax.get_legend():
            ax.legend(loc="upper right", bbox_to_anchor=(1.1, 1.1))