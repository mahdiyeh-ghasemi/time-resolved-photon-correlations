
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.dynamics import solve_dynamics
from src.correlations import time_resolved_g2


# --------------------------------------------------
# 1. Simulation parameters
# --------------------------------------------------

times = np.linspace(0, 20, 321)
tau_values = np.linspace(0, 20, 321)

pulse_amplitudes = [0.5, 1.0, 2.0]
detuning_ratios = [0.0, 1.0, 3.0]

t_0 = 5.0
sigma = 1.0
gamma = 0.1
gamma_phi = 0.02

solver_options = {
    "atol": 1e-12,
    "rtol": 1e-10,
}

results = {}


# --------------------------------------------------
# 2. Run simulations
# --------------------------------------------------

print("\nIntensity-Detuning Analysis")
print("=" * 75)
print("Time grid: 321 x 321")
print("Solver tolerance: strict")
print("-" * 75)

for omega_0 in pulse_amplitudes:

    results[omega_0] = {}

    print(f"\nPulse amplitude Omega_0 = {omega_0:.1f}")

    for ratio in detuning_ratios:

        delta = ratio * gamma

        dynamics = solve_dynamics(
            times=times,
            omega_0=omega_0,
            t_0=t_0,
            sigma=sigma,
            gamma=gamma,
            gamma_phi=gamma_phi,
            delta=delta,
            solver_options=solver_options,
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
            solver_options=solver_options,
        )

        max_population = float(np.max(population))
        max_g2 = float(np.max(g2))

        results[omega_0][ratio] = {
            "max_population": max_population,
            "max_g2": max_g2,
        }

        print(
            f"Delta/gamma = {ratio:.1f} | "
            f"Maximum population = {max_population:.10e} | "
            f"Maximum G2 = {max_g2:.10e}"
        )


# --------------------------------------------------
# 3. Relative changes from resonance
# --------------------------------------------------

print("\nRelative changes compared with resonance")
print("-" * 75)
print(
    "Omega_0 | Delta/gamma | "
    "Population change (%) | G2 change (%)"
)

for omega_0 in pulse_amplitudes:

    baseline_population = (
        results[omega_0][0.0]["max_population"]
    )
    baseline_g2 = results[omega_0][0.0]["max_g2"]

    for ratio in detuning_ratios:

        current_population = (
            results[omega_0][ratio]["max_population"]
        )
        current_g2 = results[omega_0][ratio]["max_g2"]

        population_change = (
            current_population / baseline_population - 1
        ) * 100

        g2_change = (
            current_g2 / baseline_g2 - 1
        ) * 100

        print(
            f"{omega_0:7.1f} | "
            f"{ratio:11.1f} | "
            f"{population_change:21.4f} | "
            f"{g2_change:14.4f}"
        )


# --------------------------------------------------
# 4. Prepare figure directory
# --------------------------------------------------

figures_dir = PROJECT_ROOT / "figures"
figures_dir.mkdir(exist_ok=True)


# --------------------------------------------------
# 5. Plot maximum excited-state population
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(8, 5))

for omega_0 in pulse_amplitudes:

    values = [
        results[omega_0][ratio]["max_population"]
        for ratio in detuning_ratios
    ]

    ax.plot(
        detuning_ratios,
        values,
        marker="o",
        linewidth=2,
        label=rf"$\Omega_0={omega_0:.1f}$",
    )

ax.set_xlabel(r"Detuning $\Delta/\gamma$")
ax.set_ylabel("Maximum excited-state population")
ax.set_title(
    "Population Response to Detuning at Different Pulse Amplitudes"
)
ax.grid(True, alpha=0.3)
ax.legend()

fig.tight_layout()
fig.savefig(
    figures_dir / "intensity_detuning_population.png",
    dpi=300,
)
plt.close(fig)


# --------------------------------------------------
# 6. Plot maximum unnormalized G2
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(8, 5))

for omega_0 in pulse_amplitudes:

    values = [
        results[omega_0][ratio]["max_g2"]
        for ratio in detuning_ratios
    ]

    ax.plot(
        detuning_ratios,
        values,
        marker="o",
        linewidth=2,
        label=rf"$\Omega_0={omega_0:.1f}$",
    )

ax.set_xlabel(r"Detuning $\Delta/\gamma$")
ax.set_ylabel("Maximum unnormalized G2")
ax.set_title(
    "Photon Correlation Response to Detuning at Different Pulse Amplitudes"
)
ax.grid(True, alpha=0.3)
ax.legend()

fig.tight_layout()
fig.savefig(
    figures_dir / "intensity_detuning_g2.png",
    dpi=300,
)
plt.close(fig)


# --------------------------------------------------
# 7. Completion
# --------------------------------------------------

print("\n" + "=" * 75)
print("Intensity-detuning analysis completed.")
print("Figures saved:")
print("figures/intensity_detuning_population.png")
print("figures/intensity_detuning_g2.png")
