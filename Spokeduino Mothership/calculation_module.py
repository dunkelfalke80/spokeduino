from enum import Enum
from typing import Any, cast
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import curve_fit, brentq


class FitType(Enum):
    """
    Enumeration of different fitting models for tension–deflection data.
    """
    LINEAR = 1         # Polynomial of degree 1
    QUADRATIC = 2      # Polynomial of degree 2
    CUBIC = 3          # Polynomial of degree 3
    QUARTIC = 4        # Polynomial of degree 4
    SPLINE = 5         # Cubic spline
    EXPONENTIAL = 6    # y = a * exp(b * x)
    LOGARITHMIC = 7    # y = a + b * ln(x)
    POWER_LAW = 8      # y = a * x^b


class TensionDeflectionFitter:
    """
    A class for fitting tension–deflection data
    to various models and then computing tension
    for a given deflection (with optional extrapolation).

    :param extrapolation_factor:
        Fraction of deflection range to allow for
        extrapolation beyond the min/max deflections in the data.
    :type extrapolation_factor: float
    """

    def __init__(self, extrapolation_factor: float = 0.1) -> None:
        """
        Constructor. Stores an extrapolation factor used in calculating
        tension outside the fitted deflection range.
        """
        self.extrapolation_factor = extrapolation_factor

    def fit_data(self,
                 data: list[tuple[float, float]], fit_type: FitType) -> dict:
        """
        Fit the provided tension–deflection data with the given model type.

        :param data:
            A list of (tension, deflection) pairs
        :type data: list[tuple[float, float]]
        :param fit_type:
            The type of model to use for fitting
        :type fit_type: FitType
        :return:
            A dictionary encapsulating the fitted model and metadata:

            - **"fit_type"**: The FitType used.
            - **"model"**: The fitted coefficients or model object.
            - **"t_min"**: Minimum tension in the input data.
            - **"t_max"**: Maximum tension in the input data.
            - **"d_min"**: Minimum deflection in the input data.
            - **"d_max"**: Maximum deflection in the input data.
            - **"scaling_params"**: If Chebyshev, a tuple for
              min/max tension used in normalization.
        :rtype: dict
        """
        # Sort by ascending tension for internal consistency
        data_sorted: list[tuple[float, float]] = sorted(
            data, key=lambda x: x[0])
        tensions = np.array([pt[0] for pt in data_sorted], dtype=float)
        deflections = np.array([pt[1] for pt in data_sorted], dtype=float)

        # Determine the domain for tension and deflection in the input data
        t_min, t_max = tensions[0], tensions[-1]
        d_min, d_max = min(deflections), max(deflections)

        # Prepare a dict to store the result
        fit_model: dict[str, Any] = {
            "fit_type": fit_type,
            "t_min": t_min,
            "t_max": t_max,
            "d_min": d_min,
            "d_max": d_max,
            "model": None,
            "scaling_params": None
        }

        match fit_type:
            case (FitType.LINEAR |
                  FitType.QUADRATIC |
                  FitType.CUBIC |
                  FitType.QUARTIC):
                # np.polyfit => standard polynomial coefficients
                coefs = np.polyfit(tensions, deflections, fit_type.value)
                fit_model["model"] = coefs

            case FitType.SPLINE:
                # Cubic Spline
                spline = CubicSpline(tensions, deflections)
                fit_model["model"] = spline

            case FitType.EXPONENTIAL:
                # y = a * exp(bx)
                def exponential(x, a, b):
                    return a * np.exp(b * x)
                coefs, _ = curve_fit(exponential, tensions, deflections)
                fit_model["model"] = coefs  # (a, b)

            case FitType.LOGARITHMIC:
                # y = a + b ln(x)
                def logarithmic(x, a, b):
                    return a + b * np.log(x)
                coefs, _ = curve_fit(logarithmic, tensions, deflections)
                fit_model["model"] = coefs  # (a, b)

            case FitType.POWER_LAW:
                # y = a * x^b
                # ln(y) = ln(a) + b ln(x)
                log_tensions = np.log(tensions)
                log_deflections = np.log(deflections)
                b, log_a = np.polyfit(log_tensions, log_deflections, 1)
                a = np.exp(log_a)
                fit_model["model"] = (a, b)

            case _:
                raise ValueError(f"Unsupported FitType: {fit_type}")
        return fit_model

    def calculate_tension(self,
                          fit_model: dict, deflection: float) -> float | None:
        """
        Given a fitted model (from fit_data) and a desired deflection,
        return the predicted tension. Extrapolates beyond the deflection
        range up to ``extrapolation_factor * 100%`` outside the original
        bounds. Returns ``None`` if the request is beyond that
        extrapolation limit or no real solution is found.

        :param fit_model:
            Dictionary returned by :meth:`fit_data`.
        :type fit_model: dict
        :param deflection:
            The deflection (in mm) for tension calculation.
        :type deflection: float
        :return:
            The corresponding tension (in Newtons), or None if out of
            extrapolation range or no real solution is available.
        :rtype: float or None
        """
        fit_type = fit_model["fit_type"]
        d_min = fit_model["d_min"]
        d_max = fit_model["d_max"]
        model = fit_model["model"]
        t_min = fit_model["t_min"]
        t_max = fit_model["t_max"]

        # Determine allowable deflection range for extrapolation
        d_range = d_max - d_min
        d_lower = d_min - self.extrapolation_factor * d_range
        d_upper = d_max + self.extrapolation_factor * d_range

        # Deflection outside limits
        if deflection < d_lower or deflection > d_upper:
            return None

        match fit_type:
            # Polynomial models (LINEAR, QUADRATIC, CUBIC, QUARTIC)
            case (FitType.LINEAR |
                  FitType.QUADRATIC |
                  FitType.CUBIC |
                  FitType.QUARTIC):
                coefs = model  # np.polyfit(...) => array of coefficients
                poly = np.poly1d(coefs) - deflection
                roots = np.roots(poly)

                t_range = t_max - t_min
                t_lower = t_min - self.extrapolation_factor * t_range
                t_upper = t_max + self.extrapolation_factor * t_range

                # Filter real solutions in [t_lower, t_upper]
                real_candidates = [r.real
                                   for r in roots
                                   if abs(r.imag) < 1e-14]
                valid_tensions = [t
                                  for t
                                  in real_candidates
                                  if t_lower <= t <= t_upper]

                if valid_tensions:
                    # If multiple are valid, pick the first
                    return valid_tensions[0]
                else:
                    return None

            # Spline (CubicSpline)
            case FitType.SPLINE:
                spline = model  # CubicSpline object

                t_range = t_max - t_min
                t_lower = t_min - self.extrapolation_factor * t_range
                t_upper = t_max + self.extrapolation_factor * t_range

                def f(t: float) -> float:
                    return spline(t) - deflection

                steps = 200
                ts = np.linspace(t_lower, t_upper, steps)
                fs = [f(x) for x in ts]

                solution: float | None = None

                for i in range(steps - 1):
                    # If the function is exactly zero at fs[i]
                    if fs[i] == 0.0:
                        solution = ts[i]
                        break

                    # If there's a sign change between fs[i] and fs[i+1],
                    # brentq can bracket that root
                    if fs[i] * fs[i + 1] < 0.0:
                        try:
                            solution = cast(float, brentq(f, ts[i], ts[i + 1]))
                            break
                        except ValueError:
                            pass

                return solution  # Either float or None

            # Exponential (y = a * exp(bx))
            case FitType.EXPONENTIAL:
                a, b = model
                if deflection <= 0 or a <= 0:
                    return None
                tension = np.log(deflection / a) / b

                t_range = t_max - t_min
                t_lower = t_min - self.extrapolation_factor * t_range
                t_upper = t_max + self.extrapolation_factor * t_range
                if t_lower <= tension <= t_upper:
                    return tension
                else:
                    return None

            # Logarithmic (y = a + b ln(x))
            case FitType.LOGARITHMIC:
                a, b = model
                if b == 0:
                    return None
                tension = np.exp((deflection - a) / b)
                if tension <= 0:
                    return None

                t_range = t_max - t_min
                t_lower = t_min - self.extrapolation_factor * t_range
                t_upper = t_max + self.extrapolation_factor * t_range
                if t_lower <= tension <= t_upper:
                    return tension
                else:
                    return None

            # Power-law (y = a * x^b)
            case FitType.POWER_LAW:
                a, b = model
                if a <= 0 or deflection <= 0:
                    return None
                tension = (deflection / a) ** (1.0 / b)

                t_range = t_max - t_min
                t_lower = t_min - self.extrapolation_factor * t_range
                t_upper = t_max + self.extrapolation_factor * t_range
                if t_lower <= tension <= t_upper:
                    return tension
                else:
                    return None
            case _:
                return None
