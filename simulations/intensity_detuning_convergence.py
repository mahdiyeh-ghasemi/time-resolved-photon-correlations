
import sys
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.dynamics import solve_dynamics
from src.correlations import time_resolved_g2


# Physical parameters
pulse_amplitudes = [0.5, 1.0, 2.0]
detuning_ratios = [0.0, 1.0, 3.0]
grid_sizes = [161, 321]

t_0 = 5.0
sigma = 1.0
gamma = 0.1
gamma_phi = 0.02

solver_options = {
    "atol": 1e-12,
    "rtol": 1e-10,
}

results = {}

print("\nIntensity-Detuning Grid Refinement Test")
print("=" * 85)
print("Solver tolerance: strict")
print("Grid sizes: 161 and 321 points")
print("-" * 85)


# Run simulations
for omega_0 in pulse_amplitudes:
    for ratio in detuning_ratios:

        delta = ratio * gamma
        key = (omega_0, ratio)
        results[key] = {}

        print(
            f"\nOmega_0 = {omega_0:.1f}, "
            f"Delta/gamma = {ratio:.1f}"
        )

        for n_points in grid_sizes:

            times = np.linspace(0, 20, n_points)
            tau_values = np.linspace(0, 20, n_points)

            dynamics = solve_dynamics(
                times=times,
                omega_0=omega_0,
                t_0=t_0,
                sigma=sigma,
                gamma=gamma,
                gamma_phi=gamma_phi,
                delta=delta,
                solver_options=solver_options,
            )

            population = np.real(dynamics.expect[0])

            g2 = time_resolved_g2(
                times=times,
                rho_states=dynamics.states,
                tau_values=tau_values,
                omega_0=omega_0,
                t_0=t_0,
                sigma=sigma,
                gamma=gamma,
                gamma_phi=gamma_phi,
                delta=delta,
                solver_options=solver_options,
            )

            results[key][n_points] = {
                "max_population": float(np.max(population)),
                "max_g2": float(np.max(g2)),
            }

            print(
                f"Grid = {n_points:3d} | "
                f"Maximum population = {np.max(population):.10e} | "
                f"Maximum G2 = {np.max(g2):.10e}"
            )


# Compare the maxima
print("\n\nGrid refinement comparison")
print("=" * 85)

for omega_0 in pulse_amplitudes:
    for ratio in detuning_ratios:

        coarse = results[(omega_0, ratio)][161]
        fine = results[(omega_0, ratio)][321]

        population_difference = abs(
            fine["max_population"] - coarse["max_population"]
        )

        g2_difference = abs(
            fine["max_g2"] - coarse["max_g2"]
        )

        population_relative = (
            population_difference / abs(fine["max_population"])
        ) * 100

        g2_relative = (
            g2_difference / abs(fine["max_g2"])
        ) * 100

        print(
            f"\nOmega_0 = {omega_0:.1f}, "
            f"Delta/gamma = {ratio:.1f}"
        )
        print(
            f"Population difference: {population_difference:.6e} "
            f"({population_relative:.5f}%)"
        )
        print(
            f"G2 difference: {g2_difference:.6e} "
            f"({g2_relative:.5f}%)"
        )


print("\n" + "=" * 85)
print("Grid refinement test completed.")
