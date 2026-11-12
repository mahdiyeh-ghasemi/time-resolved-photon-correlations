
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

times = np.linspace(0, 20, 41)
tau_values = np.linspace(0, 20, 41)

omega_0 = 1.0
t_0 = 5.0
sigma = 1.0
gamma = 0.1
gamma_phi = 0.02

detuning_ratios = [0.0, 1.0, 3.0]
selected_times = [4.0, 5.0, 6.0, 7.0]

results = {}


# --------------------------------------------------
# 2. Calculate G2 for each detuning
# --------------------------------------------------

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
    )

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

    results[ratio] = g2


# --------------------------------------------------
# 3. Normalize profiles at selected times
# --------------------------------------------------

normalized_profiles = {}

for selected_time in selected_times:

    time_index = np.argmin(
        np.abs(times - selected_time)
    )

    actual_time = times[time_index]

    normalized_profiles[actual_time] = {}

    for ratio in detuning_ratios:

        profile = results[ratio][time_index, :]
        profile_max = np.max(profile)

        if profile_max <= 0:
            raise ValueError(
                f"Non-positive maximum at t={actual_time}, "
                f"Delta/gamma={ratio}"
            )

        normalized_profiles[actual_time][ratio] = (
            profile / profile_max
        )


# --------------------------------------------------
# 4. Plot normalized profiles
# --------------------------------------------------

figures_dir = PROJECT_ROOT / "figures"
figures_dir.mkdir(exist_ok=True)

fig, axes = plt.subplots(
    2, 2,
    figsize=(12, 9),
    sharex=True,
    sharey=True,
    constrained_layout=True,
)

axes = axes.flatten()

for ax, selected_time in zip(axes, normalized_profiles):

    for ratio in detuning_ratios:

        ax.plot(
            tau_values,
            normalized_profiles[selected_time][ratio],
            marker="o",
            markersize=2.5,
            label=rf"$\Delta/\gamma={ratio:.1f}$",
        )

    ax.set_title(rf"Detection time $t={selected_time:.1f}$")
    ax.set_xlabel(r"Delay time $\tau$")
    ax.set_ylabel("Normalized correlation")
    ax.set_ylim(0, 1.05)
    ax.grid(True, alpha=0.3)
    ax.legend()

fig.suptitle(
    "Normalized Correlation Profiles at Different Detection Times"
)

fig.savefig(
    figures_dir / "g2_detuning_time_dependence.png",
    dpi=300,
)

plt.close(fig)


# --------------------------------------------------
# 5. Calculate RMS differences
# --------------------------------------------------

print("\nRMS differences from resonant profiles")
print("Detection time | Delta/gamma | RMS difference")

for selected_time in normalized_profiles:

    reference = normalized_profiles[selected_time][0.0]

    for ratio in detuning_ratios:

        profile = normalized_profiles[selected_time][ratio]

        rms_difference = np.sqrt(
            np.mean((profile - reference) ** 2)
        )

        print(
            f"{selected_time:14.1f} | "
            f"{ratio:11.1f} | "
            f"{rms_difference:14.8e}"
        )


# --------------------------------------------------
# 6. Completion message
# --------------------------------------------------

print("\nTime-dependent detuning analysis completed.")
print("Figure saved: figures/g2_detuning_time_dependence.png")
