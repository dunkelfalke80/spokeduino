from typing import Any, cast
import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout
import pyqtgraph as pg
from PySide6.QtCore import QRectF
from calculation_module import FitType, TensionDeflectionFitter


class PyQtGraphCanvas(QWidget):
    """
    A QWidget that contains a PyQtGraph PlotWidget for embedding plots
    into a PySide6 application.
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
        self.__legend_added = False
        self.__clockwise: bool = True
        self.__deviation_viewbox: pg.ViewBox
        self.__legend: pg.LegendItem

    def __predict_deflection(
        self,
        fit_type: FitType,
        model: Any,
        tensions: np.ndarray
    ) -> np.ndarray:
        """
        Calculate deflection values from a range of tension values,
        using the given fit type and model.

        :param fit_type: The FitType used (e.g., FitType.LINEAR).
        :type fit_type: FitType
        :param model: The fitted model (coeffs, spline object, etc.).
        :type model: Any
        :param tensions: Array of tension values (N).
        :type tensions: np.ndarray
        :param fit_model: The complete dictionary with scaling_params.
        :type fit_model: dict
        :return: An array of deflection values corresponding to `tensions`.
        :rtype: np.ndarray
        """
        if fit_type in (
                FitType.LINEAR,
                FitType.QUADRATIC,
                FitType.CUBIC,
                FitType.QUARTIC):
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
            a, b = model
            safe_tensions = np.where(tensions <= 0, np.nan, tensions)
            return a + b * np.log(safe_tensions)

        elif fit_type == FitType.POWER_LAW:
            # model = (a, b), d = a * tension^b
            a, b = model
            # If tension < 0, that yields an invalid deflection => produce NaN
            safe_tensions = np.where(tensions < 0, np.nan, tensions)
            return a * (safe_tensions ** b)

        else:
            # Unsupported or unknown fit type => return all zeros or NaNs
            return np.full_like(tensions, np.nan)

    def clear_fit_plot(self, plot_widget: pg.PlotWidget) -> None:
        if hasattr(self, "__deviation_viewbox"):
            self.__deviation_viewbox.clear()
        plot_widget.clear()

    def update_fit_plot(
        self,
        plot_widget: pg.PlotWidget,
        fit_model: dict,
        data: list[tuple[float, float]],
        step: float = 100.0,
        deviation_range: tuple[float, float] = (-20, 20),
        header: str = ""
    ) -> None:
        """
        Generates a chart showing the fitted deflection curve
        and the deviation data (on a secondary Y axis to the right).
        """

        # Clear old items from the widget
        self.clear_fit_plot(plot_widget)

        # Disable mouse-based panning/zooming
        plot_widget.setMouseEnabled(x=False, y=False)

        # Get the main PlotItem and check None
        plot_item = plot_widget.getPlotItem()
        if plot_item is None:
            raise RuntimeError("No PlotItem found in the given PlotWidget.")

        plot_item.showGrid(x=True, y=True)
        # Disable scrolling/zooming from scroll wheel or axis dragging
        plot_widget.setMouseEnabled(x=False, y=False)
        plot_widget.enableAutoRange(axis=pg.ViewBox.XYAxes, enable=False)

        # Create (or retrieve) a second ViewBox for deviation data
        if not hasattr(self, "__deviation_viewbox"):
            self.__deviation_viewbox = pg.ViewBox()
            # Show the right axis in the main PlotItem
            plot_item.showAxis("right")
            plot_item.getAxis("right").setLabel("Deviation (N)", color="green")
            # Add the second ViewBox to the PlotItem's scene
            plot_item.scene().addItem(self.__deviation_viewbox)
            # Link the right axis to the new ViewBox
            plot_item.getAxis("right").linkToView(self.__deviation_viewbox)
        else:
            self.__deviation_viewbox.clear()

        # Link the second ViewBox's X-axis to the main view box
        main_vb = plot_item.getViewBox()
        if main_vb is None:
            raise RuntimeError("No default ViewBox found in the PlotItem.")
        self.__deviation_viewbox.setXLink(main_vb)

        # Extract fit_model info
        t_min = fit_model["t_min"]
        t_max = fit_model["t_max"]
        fit_type = fit_model["fit_type"]
        model = fit_model["model"]

        # Generate tension values (X) and predicted deflections (Y)
        tensions = np.arange(t_min, t_max + step, step)
        deflections = self.__predict_deflection(
            fit_type, model, tensions)

        # Calculate deviations
        measured_tensions, measured_deflections = zip(*data)
        calculated_tensions = [
            self.fitter.calculate_tension(fit_model, d_meas)
            for d_meas in measured_deflections
        ]
        deviations = [
            (t_calc - t_meas) if t_calc is not None else np.nan
            for t_calc, t_meas in zip(calculated_tensions, measured_tensions)
        ]

        # Plot main data on the main PlotItem/view
        # Fitted curve (blue)
        fitted_curve = pg.PlotDataItem(
            x=tensions,
            y=deflections,
            pen=pg.mkPen(color="blue", width=2),
            name="Fitted Curve"
        )
        plot_item.addItem(fitted_curve)

        # Measured points (red)
        measured_points = pg.PlotDataItem(
            x=measured_tensions,
            y=measured_deflections,
            pen=None,
            symbol="o",
            symbolBrush="red",
            name="Measured Points"
        )
        plot_item.addItem(measured_points)

        # Plot deviation data on the second ViewBox
        deviation_curve = pg.PlotDataItem(
            x=measured_tensions,
            y=deviations,
            pen=None,  # No line
            symbol="o",
            symbolBrush="green",
            name="Deviation"
        )
        self.__deviation_viewbox.addItem(deviation_curve)

        # Labels, Title, Legend
        plot_item.setLabel("left", "Deflection (mm)", color="blue")
        plot_item.setLabel("bottom", "Tension (N)", color="black")
        plot_item.setTitle(header, color="black", size="12pt")

        if not hasattr(self, "__legend"):
            self.__legend = plot_item.addLegend(offset=(10, 10))

        # Sync second ViewBox with main ViewBox
        def update_views():
            """Keep second ViewBox geometry in sync with main one."""
            self.__deviation_viewbox.setGeometry(main_vb.sceneBoundingRect())

        try:
            main_vb.sigResized.disconnect()
        except TypeError:
            pass
        main_vb.sigResized.connect(update_views)
        update_views()

        # Manually zoom out to make sure everything is visible
        all_x_vals = np.concatenate([tensions, measured_tensions])
        all_y_vals = np.concatenate([deflections, measured_deflections])

        x_min, x_max = np.nanmin(all_x_vals), np.nanmax(all_x_vals)
        y_min, y_max = np.nanmin(all_y_vals), np.nanmax(all_y_vals)
        x_min_float: float = cast(float, x_min)
        x_max_float: float = cast(float, x_max)

        # Add a small margin so points are not on the extreme edge:
        x_margin: float = 0.05 * (
            x_max_float - x_min_float
            if x_max_float > x_min_float
            else 1.0)
        y_margin: float = 0.05 * (
            y_max - y_min
            if y_max > y_min
            else 1.0)

        plot_widget.setXRange(x_min - x_margin, x_max_float + x_margin)
        plot_widget.setYRange(y_min - y_margin, y_max + y_margin)

        # And fix the second axis range for deviations
        self.__deviation_viewbox.setYRange(
            deviation_range[0], deviation_range[1])
        deviation_curve = pg.PlotDataItem(
            x=measured_tensions,
            y=deviations,
            pen=pg.mkPen(color="green", width=1),  # <-- Draw a green line
            symbol="o",
            symbolBrush="green",
            name="Deviation"
        )
        self.__deviation_viewbox.addItem(deviation_curve)

    @staticmethod
    def __prepare_radar_data(
        spokes: int,
        tensions: np.ndarray,
            clockwise: bool = False) -> tuple[np.ndarray, np.ndarray]:
        """
        Prepares angles and closes the radar chart data for plotting.

        :param spokes: Number of spokes in the radar chart.
        :param tensions: Array of tension values.
        :param clockwise: Direction of the radar chart.
                          True for clockwise, False for anticlockwise.
        :return: Tuple of angles and closed tensions arrays.
        """
        # Starting angle at pi/2 to position the first spoke at the top
        start_angle = np.pi / 2

        if clockwise:
            angles = np.linspace(
                start_angle, start_angle - 2 * np.pi, spokes, endpoint=False)
        else:
            angles = np.linspace(
                start_angle, start_angle + 2 * np.pi, spokes, endpoint=False)

        tensions_closed = np.append(tensions, tensions[0])  # Close the loop
        angles_closed = np.append(angles, angles[0])        # Close the loop
        return angles_closed, tensions_closed

    # Draw target circles
    def __draw_circle(
            self,
            plot_widget: pg.PlotWidget,
            target_tension: float,
            is_left: bool,
            target: bool) -> None:
        circle_x = np.cos(np.linspace(0, 2 * np.pi, 360)) * target_tension
        circle_y = np.sin(np.linspace(0, 2 * np.pi, 360)) * target_tension

        if target:
            if is_left:
                color: str = "red"
                name: str = "Left target tension"
            else:
                color = "blue"
                name = "Right target tension"
            circle_item = plot_widget.plot(
                circle_x, circle_y,
                pen=pg.mkPen(
                    color=color,
                    style=Qt.PenStyle.DashLine,
                    width=2,
                    name=name))
        else:
            circle_item = plot_widget.plot(
                circle_x, circle_y,
                pen=pg.mkPen(
                    color="black",
                    style=Qt.PenStyle.SolidLine,
                    width=1))

        circle_item._static_element = True

    # Helper to draw spokes and numbers
    def __draw_spokes(
            self,
            plot_widget,
            angles,
            color,
            radius,
            offset_x=0,
            offset_y=0) -> None:
        for i, angle in enumerate(angles[:-1]):  # Exclude the last angle
            x = np.cos(angle) * radius
            y = np.sin(angle) * radius

            # Draw spoke lines
            line_item = plot_widget.plot(
                [0, x + offset_x], [0, y + offset_y],
                pen=pg.mkPen(
                    color="gray",
                    style=Qt.PenStyle.DotLine,
                    width=1),
                name=None,  # Do not add spoke lines to the legend
            )
            line_item._static_element = True  # Tag as static

            # Draw spoke numbers
            text_item = pg.TextItem(
                str(i + 1), anchor=(0.5, 0.5), color=color
            )
            text_item.setPos(x * 1.05 + offset_x, y * 1.05 + offset_y)
            plot_widget.addItem(text_item)

    # Draw target polygons
    def __draw_target_polygon(
            self,
            plot_widget,
            target_tension,
            angles,
            color):
        if target_tension is not None and target_tension > 0:
            x_coords = np.cos(angles) * target_tension
            y_coords = np.sin(angles) * target_tension
            # Close the polygon by appending the first point
            x_coords = np.append(x_coords, x_coords[0])
            y_coords = np.append(y_coords, y_coords[0])
            polygon_item = plot_widget.plot(
                x_coords, y_coords,
                pen=pg.mkPen(
                    color=color,
                    style=Qt.PenStyle.DashLine,
                    width=1),
            )
            polygon_item._static_element = True  # Tag as static

    def init_radar_plot(
            self,
            plot_widget: pg.PlotWidget,
            clockwise: bool) -> None:
        # Clear everything
        plot_widget.clear()
        self.__clockwise = clockwise

        # Hide X and Y axes completely
        for axis in ("bottom", "left"):
            axis_item = plot_widget.getAxis(axis)
            axis_item.setStyle(showValues=False)
            axis_item.hide()

        # Lock the chart position
        plot_widget.setMouseEnabled(x=False, y=False)
        plot_widget.setAspectLocked(True)

    def draw_radar_plot(
        self,
        plot_widget: pg.PlotWidget,
        left_spokes: int,
        right_spokes: int,
        target_tension_left: float,
        target_tension_right: float
    ) -> None:
        """
        Draw static elements for the radar chart,
        including spoke lines, spoke numbers,
        and target tension circles.
        Handles asymmetric spoke counts and ensures proper scaling.
        Respects the direction specified by the "clockwise" attribute.
        """
        # Determine max radius for scaling
        max_target_tension: float = max(
            target_tension_left,
            target_tension_right,
            0.0)
        max_radius: float = (max_target_tension + 200.0
                             if max_target_tension > 0.0
                             else 1600)

        # Adjust chart range
        rect = QRectF(-max_radius, -max_radius, 2 * max_radius, 2 * max_radius)
        plot_widget.setRange(rect)

        # Initialize angles
        angles_left = np.array([])
        angles_right = np.array([])

        # Prepare spoke angles based on direction using the centralized method
        if left_spokes > 0:
            angles_left, _ = self.__prepare_radar_data(
                left_spokes,
                np.zeros(left_spokes),
                self.__clockwise)
        if right_spokes > 0:
            angles_right, _ = self.__prepare_radar_data(
                right_spokes,
                np.zeros(right_spokes),
                self.__clockwise)

        # Ensure the legend is created once
        if not self.__legend_added:
            legend = plot_widget.addLegend(offset=(10, 10))
            # Add target tension items manually
            legend.addItem(
                pg.PlotDataItem(pen=pg.mkPen(
                    color="red",
                    style=Qt.PenStyle.DashLine)),
                "Left Target Tension",)
            legend.addItem(
                pg.PlotDataItem(pen=pg.mkPen(
                    color="blue",
                    style=Qt.PenStyle.DashLine)),
                "Right Target Tension",)
            self.__legend_added = True

        # Draw spokes and numbers
        if left_spokes == right_spokes:
            self.__draw_spokes(
                plot_widget,
                angles_left,
                color="black",
                radius=max_radius)
        else:
            self.__draw_spokes(
                plot_widget,
                angles_left,
                color="red",
                radius=max_radius,
                offset_x=-20)
            self.__draw_spokes(
                plot_widget,
                angles_right,
                color="blue",
                radius=max_radius,
                offset_x=40)

        # Draw target polygons
        if max_target_tension > 0.0:
            if left_spokes > 0:
                self.__draw_target_polygon(
                    plot_widget,
                    target_tension_left,
                    angles_left,
                    "red")
            if right_spokes > 0:
                self.__draw_target_polygon(
                    plot_widget,
                    target_tension_right,
                    angles_right,
                    "blue")
        self.__draw_circle(plot_widget, max_radius, False, False)

    def update_radar_plot(
        self,
        plot_widget: pg.PlotWidget,
        left_spokes: int,
        right_spokes: int,
        tensions_left: np.ndarray,
        tensions_right: np.ndarray
    ) -> None:
        """
        Plot spoke tensions dynamically. Clears previous tensions and updates.
        Respects the direction specified by the `clockwise` attribute.
        """
        # Remove only dynamic elements
        for item in plot_widget.listDataItems():
            if not hasattr(item, "_static_element"):
                plot_widget.removeItem(item)

        # Initialize angles
        angles_left = np.array([])
        angles_right = np.array([])

        # Initialize tensions
        tensions_left_closed = np.array([])
        tensions_right_closed = np.array([])

        # Prepare radar data with direction
        if left_spokes > 0:
            angles_left, tensions_left_closed = self.__prepare_radar_data(
                left_spokes, tensions_left, self.__clockwise)
        if right_spokes > 0:
            angles_right, tensions_right_closed = self.__prepare_radar_data(
                right_spokes, tensions_right, self.__clockwise)

        # Convert polar to Cartesian coordinates
        if left_spokes > 0:
            left_x = np.cos(angles_left) * tensions_left_closed
            left_y = np.sin(angles_left) * tensions_left_closed
            # Plot left tensions
            left_tensions_plot = pg.PlotDataItem(
                left_x, left_y,
                pen=pg.mkPen(color="red", width=3),
                name="Left Tensions",
                symbol='o',
                symbolBrush='red'
            )
            plot_widget.addItem(left_tensions_plot)

        if right_spokes > 0:
            right_x = np.cos(angles_right) * tensions_right_closed
            right_y = np.sin(angles_right) * tensions_right_closed
            # Plot right tensions
            right_tensions_plot = pg.PlotDataItem(
                right_x, right_y,
                pen=pg.mkPen(color="blue", width=3),
                name="Right Tensions",
                symbol='o',
                symbolBrush='blue'
            )
            plot_widget.addItem(right_tensions_plot)
