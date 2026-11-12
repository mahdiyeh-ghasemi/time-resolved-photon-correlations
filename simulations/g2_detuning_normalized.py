
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

results = {}


# --------------------------------------------------
# 2. Calculate time-resolved G2
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
# 3. Select detection time
# --------------------------------------------------

selected_time = 5.0
time_index = np.argmin(np.abs(times - selected_time))

print(f"Selected detection time: t = {times[time_index]:.2f}")


# --------------------------------------------------
# 4. Normalize correlation profiles
# --------------------------------------------------

normalized_profiles = {}

for ratio in detuning_ratios:

    profile = results[ratio][time_index, :]
    profile_max = np.max(profile)

    if profile_max <= 0:
        raise ValueError(
            f"Non-positive profile maximum for Delta/gamma = {ratio}"
        )

    normalized_profiles[ratio] = profile / profile_max


# --------------------------------------------------
# 5. Plot normalized profiles
# --------------------------------------------------

figures_dir = PROJECT_ROOT / "figures"
figures_dir.mkdir(exist_ok=True)

plt.figure(figsize=(8, 5))

for ratio in detuning_ratios:

    plt.plot(
        tau_values,
        normalized_profiles[ratio],
        marker="o",
        markersize=3,
        label=rf"$\Delta/\gamma = {ratio:.1f}$",
    )

plt.xlabel(r"Delay time $\tau$")
plt.ylabel("Normalized correlation profile")
plt.title(
    rf"Normalized Correlation Profiles at $t = {times[time_index]:.1f}$"
)
plt.ylim(0, 1.05)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    figures_dir / "g2_detuning_normalized_profiles.png",
    dpi=300,
)
plt.close()


# --------------------------------------------------
# 6. Calculate normalized profile areas
# --------------------------------------------------

print("\nNormalized profile comparison:")
print("Delta/gamma | Normalized profile area")

for ratio in detuning_ratios:

    area = np.trapezoid(
        normalized_profiles[ratio],
        tau_values,
    )

    print(f"{ratio:11.1f} | {area:24.8f}")


# --------------------------------------------------
# 7. Calculate RMS differences
# --------------------------------------------------

reference_profile = normalized_profiles[0.0]

print("\nRMS difference from resonant profile:")
print("Delta/gamma | RMS difference")

for ratio in detuning_ratios:

    profile = normalized_profiles[ratio]

    rms_difference = np.sqrt(
        np.mean((profile - reference_profile) ** 2)
    )

    print(
        f"{ratio:11.1f} | "
        f"{rms_difference:14.8e}"
    )


# --------------------------------------------------
# 8. Completion message
# --------------------------------------------------

print("\nNormalized detuning analysis completed.")
print("Figure saved: figures/g2_detuning_normalized_profiles.png")
