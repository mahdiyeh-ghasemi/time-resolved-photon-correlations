
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

# Fixed time grids
times = np.linspace(0, 20, 81)
tau_values = np.linspace(0, 20, 81)

# Solver tolerance levels
tolerance_levels = {
    "default": {"atol": 1e-8, "rtol": 1e-6},
    "tight": {"atol": 1e-10, "rtol": 1e-8},
    "strict": {"atol": 1e-12, "rtol": 1e-10},
}

results = {}

print("\nSolver Tolerance Sensitivity Test")
print("=" * 65)

# Run simulations
for label, options in tolerance_levels.items():

    dynamics = solve_dynamics(
        times,
        omega_0=omega_0,
        t_0=t_0,
        sigma=sigma,
        gamma=gamma,
        gamma_phi=gamma_phi,
        delta=delta,
        solver_options=options,
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
        solver_options=options,
    )

    population = np.real(dynamics.expect[0])

    results[label] = {
        "g2": g2,
        "population": population,
    }

    print(
        f"{label:8s} | "
        f"Maximum G2: {np.max(g2):.10e} | "
        f"Maximum population: {np.max(population):.10f}"
    )


# Compare tighter tolerances with default
print("\nComparison with default tolerances")
print("=" * 65)

reference = results["default"]

for label in ["tight", "strict"]:

    g2_difference = np.max(
        np.abs(results[label]["g2"] - reference["g2"])
    )

    population_difference = np.max(
        np.abs(results[label]["population"] - reference["population"])
    )

    g2_relative = g2_difference / max(
        np.max(np.abs(reference["g2"])), 1e-15
    )

    population_relative = population_difference / max(
        np.max(np.abs(reference["population"])), 1e-15
    )

    print(
        f"{label:8s} | "
        f"Max G2 difference: {g2_difference:.10e} | "
        f"Relative: {g2_relative:.10e}"
    )

    print(
        f"{'':8s} | "
        f"Max population difference: {population_difference:.10e} | "
        f"Relative: {population_relative:.10e}"
    )


# Check the zero-delay correlation
print("\nZero-delay correlation check")
print("=" * 65)

for label, data in results.items():

    zero_delay_error = np.max(np.abs(data["g2"][:, 0]))

    print(
        f"{label:8s} | "
        f"Maximum |G2(t, 0)|: {zero_delay_error:.10e}"
    )
