
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.dynamics import solve_dynamics
from src.correlations import time_resolved_g2


# Common simulation parameters
times = np.linspace(0, 20, 41)
tau_values = np.linspace(0, 20, 41)

omega_0 = 1.0
t_0 = 5.0
sigma = 1.0
gamma = 0.1
gamma_phi = 0.02

# Detuning values expressed in units of gamma
detuning_ratios = np.array(
    [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
)

detunings = detuning_ratios * gamma

maximum_populations = []
maximum_g2_values = []

# Run simulations for all detuning values
for ratio, delta in zip(detuning_ratios, detunings):

    dynamics = solve_dynamics(
        times=times,
        omega_0=omega_0,
        t_0=t_0,
        sigma=sigma,
        gamma=gamma,
        gamma_phi=gamma_phi,
        delta=delta,
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
    )

    max_population = float(np.max(population))
    max_g2 = float(np.max(g2))

    maximum_populations.append(max_population)
    maximum_g2_values.append(max_g2)

    print(
        f"Delta/gamma = {ratio:.1f} | "
        f"Maximum population = {max_population:.8e} | "
        f"Maximum G2 = {max_g2:.8e}"
    )


# Calculate percentage changes relative to resonance
baseline_population = maximum_populations[0]
baseline_g2 = maximum_g2_values[0]

population_changes = (
    (np.array(maximum_populations) / baseline_population) - 1
) * 100

g2_changes = (
    (np.array(maximum_g2_values) / baseline_g2) - 1
) * 100


# Print relative changes
print("\nRelative changes compared with resonance:")
print("Delta/gamma | Population change (%) | G2 change (%)")

for ratio, pop_change, g2_change in zip(
    detuning_ratios, population_changes, g2_changes
):
    print(
        f"{ratio:11.1f} | "
        f"{pop_change:21.3f} | "
        f"{g2_change:14.3f}"
    )


# Create output directory
figures_dir = PROJECT_ROOT / "figures"
figures_dir.mkdir(exist_ok=True)


# Plot population changes
plt.figure(figsize=(7, 5))

plt.plot(
    detuning_ratios,
    population_changes,
    marker="o",
)

plt.xlabel(r"Detuning $\Delta/\gamma$")
plt.ylabel("Change in maximum excited-state population (%)")
plt.title("Population Sensitivity to Detuning")
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    figures_dir / "detuning_population_sweep.png",
    dpi=300,
)
plt.close()


# Plot unnormalized G2 changes
plt.figure(figsize=(7, 5))

plt.plot(
    detuning_ratios,
    g2_changes,
    marker="o",
)

plt.xlabel(r"Detuning $\Delta/\gamma$")
plt.ylabel("Change in maximum unnormalized G2 (%)")
plt.title("Second-Order Correlation Sensitivity to Detuning")
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    figures_dir / "detuning_g2_sweep.png",
    dpi=300,
)
plt.close()


print("\nDetuning sweep completed.")
print("Figures saved in the figures/ directory.")
