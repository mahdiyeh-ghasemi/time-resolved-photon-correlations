import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.dynamics import solve_dynamics
from src.correlations import time_resolved_g2


# Simulation parameters
times = np.linspace(0, 20, 41)
tau_values = np.linspace(0, 20, 41)

omega_0 = 1.0
t_0 = 5.0
sigma = 1.0
gamma = 0.1
gamma_phi = 0.02
delta = 0.0

# Solve the emitter dynamics
result = solve_dynamics(
    times,
    omega_0=omega_0,
    t_0=t_0,
    sigma=sigma,
    gamma=gamma,
    gamma_phi=gamma_phi,
    delta=delta,
)

# Calculate time-resolved photon correlations
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

# Plot the two-dimensional correlation map
plt.figure(figsize=(8, 6))

plt.pcolormesh(
    tau_values,
    times,
    g2,
    shading="auto",
    cmap="viridis",
)

plt.colorbar(label=r"$G^{(2)}(t,\tau)$")
plt.xlabel(r"Delay time $\tau$ ($1/\gamma$ units)")
plt.ylabel(r"First detection time $t$ ($1/\gamma$ units)")
plt.title("Time-Resolved Second-Order Photon Correlations")

plt.tight_layout()

# Save the figure
output_path = PROJECT_ROOT / "figures" / "time_resolved_g2.png"
plt.savefig(output_path, dpi=300)
plt.close()

print(f"Figure saved to: {output_path}")
print(f"G2 shape: {g2.shape}")
print(f"Maximum G2: {np.max(g2):.8e}")
print(f"G2 at zero delay: {np.max(np.abs(g2[:, 0])):.8e}")