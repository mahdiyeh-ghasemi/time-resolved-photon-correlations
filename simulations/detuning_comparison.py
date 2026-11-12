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

# Detuning values
detunings = [0.0, gamma, 2 * gamma]

results = {}

for delta in detunings:
    dynamics = solve_dynamics(
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
        dynamics.states,
        tau_values,
        omega_0=omega_0,
        t_0=t_0,
        sigma=sigma,
        gamma=gamma,
        gamma_phi=gamma_phi,
        delta=delta,
    )

    results[delta] = {
        "population": np.real(dynamics.expect[0]),
        "g2": g2,
    }

    print(
        f"Delta = {delta:.3f} | "
        f"Maximum excited-state population = "
        f"{np.max(np.real(dynamics.expect[0])):.8e} | "
        f"Maximum G2 = {np.max(g2):.8e}"
    )

# Relative changes with respect to the resonant case
baseline_population = np.max(results[0.0]["population"])
baseline_g2 = np.max(results[0.0]["g2"])

print("\nRelative changes compared with resonance:")

for delta in detunings:
    population_max = np.max(results[delta]["population"])
    g2_max = np.max(results[delta]["g2"])

    population_change = (
        (population_max - baseline_population)
        / baseline_population
    ) * 100

    g2_change = (
        (g2_max - baseline_g2)
        / baseline_g2
    ) * 100

    print(
        f"Delta = {delta:.3f} | "
        f"Population change = {population_change:.3f}% | "
        f"G2 change = {g2_change:.3f}%"
    )


# Create output directory
figures_dir = PROJECT_ROOT / "figures"
figures_dir.mkdir(exist_ok=True)


# 1. Excited-state population comparison
plt.figure(figsize=(8, 5))

for delta in detunings:
    plt.plot(
        times,
        results[delta]["population"],
        label=fr"$\Delta={delta:.2f}$",
    )

plt.xlabel(r"Time ($1/\gamma$ units)")
plt.ylabel("Excited-state population")
plt.title("Effect of Detuning on Emitter Population")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(
    figures_dir / "detuning_population_comparison.png",
    dpi=300,
)
plt.close()


# 2. Time-resolved G2 comparison
fig, axes = plt.subplots(
    1, 3,
    figsize=(15, 4.5),
    sharex=True,
    sharey=True,
    constrained_layout=True,
)

vmax = max(
    np.max(results[delta]["g2"])
    for delta in detunings
)

for ax, delta in zip(axes, detunings):
    mesh = ax.pcolormesh(
        tau_values,
        times,
        results[delta]["g2"],
        shading="auto",
        cmap="viridis",
        vmin=0,
        vmax=vmax,
    )

    ax.set_title(fr"$\Delta={delta:.2f}$")
    ax.set_xlabel(r"Delay time $\tau$")

axes[0].set_ylabel(r"First detection time $t$")

fig.colorbar(
    mesh,
    ax=axes,
    label=r"$G^{(2)}(t,\tau)$",
)

fig.suptitle("Effect of Detuning on Time-Resolved Photon Correlations")

fig.savefig(
    figures_dir / "detuning_g2_comparison.png",
    dpi=300,
)
plt.close(fig)

print("\nFigures saved:")
print("figures/detuning_population_comparison.png")
print("figures/detuning_g2_comparison.png")