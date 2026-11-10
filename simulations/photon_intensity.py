import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.dynamics import solve_dynamics
from src.model import projector_e


# Simulation parameters
times = np.linspace(0, 60, 601)

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

# Calculate photon emission intensity
population = result.expect[0]
intensity = gamma * population

# Plot the photon emission intensity
plt.figure(figsize=(8, 5))
plt.plot(times, intensity, linewidth=2)

plt.xlabel(r"Time $t$ ($1/\gamma$ units)")
plt.ylabel(r"Photon emission intensity $I(t)$")
plt.title("Time-Dependent Photon Emission Intensity")
plt.grid(alpha=0.3)
plt.tight_layout()

# Save the figure
output_path = PROJECT_ROOT / "figures" / "photon_intensity.png"
plt.savefig(output_path, dpi=300)
plt.close()

print(f"Figure saved to: {output_path}")
print(f"Maximum intensity: {np.max(intensity):.8e}")
print(f"Final intensity: {intensity[-1]:.8e}")