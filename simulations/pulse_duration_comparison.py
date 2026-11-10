import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.dynamics import solve_dynamics


# Common simulation parameters
times = np.linspace(0, 60, 601)

omega_0 = 1.0
t_0 = 10.0
gamma = 0.1
gamma_phi = 0.02
delta = 0.0

# Pulse widths to compare
pulse_widths = [0.5, 1.0, 2.0]

plt.figure(figsize=(8, 5))

for sigma in pulse_widths:

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

    plt.plot(
        times,
        population,
        linewidth=2,
        label=rf"$\sigma={sigma}$",
    )

plt.xlabel(r"Time $t$ ($1/\gamma$ units)")
plt.ylabel("Excited-state population")
plt.title("Effect of Pulse Duration on Emitter Dynamics")
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()

# Save the figure
output_path = PROJECT_ROOT / "figures" / "pulse_duration_comparison.png"
plt.savefig(output_path, dpi=300)
plt.close()

print(f"Figure saved to: {output_path}")
print("Pulse-duration comparison completed.")