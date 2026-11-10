
import sys
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.dynamics import solve_dynamics
from src.correlations import time_resolved_g2


# Physical parameters
pulse_area = 1.0
t_0 = 5.0
sigma = 1.0
omega_0 = pulse_area / (np.sqrt(2 * np.pi) * sigma)

gamma = 0.1
gamma_phi = 0.02
delta = 0.0

# Nested time-grid resolutions
grid_sizes = [41, 81, 161]

results = {}

print("\nNumerical Convergence Test")
print("=" * 65)

for n_points in grid_sizes:

    times = np.linspace(0, 20, n_points)
    tau_values = np.linspace(0, 20, n_points)

    dynamics = solve_dynamics(
        times,
        omega_0=omega_0,
        t_0=t_0,
        sigma=sigma,
        gamma=gamma,
        gamma_phi=gamma_phi,
        delta=delta,
    )

    g2 = time_resolved_g2(
        times,
        dynamics.states,
        tau_values,
        omega_0=omega_0,
        t_0=t_0,
        sigma=sigma,
        gamma=gamma,
        gamma_phi=gamma_phi,
        delta=delta,
    )

    population = np.real(dynamics.expect[0])

    results[n_points] = {
        "g2": g2,
        "population": population,
    }

    print(
        f"Grid: {n_points:3d} x {n_points:3d} | "
        f"Maximum G2: {np.max(g2):.8e} | "
        f"Maximum population: {np.max(population):.8f}"
    )


print("\nConvergence comparison")
print("-" * 65)

all_differences = []

for coarse_n, fine_n in [(41, 81), (81, 161)]:

    coarse = results[coarse_n]
    fine = results[fine_n]

    # Compare matching points on the nested grids
    fine_g2_sampled = fine["g2"][::2, ::2]
    fine_population_sampled = fine["population"][::2]

    g2_difference = np.max(
        np.abs(coarse["g2"] - fine_g2_sampled)
    )

    population_difference = np.max(
        np.abs(coarse["population"] - fine_population_sampled)
    )

    reference = np.max(np.abs(fine_g2_sampled))

    relative_g2_difference = (
        g2_difference / reference if reference > 0 else 0.0
    )

    all_differences.append(
        (g2_difference, population_difference)
    )

    print(f"\nComparison: {coarse_n} vs {fine_n} points")
    print(f"Maximum absolute G2 difference: {g2_difference:.8e}")
    print(f"Relative G2 difference:         {relative_g2_difference:.8e}")
    print(f"Maximum population difference:  {population_difference:.8e}")


print("\n" + "=" * 65)
print("Convergence test completed.")
