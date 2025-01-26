from typing import Any
import numpy as np
from matplotlib.projections.polar import PolarAxes
from matplotlib.figure import Figure
from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.axes import Axes
from calculation_module import FitType


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
    Assumes the 'fit_model' dictionary was produced by TensionDeflectionFitter.fit_data(...).
    """

    def __init__(self, fitter) -> None:
        """
        Store or instantiate a TensionDeflectionFitter here.
        """
        self.fitter = fitter

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
        measured data points (in tension) from the fitted model, **on the Axes you provide**.

        :param ax: A Matplotlib Axes (regular Cartesian axes).
        :param fit_model: Dictionary returned by TensionDeflectionFitter.fit_data(...).
        :param data: List of (tension, deflection) pairs (N, mm).
        :param step: Step size for tension values in the plotted range (N).
        :param deviation_range: (ymin, ymax) for the deviation axis on the twin Axes.
        """
        # Clear these axes
        ax.cla()
        ax2 = ax.twinx()
        ax2.cla()

        # Extract metadata from fit_model
        t_min = fit_model["t_min"]
        t_max = fit_model["t_max"]
        fit_type = fit_model["fit_type"]
        model = fit_model["model"]

        # Generate tension values for plotting
        tensions = np.arange(t_min, t_max + step, step)

        # Compute deflections from the model
        deflections = self.__predict_deflection(
            fit_type=fit_type,
            model=model,
            tensions=tensions,
            fit_model=fit_model)

        # Calculate deviations for the measured data
        measured_tensions, measured_deflections = zip(*data)

        calculated_tensions = [
            self.fitter.calculate_tension(fit_model, d_meas)
            for d_meas in measured_deflections
        ]

        # Deviation = (calculated tension) - (measured tension)
        deviations = [
            (t_calc - t_meas) if t_calc is not None else np.nan
            for t_calc, t_meas in zip(calculated_tensions, measured_tensions)
        ]

        # Plot the fitted curve (left Y-axis)
        ax.plot(tensions, deflections, label="Fitted Curve", color="blue")
        ax.scatter(measured_tensions, measured_deflections, label="Measured Points", color="red")
        ax.set_xlabel("Tension (N)")
        ax.set_ylabel("Deflection (mm)", color="blue")
        ax.tick_params(axis="y", labelcolor="blue")
        ax.legend(loc="upper left")
        ax.grid(True)

        # Plot the deviations (right Y-axis)
        ax2.scatter(measured_tensions, deviations,
                    label="Deviation (Measured vs Calculated)",
                    color="orange", marker="x")
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
        spokes_per_side: int,
        tensions_left: list[tuple[int, float]],
        tensions_right: list[tuple[int, float]],
        target_left: float,
        target_right: float
    ) -> None:
        """
        Plots a radar chart of spoke tensions for both sides of a wheel,
        **on the polar Axes you provide**.

        :param ax: A Matplotlib polar Axes (e.g., from figure.add_subplot(projection="polar")).
        :param spokes_per_side: Number of spokes on each side (assumes symmetrical).
        :param tensions_left: List of (index, tension) for left spokes.
        :param tensions_right: List of (index, tension) for right spokes.
        :param target_left: Optional target tension for left spokes.
        :param target_right: Optional target tension for right spokes.
        """
        # Clear the polar Axes
        ax.cla()

        # Build arrays
        tensions_left_array = np.zeros(spokes_per_side)
        tensions_right_array = np.zeros(spokes_per_side)

        for idx, tension_val in tensions_left:
            tensions_left_array[idx % spokes_per_side] = tension_val
        for idx, tension_val in tensions_right:
            tensions_right_array[idx % spokes_per_side] = tension_val

        # Radar angles
        angles: Any = np.linspace(0, 2 * np.pi, spokes_per_side, endpoint=False).tolist()
        angles += angles[:1]  # close loop

        # Close each array for radar
        tensions_left_array = np.append(tensions_left_array, tensions_left_array[0])
        tensions_right_array = np.append(tensions_right_array, tensions_right_array[0])

        # Plot left side
        ax.plot(angles, tensions_left_array, label="Left Tensions", color="blue")
        ax.fill(angles, tensions_left_array, color="blue", alpha=0.25)

        # Plot right side
        ax.plot(angles, tensions_right_array, label="Right Tensions", color="red")
        ax.fill(angles, tensions_right_array, color="red", alpha=0.25)

        # Optionally plot target lines
        if target_left is not None:
            target_left_array = np.full(spokes_per_side, target_left)
            target_left_array = np.append(target_left_array, target_left_array[0])
            ax.plot(angles, target_left_array, label="Left Target", color="blue", linestyle="--")

        if target_right is not None:
            target_right_array = np.full(spokes_per_side, target_right)
            target_right_array = np.append(target_right_array, target_right_array[0])
            ax.plot(angles, target_right_array, label="Right Target", color="red", linestyle="--")

        # Polar adjustments
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels([f"{i + 1}" for i in range(spokes_per_side)])
        ax.set_rlabel_position(180 / spokes_per_side)
        ax.set_yticks([])
        ax.legend(loc="upper right", bbox_to_anchor=(1.1, 1.1))

    def plot_asymmetric_spoke_tensions(
        self,
        ax: PolarAxes,
        left_spokes: int,
        right_spokes: int,
        tensions_left: list[tuple[int, float]],
        tensions_right: list[tuple[int, float]],
        target_left: float,
        target_right: float
    ) -> None:
        """
        Plots a radar chart for asymmetric hubs with different spoke counts
        on each side, **on the polar Axes you provide**.

        :param ax: A Matplotlib polar Axes (e.g., from figure.add_subplot(projection="polar")).
        :param left_spokes: Number of spokes on the left side.
        :param right_spokes: Number of spokes on the right side.
        :param tensions_left: List of (index, tension) for left spokes.
        :param tensions_right: List of (index, tension) for right spokes.
        :param target_left: Optional target tension for left spokes.
        :param target_right: Optional target tension for right spokes.
        """
        # Clear
        ax.cla()

        tensions_left_array = np.zeros(left_spokes)
        tensions_right_array = np.zeros(right_spokes)

        # Fill arrays
        for idx, tension_val in tensions_left:
            tensions_left_array[idx % left_spokes] = tension_val
        for idx, tension_val in tensions_right:
            tensions_right_array[idx % right_spokes] = tension_val

        # Angles for each side
        angles_left: Any = np.linspace(0, 2 * np.pi, left_spokes, endpoint=False).tolist()
        angles_right: Any = np.linspace(0, 2 * np.pi, right_spokes, endpoint=False).tolist()

        # Close the arrays
        tensions_left_array = np.append(tensions_left_array, tensions_left_array[0])
        tensions_right_array = np.append(tensions_right_array, tensions_right_array[0])
        angles_left += angles_left[:1]
        angles_right += angles_right[:1]

        # Plot left side
        ax.plot(angles_left, tensions_left_array, label="Left Tensions", color="blue")
        ax.fill(angles_left, tensions_left_array, color="blue", alpha=0.25)

        # Plot right side
        ax.plot(angles_right, tensions_right_array, label="Right Tensions", color="red")
        ax.fill(angles_right, tensions_right_array, color="red", alpha=0.25)

        # Targets, if given
        if target_left is not None:
            target_left_array = np.full(left_spokes, target_left)
            target_left_array = np.append(target_left_array, target_left_array[0])
            ax.plot(angles_left, target_left_array, label="Left Target", color="blue", linestyle="--")

        if target_right is not None:
            target_right_array = np.full(right_spokes, target_right)
            target_right_array = np.append(target_right_array, target_right_array[0])
            ax.plot(angles_right, target_right_array, label="Right Target", color="red", linestyle="--")

        # Polar adjustments
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.legend(loc="upper right", bbox_to_anchor=(1.1, 1.1))

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