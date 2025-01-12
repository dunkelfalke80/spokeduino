import numpy as np
from typing import Any


class PiecewiseQuarticFit:
    @staticmethod
    def generate_model(
            measurements: list[tuple[float, float]],
            pieces: int = 4,
            extend_range: tuple[int, int] = (200, 1800)) -> str:
        """
        Generates the piecewise quartic fit model
        and returns it as a serialized string.

        :param measurements: List of (tension, deflection) pairs.
        :param pieces: Number of pieces to divide the dataset into for fitting.
        :param extend_range: Tuple specifying the new
        :param tension range (min_tension, max_tension).
        :return: Serialized quartic coefficients for each piece.
        """
        measurements = sorted(measurements, key=lambda x: x[0])

        # Separate into x (tension) and y (deflection) arrays
        tensions = np.array([m[0] for m in measurements])
        deflections = np.array([m[1] for m in measurements])

        # Split data into equal sections
        section_size: int = len(tensions) // pieces
        equations: list[Any] = []

        for i in range(pieces):
            start: int = i * section_size
            end: int = (start + section_size
                   if i < pieces - 1
                   else len(tensions))

            # Fit quartic polynomial for this section
            coeffs = np.polyfit(tensions[start:end], deflections[start:end], 4)
            coeffs_ascii: str = ",".join(f"{c:.10e}" for c in coeffs)

            # Store coefficients and range
            deflection_start = np.polyval(coeffs, tensions[start])
            deflection_end = np.polyval(coeffs, tensions[end - 1])

            # Adjust ranges to ensure continuity
            if i > 0:  # Ensure overlap with the previous range
                prev_range = equations[-1].split(";")[0]
                prev_start, prev_end = [float(x) for x in
                                        prev_range.split(",")]
                deflection_start: float = min(deflection_start, prev_end)

            range_ascii: str = f"{deflection_start:.10e},{deflection_end:.10e}"
            equations.append(f"{range_ascii};{coeffs_ascii}")

        # Extend the range by fitting quartic to the first and last pieces
        min_tension, max_tension = extend_range
        first_coeffs = np.polyfit(tensions[:section_size],
                                  deflections[:section_size],
                                  4)
        last_coeffs = np.polyfit(tensions[-section_size:],
                                 deflections[-section_size:],
                                 4)

        # Extend below
        extended_deflection_start = np.polyval(first_coeffs, min_tension)
        extended_range_start: str = \
            f"{extended_deflection_start:.10e}," \
            f"{np.polyval(first_coeffs, tensions[0]):.10e}"
        extended_coeffs_start: str = ",".join(f"{c:.10e}" for c in first_coeffs)
        equations.insert(0, f"{extended_range_start};{extended_coeffs_start}")

        # Extend above
        extended_deflection_end = np.polyval(last_coeffs, max_tension)
        extended_range_end: str = \
            f"{np.polyval(last_coeffs, tensions[-1]):.10e}," \
            f"{extended_deflection_end:.10e}"
        extended_coeffs_end: str = ",".join(f"{c:.10e}" for c in last_coeffs)
        equations.append(f"{extended_range_end};{extended_coeffs_end}")

        return "|".join(equations)

    @staticmethod
    def evaluate(serialized_model: str, deflection: float) -> float:
        """
        Takes a deflection value and calculates the corresponding tension.

        :param: deflection: Deflection value (mm).
        :return: Calculated tension (N).
        """
        pieces: list[str] = serialized_model.split("|")

        for piece in pieces:
            range_str, coeffs_str = piece.split(";")
            coeffs = np.array([float(c) for c in coeffs_str.split(",")])
            range_start, range_end = [float(x) for x in range_str.split(",")]

            # Check if deflection falls within this range
            if range_start <= deflection <= range_end:
                # Quartic equation: ax^4 + bx^3 + cx^2 + dx + e = deflection
                coeffs[-1] -= deflection

                # Find roots
                roots = np.roots(coeffs)

                # Filter for real, positive roots (tension must be positive)
                real_roots: list[Any] = [r.real for r in roots
                              if np.isreal(r) and r.real > 0]

                if not real_roots:
                    raise ValueError("No valid value.")

                # Return the smallest positive real root
                return min(real_roots)

        raise ValueError("Deflection out of range.")
