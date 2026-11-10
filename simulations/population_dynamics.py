
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Make the project root accessible
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.dynamics import solve_dynamics


# Simulation parameters
times = np.linspace(0, 60, 601)

omega_0 = 1.0
t_0 = 5.0
sigma = 1.0
gamma = 0.1
gamma_phi = 0.02
delta = 0.0

# Solve the master equation
result = solve_dynamics(
    times,
    omega_0=omega_0,
    t_0=t_0,
    sigma=sigma,
    gamma=gamma,
    gamma_phi=gamma_phi,
    delta=delta,
)

population = result.expect[0]

# Plot the excited-state population
plt.figure(figsize=(8, 5))
plt.plot(times, population, linewidth=2, label="Excited-state population")

plt.xlabel("Time (1 / gamma units)")
plt.ylabel("Excited-state population")
plt.title("Population Dynamics of a Gaussian-Driven Two-Level Emitter")
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()

# Save the figure
output_path = PROJECT_ROOT / "figures" / "population_dynamics.png"
plt.savefig(output_path, dpi=300)
plt.close()

print(f"Figure saved to: {output_path}")
print(f"Maximum population: {np.max(population):.6f}")
print(f"Final population: {population[-1]:.6f}")
