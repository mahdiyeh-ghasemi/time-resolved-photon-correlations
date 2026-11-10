
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

pulse_area = 1.0
t_0 = 5.0
gamma = 0.1
gamma_phi = 0.02
delta = 0.0

pulse_widths = [0.5, 1.0, 2.0]

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

for ax, sigma in zip(axes, pulse_widths):

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

    mesh = ax.pcolormesh(
        tau_values,
        times,
        g2,
        shading="auto",
        cmap="viridis",
    )

    ax.set_title(f"Pulse width σ = {sigma}")
    ax.set_xlabel("Delay τ")
    ax.set_ylabel("Detection time t")

    fig.colorbar(mesh, ax=ax, label="G²(t, τ)")

fig.suptitle(
    "Time-Resolved Photon Correlations\n"
    "Constant Gaussian Pulse Area",
    fontsize=14,
)

plt.tight_layout()

output_path = PROJECT_ROOT / "figures" / "g2_constant_area_comparison.png"
plt.savefig(output_path, dpi=300)
plt.close()

print(f"Figure saved to: {output_path}")
print("Constant-area correlation comparison completed.")
