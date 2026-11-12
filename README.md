
# Time-Resolved Photon Correlations in Driven Quantum Systems

## Project Overview

This project investigates time-resolved photon correlations emitted by a driven quantum emitter under pulsed excitation.

The initial study uses a driven two-level quantum system as a minimal theoretical model. Its dynamics are described using the Lindblad master equation, with particular attention to the temporal structure of second-order photon correlations.

The computational framework is used to examine how pulse duration, pulse amplitude, and frequency detuning influence the emitter dynamics and photon correlations.

## Research Questions

- How do pulse duration and excitation strength affect time-resolved photon correlations?
- How does frequency detuning modify the excited-state population and photon-correlation signal?
- Does the sensitivity to detuning depend on the driving-pulse amplitude?

## Methodology

- Model a driven two-level quantum emitter.
- Implement time-dependent Gaussian pulsed excitation.
- Solve the open-system dynamics using the Lindblad master equation.
- Calculate time-resolved, unnormalized second-order photon correlations.
- Investigate pulse-duration and pulse-amplitude dependence.
- Examine the effects of frequency detuning.
- Test numerical stability through solver-tolerance and temporal-grid refinement studies.

## Scope

The initial stage focuses on a minimal two-level emitter model. More complex systems and additional physical effects may be considered in later extensions.

## Project Status

The research model and computational framework have been implemented and tested through numerical consistency, solver-tolerance, and grid-refinement studies.

## Theoretical Model

The system is modeled as a driven two-level quantum emitter with ground state $|g\rangle$ and excited state $|e\rangle$.

In the rotating frame and using $\hbar=1$, the Hamiltonian is

$$
H(t)=\Delta\sigma_+\sigma_-+
\frac{\Omega(t)}{2}(\sigma_++\sigma_-).
$$

The Gaussian driving pulse is

$$
\Omega(t)=\Omega_0
\exp\left[-\frac{(t-t_0)^2}{2\sigma^2}\right].
$$

The open-system dynamics are described by the Lindblad master equation:

$$
\dot{\rho}=-i[H(t),\rho]
+\gamma\mathcal{D}[\sigma_-]\rho
+\frac{\gamma_\phi}{2}\mathcal{D}[\sigma_z]\rho.
$$

Here, $\gamma$ describes spontaneous emission, while $\gamma_\phi$ is the pure-dephasing rate.

The Lindblad dissipator is defined as

$$
\mathcal{D}[c]\rho =
c\rho c^\dagger -
\frac{1}{2}(c^\dagger c\rho+\rho c^\dagger c).
$$

## Numerical Validation

The computational implementation was examined through several numerical tests:

- Population dynamics and spontaneous-emission behavior.
- Zero-delay suppression of the second-order correlation for the two-level emitter.
- Positivity of the calculated second-order correlation within numerical tolerance.
- Convergence with respect to temporal-grid refinement.
- Weak-excitation scaling of population and photon correlations.
- Sensitivity of the numerical results to solver tolerances.

For weak excitation, the numerical results are consistent with

$$
P_e^{\max}\propto A^2,
\qquad
G_{\max}^{(2)}\propto A^4,
$$

where $A$ is the Gaussian pulse area.

### Solver Tolerance Sensitivity

The solver tolerance sensitivity was tested using three absolute and relative tolerance settings:

| Setting | Absolute tolerance | Relative tolerance |
|---|---:|---:|
| Default | $10^{-8}$ | $10^{-6}$ |
| Tight | $10^{-10}$ | $10^{-8}$ |
| Strict | $10^{-12}$ | $10^{-10}$ |

The maximum absolute difference in the second-order correlation relative to the default setting was approximately $2.39\times10^{-9}$ for both tighter settings. The maximum relative difference was approximately $8.6\times10^{-5}$.

The corresponding maximum population difference was below $2.9\times10^{-7}$.

The tight and strict settings produced nearly identical results, indicating numerical stability with respect to further tightening of the solver tolerances for the parameters considered.

The zero-delay condition,

$$
G^{(2)}(t,0)=0,
$$

was also satisfied to numerical precision for all three tolerance settings.

### Temporal Grid Refinement

A grid-refinement test was performed using 161 and 321 time points, with strict solver tolerances:

$$
\mathrm{atol}=10^{-12},
\qquad
\mathrm{rtol}=10^{-10}.
$$

The comparison covered three pulse amplitudes and three detuning values.

The maximum relative difference between the sampled maxima obtained with the two grids was approximately:

- $0.267\%$ for the excited-state population.
- $0.023\%$ for the unnormalized second-order correlation.

These results indicate good numerical agreement for the sampled maxima at the selected resolutions. They do not, by themselves, establish convergence of every point in the full time-dependent correlation map.

## Results

The simulations examine the population dynamics, emission intensity, and time-resolved second-order photon correlations of a driven two-level emitter.

### Population Dynamics

The time evolution of the excited-state population illustrates the emitter's response to the Gaussian driving pulse and its subsequent relaxation through spontaneous emission.

![Excited-state population dynamics](figures/population_dynamics.png)

### Photon Emission Intensity

The emission intensity is obtained from the excited-state population and the spontaneous emission rate, illustrating the temporal profile of photon emission.

![Time-dependent photon emission intensity](figures/photon_intensity.png)

### Time-Resolved Photon Correlations

The second-order correlation function $G^{(2)}(t,\tau)$ describes the time-dependent conditional photon-emission signal following pulsed excitation.

The quantity calculated in the current implementation is unnormalized. It should therefore be distinguished from the normalized correlation function $g^{(2)}(t,\tau)$.

![Time-resolved second-order photon correlation](figures/time_resolved_g2.png)

### Pulse-Duration Dependence

A comparison was performed for Gaussian driving pulses with different temporal widths while keeping the pulse area constant at $A=1$. The pulse amplitudes were adjusted according to

$$
\Omega_0=\frac{A}{\sqrt{2\pi}\sigma}.
$$

For pulse widths $\sigma=0.5,\ 1.0,\ 2.0$, the maximum values of the time-resolved correlation function were approximately:

| Pulse width $\sigma$ | Maximum $G^{(2)}$ | Peak delay |
|---:|---:|---:|
| 0.5 | $3.17\times10^{-5}$ | 1.5 |
| 1.0 | $2.78\times10^{-5}$ | 2.5 |
| 2.0 | $2.13\times10^{-5}$ | 4.0 |

For the parameters considered here, increasing the pulse width reduces the peak correlation value and shifts the peak toward longer delays. These results illustrate how the temporal profile of the excitation can influence the emission correlations, even when the pulse area is held fixed.

![Population dynamics for different pulse durations](figures/pulse_duration_comparison.png)

![Photon correlation comparison at constant pulse area](figures/g2_constant_area_comparison.png)

### Detuning Dependence

The effect of frequency detuning was investigated by varying the dimensionless ratio

$$
\frac{\Delta}{\gamma}
$$

while keeping the other physical parameters fixed.

A detuning sweep was performed over

$$
\frac{\Delta}{\gamma}
=
0,\ 0.5,\ 1,\ 1.5,\ 2,\ 2.5,\ 3.
$$

For the selected parameter set, increasing detuning reduced both the maximum excited-state population and the maximum unnormalized second-order correlation.

At $\Delta=3\gamma$, the maximum population decreased by approximately $7.14\%$ relative to the resonant case, while the maximum unnormalized correlation decreased by approximately $5.85\%$.

![Excited-state population across the detuning sweep](figures/detuning_population_sweep.png)

![Maximum unnormalized correlation across the detuning sweep](figures/detuning_g2_sweep.png)

The full time-resolved correlation maps were also compared at selected detunings.

![Time-resolved correlation maps for different detunings](figures/g2_detuning_maps.png)

### Detuning Dependence of Correlation Profiles

To examine changes in the temporal profile separately from changes in its overall magnitude, correlation profiles were normalized by their own maximum values at selected detection times.

This profile normalization is used only to compare shapes; it is not the standard intensity-normalized photon correlation function $g^{(2)}$.

At the selected detection time $t=5$, the normalized profiles showed relatively small differences across the tested detunings. The root-mean-square difference from the resonant profile increased with detuning.

![Normalized correlation profiles at selected detunings](figures/g2_detuning_normalized_profiles.png)

The time dependence of this profile-shape difference was also investigated at detection times $t=4,\ 5,\ 6,\ 7$.

For the chosen parameters, the differences were more pronounced at earlier detection times and became smaller at later times.

![Time dependence of normalized detuning profiles](figures/g2_detuning_time_dependence.png)

### Pulse-Amplitude and Detuning Dependence

The combined influence of pulse amplitude and frequency detuning was investigated using three peak Rabi frequencies:

$$
\Omega_0=0.5,\ 1.0,\ 2.0.
$$

For each pulse amplitude, the detuning was varied over

$$
\frac{\Delta}{\gamma}=0,\ 1,\ 3.
$$

The simulations used a 321-point temporal grid and strict solver tolerances.

The following table summarizes the relative changes in the maximum excited-state population and maximum unnormalized second-order correlation compared with the resonant case at the same pulse amplitude.

| $\Omega_0$ | $\Delta/\gamma$ | Population change (%) | $G_{\max}^{(2)}$ change (%) |
|---:|---:|---:|---:|
| 0.5 | 1 | -0.8675 | -0.6505 |
| 0.5 | 3 | -7.5270 | -5.6817 |
| 1.0 | 1 | -0.8511 | -0.6482 |
| 1.0 | 3 | -7.3299 | -5.6800 |
| 2.0 | 1 | -0.4426 | -0.6354 |
| 2.0 | 3 | -3.9047 | -5.5623 |

For the parameter set considered, increasing the pulse amplitude reduced the relative sensitivity of the maximum excited-state population to detuning. The relative change in the maximum unnormalized correlation remained within a similar range across the three pulse amplitudes.

These observations are specific to the present two-level model and parameter range and should not be interpreted as universal behavior.

![Maximum excited-state population versus detuning for different pulse amplitudes](figures/intensity_detuning_population.png)

![Maximum unnormalized correlation versus detuning for different pulse amplitudes](figures/intensity_detuning_g2.png)

## Generated Figures

| Figure | Description |
|---|---|
| `population_dynamics.png` | Excited-state population dynamics |
| `photon_intensity.png` | Time-dependent emission intensity |
| `time_resolved_g2.png` | Time-resolved second-order photon correlation |
| `pulse_duration_comparison.png` | Population response for different pulse durations |
| `g2_constant_area_comparison.png` | Correlation comparison at constant pulse area |
| `detuning_population_sweep.png` | Population response across the detuning sweep |
| `detuning_g2_sweep.png` | Maximum unnormalized correlation across the detuning sweep |
| `g2_detuning_maps.png` | Time-resolved correlation maps at selected detunings |
| `g2_detuning_normalized_profiles.png` | Shape comparison of normalized correlation profiles |
| `g2_detuning_time_dependence.png` | Time dependence of detuning-induced profile differences |
| `intensity_detuning_population.png` | Population dependence on pulse amplitude and detuning |
| `intensity_detuning_g2.png` | Unnormalized correlation dependence on pulse amplitude and detuning |

## Software

All simulations are implemented in Python using QuTiP, NumPy, SciPy, and Matplotlib.
