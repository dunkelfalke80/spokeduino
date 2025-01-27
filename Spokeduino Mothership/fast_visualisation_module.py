from typing import Any, Optional
import numpy as np
from PySide6.QtWidgets import QWidget, QVBoxLayout
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from PySide6.QtCore import QRectF
from calculation_module import FitType, TensionDeflectionFitter


class PyQtGraphCanvas(QWidget):
    """
    A QWidget that contains a PyQtGraph PlotWidget for embedding plots into a PySide6 application.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        # Create the PlotWidget
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground("w")  # Set background to white

        # Layout: place the PlotWidget inside this QWidget
        layout = QVBoxLayout(self)
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

    def clear(self) -> None:
        """
        Clears all plots on the widget.
        """
        self.plot_widget.clear()


class VisualisationModule:
    """
    A module for visualizing fitted curves and spoke tensions using PyQtGraph.
    """

    def __init__(self, fitter: TensionDeflectionFitter) -> None:
        """
        Store or instantiate a TensionDeflectionFitter here.
        """
        self.fitter: TensionDeflectionFitter = fitter

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
        plot_widget: pg.PlotWidget,
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
        # Clear the plot
        plot_widget.clear()

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
        plot_widget.plot(
            tensions, deflections, pen=pg.mkPen(color="b", width=2), name="Fitted Curve"
        )

        # Plot measured points
        plot_widget.plot(
            measured_tensions,
            measured_deflections,
            pen=None,
            symbol="o",
            symbolBrush="r",
            name="Measured Points",
        )

        # Add a second plot for deviations
        deviation_plot = pg.ViewBox()
        plot_widget.scene().addItem(deviation_plot)
        deviation_plot.setYRange(deviation_range[0], deviation_range[1])
        deviation_curve = pg.PlotCurveItem(
            measured_tensions, deviations, pen=pg.mkPen(color="orange", width=2)
        )
        deviation_plot.addItem(deviation_curve)

        # Set plot labels and grid
        plot_widget.setTitle(header, color="black", size="12pt")
        plot_widget.setLabel("left", "Deflection (mm)", color="blue")
        plot_widget.setLabel("bottom", "Tension (N)", color="black")
        plot_widget.showGrid(x=True, y=True)

    @staticmethod
    def __prepare_radar_data(spokes: int, tensions: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """
        Prepares angles and closes the radar chart data for plotting.
        """
        angles = np.linspace(0, 2 * np.pi, spokes, endpoint=False)
        tensions_closed = np.append(tensions, tensions[0])  # Close the loop
        angles_closed = np.append(angles, angles[0])  # Close the loop
        return angles_closed, tensions_closed

    def draw_static_elements(
        self,
        plot_widget: pg.PlotWidget,
        left_spokes: int,
        right_spokes: int,
        target_tension_left: Optional[float] = None,
        target_tension_right: Optional[float] = None
    ) -> None:
        """
        Draw static elements for the radar chart, including spoke lines, spoke numbers,
        and target tension circles. Handles asymmetric spoke counts and ensures proper scaling.
        """
        # Clear everything
        plot_widget.clear()

        # Hide X and Y axes completely
        for axis in ("bottom", "left"):
            axis_item = plot_widget.getAxis(axis)
            axis_item.setStyle(showValues=False)
            axis_item.hide()

        # Lock the chart position
        plot_widget.setMouseEnabled(x=False, y=False)
        plot_widget.setAspectLocked(True)

        # Determine max radius for scaling
        max_target_tension = max(target_tension_left or 0, target_tension_right or 0, 1)
        max_radius = max_target_tension + 200  # Add smaller buffer

        # Adjust chart range
        rect = QRectF(-max_radius, -max_radius, 2 * max_radius, 2 * max_radius)
        plot_widget.setRange(rect)

        # Prepare spoke angles (align first spoke to 0° and clockwise)
        angles_left = -np.linspace(0, 2 * np.pi, left_spokes, endpoint=False) - np.pi / 2
        angles_right = -np.linspace(0, 2 * np.pi, right_spokes, endpoint=False) - np.pi / 2

        # Helper to draw spokes and numbers
        def draw_spokes(angles, color, radius, offset_x=0, offset_y=0):
            for i, angle in enumerate(angles):
                x = np.cos(angle) * radius
                y = np.sin(angle) * radius

                # Draw spoke lines
                plot_widget.plot(
                    [0, x + offset_x], [0, y + offset_y],
                    pen=pg.mkPen(color="gray", style=pg.QtCore.Qt.PenStyle.DotLine, width=1),
                )

                # Draw spoke numbers
                text_item = pg.TextItem(
                    str(i + 1), anchor=(0.5, 0.5), color=color
                )
                text_item.setPos(x * 1.1 + offset_x, y * 1.1 + offset_y)
                plot_widget.addItem(text_item)

        # Draw spokes and numbers
        if left_spokes == right_spokes:
            draw_spokes(angles_left, color="blue", radius=max_radius)
        else:
            draw_spokes(angles_left, color="blue", radius=max_radius, offset_x=-20)
            draw_spokes(angles_right, color="red", radius=max_radius, offset_x=20)

        # Draw target circles
        def draw_target_circle(target_tension, color):
            if target_tension is not None and target_tension > 0:
                circle_x = np.cos(np.linspace(0, 2 * np.pi, 360)) * target_tension
                circle_y = np.sin(np.linspace(0, 2 * np.pi, 360)) * target_tension
                plot_widget.plot(
                    circle_x, circle_y,
                    pen=pg.mkPen(color=color, style=pg.QtCore.Qt.PenStyle.DashLine, width=2),
                    name=f"{color.capitalize()} Target Tension",
                )

        draw_target_circle(target_tension_left, "blue")
        draw_target_circle(target_tension_right, "red")

        # Ensure the legend is created once
        if not hasattr(self, "_legend_added") or not self._legend_added:
            plot_widget.addLegend(offset=(10, 10))
            self._legend_added = True

    def plot_dynamic_tensions(
        self,
        plot_widget: pg.PlotWidget,
        left_spokes: int,
        right_spokes: int,
        tensions_left: np.ndarray,
        tensions_right: np.ndarray
    ) -> None:
        """
        Plot spoke tensions dynamically. Clears previous tensions and updates.
        """
        # Clear only dynamic plots
        for item in plot_widget.listDataItems():
            plot_widget.removeItem(item)

        # Prepare radar data
        angles_left, tensions_left = self.__prepare_radar_data(left_spokes, tensions_left)
        angles_right, tensions_right = self.__prepare_radar_data(right_spokes, tensions_right)

        # Adjust angles so the first spoke is at 0° and clockwise
        angles_left = -angles_left - np.pi / 2
        angles_right = -angles_right - np.pi / 2

        # Convert polar to Cartesian coordinates
        left_x = np.cos(angles_left) * tensions_left
        left_y = np.sin(angles_left) * tensions_left
        right_x = np.cos(angles_right) * tensions_right
        right_y = np.sin(angles_right) * tensions_right

        # Plot left and right tensions
        plot_widget.plot(
            left_x, left_y,
            pen=pg.mkPen(color="blue", width=2),
            name="Left Tensions",
        )
        plot_widget.plot(
            right_x, right_y,
            pen=pg.mkPen(color="red", width=2),
            name="Right Tensions",
        )
