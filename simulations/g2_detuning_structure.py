
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

# Selected detuning values
detuning_ratios = [0.0, 1.0, 3.0]
detunings = [ratio * gamma for ratio in detuning_ratios]

results = {}

# Run simulations
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

    print(
        f"Delta/gamma = {ratio:.1f} | "
        f"Maximum G2 = {np.max(g2):.8e}"
    )


# Create output directory
figures_dir = PROJECT_ROOT / "figures"
figures_dir.mkdir(exist_ok=True)


# Plot time-resolved G2 maps
fig, axes = plt.subplots(
    1, 3,
    figsize=(16, 5),
    sharex=True,
    sharey=True,
    constrained_layout=True,
)

vmax = max(np.max(g2) for g2 in results.values())

for ax, ratio in zip(axes, detuning_ratios):

    mesh = ax.pcolormesh(
        tau_values,
        times,
        results[ratio],
        shading="auto",
        cmap="viridis",
        vmin=0,
        vmax=vmax,
    )

    ax.set_title(rf"$\Delta/\gamma = {ratio:.1f}$")
    ax.set_xlabel(r"Delay time $\tau$")

axes[0].set_ylabel(r"Detection time $t$")

fig.colorbar(
    mesh,
    ax=axes,
    label=r"Unnormalized $G^{(2)}(t,\tau)$",
)

fig.suptitle("Time-Resolved Photon Correlations at Different Detunings")

fig.savefig(
    figures_dir / "g2_detuning_maps.png",
    dpi=300,
)
plt.close(fig)


# Compare temporal correlation profiles
# Select the detection time closest to the pulse center
selected_time = 5.0
time_index = np.argmin(np.abs(times - selected_time))

plt.figure(figsize=(8, 5))

for ratio in detuning_ratios:

    plt.plot(
        tau_values,
        results[ratio][time_index, :],
        marker="o",
        markersize=3,
        label=rf"$\Delta/\gamma = {ratio:.1f}$",
    )

plt.xlabel(r"Delay time $\tau$")
plt.ylabel(r"Unnormalized $G^{(2)}(t,\tau)$")
plt.title(
    rf"Correlation Profiles at $t = {times[time_index]:.1f}$"
)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    figures_dir / "g2_detuning_profiles.png",
    dpi=300,
)
plt.close()


# Quantitative comparison of correlation profiles
print("\nCorrelation profile comparison:")
print(f"Selected detection time: t = {times[time_index]:.2f}")
print("Delta/gamma | Profile maximum | Profile integral")

for ratio in detuning_ratios:

    profile = results[ratio][time_index, :]

    profile_max = np.max(profile)
    profile_integral = np.trapezoid(profile, tau_values)

    print(
        f"{ratio:11.1f} | "
        f"{profile_max:15.8e} | "
        f"{profile_integral:16.8e}"
    )


print("\nTime-resolved detuning analysis completed.")
print("Figures saved in the figures/ directory.")
