import numpy as np
from typing import List, Tuple


class PiecewiseQuarticFit:
    def __init__(self, measurements: List[Tuple[float, float]],
                 pieces: int = 4,
                 extend_range: Tuple[int, int] = (200, 1800)):
        """
        Initializes the PiecewiseQuarticFit object.

        Parameters:
            measurements: List of (tension, deflection) pairs.
            pieces: Number of pieces to divide the dataset into for fitting.
            extend_range: Tuple specifying the new
            tension range (min_tension, max_tension).
        """
        self.measurements = sorted(measurements, key=lambda x: x[0])
        self.pieces = pieces
        self.extend_range = extend_range
        self.serialized_model = self._generate_model()

    def _generate_model(self) -> str:
        """
        Generates the piecewise quartic fit model
        and returns it as a serialized string.

        Returns:
            str: Serialized quartic coefficients for each piece.
        """
        # Separate into x (tension) and y (deflection) arrays
        tensions = np.array([m[0] for m in self.measurements])
        deflections = np.array([m[1] for m in self.measurements])

        # Split data into equal sections
        section_size = len(tensions) // self.pieces
        equations = []

        for i in range(self.pieces):
            start = i * section_size
            end = (start + section_size
                   if i < self.pieces - 1
                   else len(tensions))

            # Fit quartic polynomial for this section
            coeffs = np.polyfit(tensions[start:end], deflections[start:end], 4)
            coeffs_ascii = ",".join(f"{c:.10e}" for c in coeffs)

            # Store coefficients and range
            deflection_start = np.polyval(coeffs, tensions[start])
            deflection_end = np.polyval(coeffs, tensions[end - 1])

            # Adjust ranges to ensure continuity
            if i > 0:  # Ensure overlap with the previous range
                prev_range = equations[-1].split(";")[0]
                prev_start, prev_end = [float(x) for x in
                                        prev_range.split(",")]
                deflection_start = min(deflection_start, prev_end)

            range_ascii = f"{deflection_start:.10e},{deflection_end:.10e}"
            equations.append(f"{range_ascii};{coeffs_ascii}")

        # Extend the range by fitting quartic to the first and last pieces
        min_tension, max_tension = self.extend_range
        first_coeffs = np.polyfit(tensions[:section_size],
                                  deflections[:section_size],
                                  4)
        last_coeffs = np.polyfit(tensions[-section_size:],
                                 deflections[-section_size:],
                                 4)

        # Extend below
        extended_deflection_start = np.polyval(first_coeffs, min_tension)
        extended_range_start = \
            f"{extended_deflection_start:.10e}," \
            f"{np.polyval(first_coeffs, tensions[0]):.10e}"
        extended_coeffs_start = ",".join(f"{c:.10e}" for c in first_coeffs)
        equations.insert(0, f"{extended_range_start};{extended_coeffs_start}")

        # Extend above
        extended_deflection_end = np.polyval(last_coeffs, max_tension)
        extended_range_end = \
            f"{np.polyval(last_coeffs, tensions[-1]):.10e}," \
            f"{extended_deflection_end:.10e}"
        extended_coeffs_end = ",".join(f"{c:.10e}" for c in last_coeffs)
        equations.append(f"{extended_range_end};{extended_coeffs_end}")

        return "|".join(equations)

    def evaluate(self, deflection: float) -> float:
        """
        Takes a deflection value and calculates the corresponding tension.

        Parameters:
            deflection (float): Deflection value (mm).

        Returns:
            float: Calculated tension (N).
        """
        pieces = self.serialized_model.split("|")

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
                real_roots = [r.real for r in roots
                              if np.isreal(r) and r.real > 0]

                if not real_roots:
                    raise ValueError("No valid value.")

                # Return the smallest positive real root
                return min(real_roots)

        raise ValueError("Deflection out of range.")


# Example usage:
if __name__ == "__main__":
    # Example measurements
    example_measurements = [
        (1500, 3.1),
        (1400, 3.05),
        (1300, 3.01),
        (1200, 2.95),
        (1100, 2.89),
        (1000, 2.82),
        (900, 2.76),
        (800, 2.67),
        (700, 2.57),
        (600, 2.49),
        (500, 2.34),
        (400, 2.2)
    ]

    # Create PiecewiseQuarticFit object
    fit = PiecewiseQuarticFit(example_measurements)

    # Evaluate tension for a given deflection
    deflection_value = 3.06  # Example deflection
    tension = fit.evaluate(deflection_value)
    print(f"Tension for {deflection_value} mm deflection: {tension:.2f} N")
