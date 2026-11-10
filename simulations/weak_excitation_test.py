
import numpy as np

from src.dynamics import solve_dynamics
from src.correlations import time_resolved_g2


times = np.linspace(0, 20, 81)
tau_values = np.linspace(0, 20, 81)

t_0 = 5
sigma = 1
gamma = 0.1
gamma_phi = 0.02
delta = 0.0

pulse_areas = [0.4, 0.2, 0.1]

results = []

for area in pulse_areas:
    omega_0 = area / (np.sqrt(2 * np.pi) * sigma)

    dynamics = solve_dynamics(
        times, omega_0, t_0, sigma, gamma, gamma_phi, delta
    )

    populations = np.real(dynamics.expect[0])

    g2 = time_resolved_g2(
        times,
        dynamics.states,
        tau_values,
        omega_0,
        t_0,
        sigma,
        gamma,
        gamma_phi,
        delta,
    )

    max_population = np.max(populations)
    max_g2 = np.max(g2)

    results.append((area, max_population, max_g2))

print("\nWeak Excitation Scaling Test")
print("-" * 65)
print(f"{'Pulse Area':<15}{'Max Population':<22}{'Max G2':<20}")

for area, population, g2_value in results:
    print(f"{area:<15.2f}{population:<22.8e}{g2_value:<20.8e}")

print("\nScaling Ratios")
for i in range(len(results) - 1):
    p_ratio = results[i + 1][1] / results[i][1]
    g_ratio = results[i + 1][2] / results[i][2]

    print(f"Area ratio: 0.5")
    print(f"Population ratio: {p_ratio:.6f}")
    print(f"G2 ratio: {g_ratio:.6f}")
    print()

