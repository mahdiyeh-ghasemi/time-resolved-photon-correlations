
import sys
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.dynamics import solve_dynamics
from src.correlations import time_resolved_g2


# Simulation parameters
times = np.linspace(0, 20, 41)
tau_values = np.linspace(0, 20, 41)

pulse_area = 1.0
t_0 = 5.0
gamma = 0.1
gamma_phi = 0.02
delta = 0.0

pulse_widths = [0.5, 1.0, 2.0]

# Numerical tolerances
tolerance = 1e-10

print("\nPhysical and Numerical Validation")
print("=" * 75)

all_checks_passed = True

for sigma in pulse_widths:

    omega_0 = pulse_area / (np.sqrt(2 * np.pi) * sigma)

    result = solve_dynamics(
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
        result.states,
        tau_values,
        omega_0=omega_0,
        t_0=t_0,
        sigma=sigma,
        gamma=gamma,
        gamma_phi=gamma_phi,
        delta=delta,
    )

    population = np.real(result.expect[0])

    # Check 1: G2(t, 0) should vanish for an ideal two-level emitter
    zero_delay_max = np.max(np.abs(g2[:, 0]))
    zero_delay_pass = zero_delay_max < tolerance

    # Check 2: G2 must not contain physically significant negative values
    minimum_g2 = np.min(g2)
    positivity_pass = minimum_g2 >= -tolerance

    # Check 3: Excited-state population must remain between 0 and 1
    min_population = np.min(population)
    max_population = np.max(population)

    population_pass = (
        min_population >= -tolerance
        and max_population <= 1 + tolerance
    )

    # Check 4: The population should decay after the pulse
    final_population = population[-1]
    decay_pass = final_population < max_population

    checks = [
        zero_delay_pass,
        positivity_pass,
        population_pass,
        decay_pass,
    ]

    if not all(checks):
        all_checks_passed = False

    print(f"\nPulse width sigma = {sigma:.2f}")
    print(f"Peak population:          {max_population:.8f}")
    print(f"Final population:         {final_population:.8f}")
    print(f"Max |G2(t, 0)|:           {zero_delay_max:.8e}")
    print(f"Minimum G2:               {minimum_g2:.8e}")

    print("\nValidation checks:")
    print(f"  G2(t, 0) approximately zero: {'PASS' if zero_delay_pass else 'FAIL'}")
    print(f"  G2 non-negative:             {'PASS' if positivity_pass else 'FAIL'}")
    print(f"  Population within [0, 1]:    {'PASS' if population_pass else 'FAIL'}")
    print(f"  Population decays:           {'PASS' if decay_pass else 'FAIL'}")


print("\n" + "=" * 75)

if all_checks_passed:
    print("Overall validation: ALL CHECKS PASSED")
else:
    print("Overall validation: SOME CHECKS FAILED")

print("Validation completed.")
