# Time-Resolved Photon Correlations in Driven Quantum Systems

A numerical study of the time-resolved emission dynamics and second-order photon correlations of a coherently driven two-level quantum emitter.

The project uses a Lindblad master-equation approach to investigate how pulse duration, pulse amplitude, and frequency detuning affect the emitter population, photon emission intensity, and conditional second-order correlation dynamics.

## Project Overview

This repository contains a reproducible numerical framework for studying a two-level emitter driven by a Gaussian laser pulse.

The main objectives are to:

- Simulate the time evolution of the excited-state population.
- Calculate the time-dependent photon emission intensity.
- Evaluate the conditional, unnormalized second-order correlation function \(G^{(2)}(t,\tau)\).
- Investigate the influence of pulse duration and pulse amplitude.
- Examine the effects of frequency detuning on population dynamics and photon correlations.
- Compare correlation-profile shapes across different detunings and detection times.
- Assess numerical reliability through solver-tolerance tests, temporal-grid refinement, and physical consistency checks.

## Theoretical Model

### Two-Level Quantum Emitter

The system consists of a ground state \(|g\rangle\) and an excited state \(|e\rangle\).

The emitter is driven by a time-dependent Gaussian pulse:

\[
\Omega(t)=\Omega_0
\exp\left[-\frac{(t-t_0)^2}{2\sigma^2}\right],
\]

where:

- \(\Omega_0\) is the peak Rabi frequency.
- \(t_0\) is the pulse-center time.
- \(\sigma\) is the pulse-width parameter.

The pulse area is defined as

\[
A=\int_{-\infty}^{\infty}\Omega(t)\,dt
=\sqrt{2\pi}\,\Omega_0\sigma.
\]

### Hamiltonian

In the rotating frame and using \(\hbar=1\), the Hamiltonian is

\[
H(t)=
\Delta |e\rangle\langle e|
+\frac{\Omega(t)}{2}
(\sigma_++\sigma_-),
\]

where \(\Delta\) is the laser-emitter detuning and

\[
\sigma_+=|e\rangle\langle g|,
\qquad
\sigma_-=|g\rangle\langle e|.
\]

### Master Equation

The density matrix evolves according to the Lindblad master equation:

\[
\frac{d\rho}{dt}
=-i[H(t),\rho]
+\gamma\mathcal{D}[\sigma_-]\rho
+\frac{\gamma_\phi}{2}
\mathcal{D}[\sigma_z]\rho,
\]

with the dissipator defined as

\[
\mathcal{D}[C]\rho
=C\rho C^\dagger
-\frac{1}{2}
\left(C^\dagger C\rho+\rho C^\dagger C\right).
\]

Here:

- \(\gamma\) is the spontaneous-emission rate.
- \(\gamma_\phi\) is the pure-dephasing parameter.
- \(\sigma_z=|e\rangle\langle e|-|g\rangle\langle g|\).

The collapse operators implemented in the code are

\[
C_1=\sqrt{\gamma}\,\sigma_-,
\qquad
C_2=\sqrt{\frac{\gamma_\phi}{2}}\,\sigma_z.
\]

The initial state is the ground-state density matrix:

\[
\rho(0)=|g\rangle\langle g|.
\]

### Excited-State Population and Photon Intensity

The excited-state population is

\[
P_e(t)=\langle e|\rho(t)|e\rangle.
\]

The photon emission intensity is calculated as

\[
I(t)=\gamma P_e(t).
\]

### Time-Resolved Second-Order Correlations

The conditional density matrix following a photon detection at time \(t\) is initialized as

\[
\rho_{\mathrm{cond}}(t)
=\sigma_-\rho(t)\sigma_+.
\]

The subsequent conditional evolution is used to calculate

\[
G^{(2)}(t,\tau)
=
\mathrm{Tr}
\left[
L^\dagger L\,\rho_{\mathrm{cond}}(t+\tau)
\right],
\qquad
L=\sqrt{\gamma}\,\sigma_-.
\]

In this implementation, \(G^{(2)}(t,\tau)\) is **unnormalized**. It is not divided by the product of the mean intensities, and therefore should not be interpreted as the normalized correlation function \(g^{(2)}(t,\tau)\).

The calculation uses the conditional quantum state and subsequent master-equation evolution to resolve the dependence on both detection time \(t\) and delay \(\tau\).

## Numerical Implementation

The simulations are implemented in Python using QuTiP's master-equation solver, `mesolve`.

The code is organized into three core modules:

- `src/model.py`: quantum states, operators, Gaussian pulse, Hamiltonian, collapse operators, and initial state.
- `src/dynamics.py`: master-equation evolution and excited-state population.
- `src/correlations.py`: conditional evolution and time-resolved second-order correlations.

The analysis scripts in `simulations/` use these shared modules to perform the parameter sweeps, numerical tests, and figure generation.

### Representative Parameters

The baseline parameter set used in the main simulations is:

| Parameter | Value | Description |
|---|---:|---|
| \(\Omega_0\) | 1.0 | Peak Rabi frequency |
| \(t_0\) | 5.0 | Gaussian pulse center |
| \(\sigma\) | 1.0 | Gaussian pulse width |
| \(\gamma\) | 0.1 | Spontaneous-emission rate |
| \(\gamma_\phi\) | 0.02 | Pure-dephasing parameter |
| \(\Delta\) | 0.0 | Resonant baseline detuning |

Unless otherwise specified, the main time-resolved calculations use 41 points over \(0\leq t\leq20\) and 41 points over \(0\leq\tau\leq20\).

Some analyses use finer grids or extended time intervals. The parameter values are representative simulation settings, not universal physical constants.

## Numerical Validation

Several numerical checks are included to assess the reliability and physical consistency of the calculations.

### Physical Consistency Checks

`simulations/correlation_metrics.py` evaluates:

1. Zero-delay correlation: \(G^{(2)}(t,0)\) should approach zero for the ideal two-level emitter.
2. Non-negativity of the calculated correlation values within numerical tolerance.
3. Physical bounds of the excited-state population.
4. Decay of the excited-state population after the pulse.

These checks are implemented with numerical tolerances to account for floating-point and solver errors.

### Solver-Tolerance Sensitivity

The solver is tested using three tolerance settings:

| Setting | Absolute tolerance | Relative tolerance |
|---|---:|---:|
| Default | \(10^{-8}\) | \(10^{-6}\) |
| Tight | \(10^{-10}\) | \(10^{-8}\) |
| Strict | \(10^{-12}\) | \(10^{-10}\) |

The comparison shows that the tighter and stricter settings produce very similar results for the tested parameter set.

The maximum absolute difference in the calculated correlation values relative to the default setting is approximately \(2.39\times10^{-9}\) for the tighter settings. The maximum population difference remains below \(2.9\times10^{-7}\).

### Temporal-Grid Refinement

The project includes grid-refinement tests using 41, 81, and 161 points.

A separate intensity-detuning convergence analysis compares 161-point and 321-point grids for the sampled maxima across the tested parameter combinations.

The maximum relative differences between the sampled maxima are:

| Quantity | Maximum relative difference |
|---|---:|
| Excited-state population | 0.26714% |
| Unnormalized \(G^{(2)}\) | 0.02261% |

These values describe the convergence of the sampled maxima in the tested calculations; they do not establish convergence of every point in the full two-dimensional correlation maps.

### Weak-Excitation Scaling

The weak-excitation analysis compares pulse areas of 0.4, 0.2, and 0.1.

For the tested regime, the numerical results are examined against the expected scaling:

\[
P_e^{\max}\propto A^2,
\qquad
G_{\max}^{(2)}\propto A^4.
\]

This provides an additional consistency test of the numerical implementation.

## Results

### 1. Population Dynamics

The excited-state population is calculated by solving the master equation over an extended time interval.

![Excited-state population dynamics](figures/population_dynamics.png)

### 2. Photon Emission Intensity

The time-dependent photon emission intensity is obtained from

\[
I(t)=\gamma P_e(t).
\]

![Photon emission intensity](figures/photon_intensity.png)

### 3. Time-Resolved Photon Correlations

The conditional, unnormalized second-order correlation function is evaluated over detection time and delay.

![Time-resolved second-order correlation](figures/time_resolved_g2.png)

### 4. Pulse-Duration Dependence

The effect of pulse duration is investigated using two complementary comparisons.

The first comparison examines population dynamics for different Gaussian pulse widths at fixed peak amplitude.

![Pulse duration comparison](figures/pulse_duration_comparison.png)

The second comparison investigates the correlation response at constant pulse area \(A=1\), using

\[
\Omega_0=\frac{1}{\sqrt{2\pi}\sigma}.
\]

The tested pulse widths are \(\sigma=0.5,\ 1.0,\ 2.0\).

| Pulse width \(\sigma\) | Maximum \(G^{(2)}\) | Peak delay |
|---:|---:|---:|
| 0.5 | \(3.17\times10^{-5}\) | 1.5 |
| 1.0 | \(2.78\times10^{-5}\) | 2.5 |
| 2.0 | \(2.13\times10^{-5}\) | 4.0 |

![Constant-area correlation comparison](figures/g2_constant_area_comparison.png)

![Pulse-duration correlation comparison](figures/g2_pulse_duration_comparison.png)

### 5. Detuning Dependence

The influence of detuning is investigated using

\[
\frac{\Delta}{\gamma}
=
0,\ 0.5,\ 1,\ 1.5,\ 2,\ 2.5,\ 3.
\]

The population and correlation maxima decrease as the detuning increases over this parameter range.

For the 41-point baseline sweep, the results are:

| \(\Delta/\gamma\) | Maximum population | Maximum \(G^{(2)}\) |
|---:|---:|---:|
| 0.0 | 0.72324 | \(8.8308\times10^{-4}\) |
| 0.5 | 0.72159 | \(8.8160\times10^{-4}\) |
| 1.0 | 0.71668 | \(8.7718\times10^{-4}\) |
| 1.5 | 0.70856 | \(8.6986\times10^{-4}\) |
| 2.0 | 0.69855 | \(8.5971\times10^{-4}\) |
| 2.5 | 0.68628 | \(8.4684\times10^{-4}\) |
| 3.0 | 0.67158 | \(8.3139\times10^{-4}\) |

At \(\Delta=3\gamma\), the maximum population decreases by approximately 7.14%, while the maximum unnormalized correlation decreases by approximately 5.85% relative to resonance.

The following figures show selected-detuning comparisons and the full detuning sweeps.

![Detuning population comparison](figures/detuning_population_comparison.png)

![Detuning correlation comparison](figures/detuning_g2_comparison.png)

![Detuning population sweep](figures/detuning_population_sweep.png)

![Detuning correlation sweep](figures/detuning_g2_sweep.png)

### 6. Detuning Dependence of Correlation Structure

Beyond the maximum correlation value, the project examines the shape of the correlation profiles.

Full time-delay correlation maps are calculated for

\[
\frac{\Delta}{\gamma}=0,\ 1,\ 3.
\]

![Detuning-dependent correlation maps](figures/g2_detuning_maps.png)

The corresponding correlation profiles are compared at a selected detection time.

![Detuning-dependent correlation profiles](figures/g2_detuning_profiles.png)

### 7. Normalized Profile-Shape Comparison

To separate changes in profile shape from changes in overall amplitude, each selected correlation profile is divided by its own maximum.

This is a profile-shape normalization for comparison purposes. It is **not** the standard intensity-normalized \(g^{(2)}\) function.

The root-mean-square (RMS) difference from the resonant profile at \(t=5\) is:

| \(\Delta/\gamma\) | RMS difference |
|---:|---:|
| 0 | 0 |
| 1 | \(4.05\times10^{-4}\) |
| 3 | \(3.64\times10^{-3}\) |

![Normalized correlation profiles](figures/g2_detuning_normalized_profiles.png)

### 8. Detection-Time Dependence

The correlation-profile shape is also examined at different detection times:

\[
t=4,\ 5,\ 6,\ 7.
\]

For the selected parameters, the RMS difference from the resonant profile generally decreases at later detection times.

![Detection-time dependence of correlation profiles](figures/g2_detuning_time_dependence.png)

### 9. Pulse-Amplitude and Detuning Dependence

A finer 321-point temporal grid is used to investigate three peak pulse amplitudes:

\[
\Omega_0=0.5,\ 1.0,\ 2.0,
\]

and three detuning ratios:

\[
\frac{\Delta}{\gamma}=0,\ 1,\ 3.
\]

The simulations use \(\gamma=0.1\), \(\gamma_\phi=0.02\), \(t_0=5\), and \(\sigma=1\), with strict solver tolerances.

The calculated maxima are:

| \(\Omega_0\) | \(\Delta/\gamma\) | Maximum population | Maximum \(G^{(2)}\) |
|---:|---:|---:|---:|
| 0.5 | 0 | 0.26527 | \(6.7035\times10^{-5}\) |
| 0.5 | 1 | 0.26297 | \(6.6599\times10^{-5}\) |
| 0.5 | 3 | 0.24531 | \(6.3226\times10^{-5}\) |
| 1.0 | 0 | 0.72669 | \(8.8564\times10^{-4}\) |
| 1.0 | 1 | 0.72051 | \(8.7990\times10^{-4}\) |
| 1.0 | 3 | 0.67342 | \(8.3533\times10^{-4}\) |
| 2.0 | 0 | 0.93153 | \(6.3853\times10^{-3}\) |
| 2.0 | 1 | 0.92740 | \(6.3448\times10^{-3}\) |
| 2.0 | 3 | 0.89515 | \(6.0302\times10^{-3}\) |

For this parameter set, increasing the pulse amplitude reduces the relative detuning sensitivity of the maximum excited-state population. The relative change in the maximum unnormalized correlation remains of a similar order across the tested amplitudes.

These observations are specific to the investigated model and parameter range.

![Population versus pulse amplitude and detuning](figures/intensity_detuning_population.png)

![Correlation versus pulse amplitude and detuning](figures/intensity_detuning_g2.png)

## Repository Structure

```text
time-resolved-photon-correlations/
│
├── src/
│   ├── model.py
│   ├── dynamics.py
│   └── correlations.py
│
├── simulations/
│   ├── convergence_test.py
│   ├── correlation_metrics.py
│   ├── detuning_comparison.py
│   ├── detuning_sweep.py
│   ├── g2_detuning_normalized.py
│   ├── g2_detuning_structure.py
│   ├── g2_detuning_time_dependence.py
│   ├── g2_pulse_duration_comparison.py
│   ├── intensity_detuning_analysis.py
│   ├── intensity_detuning_convergence.py
│   ├── photon_correlations.py
│   ├── photon_intensity.py
│   ├── population_dynamics.py
│   ├── pulse_duration_comparison.py
│   ├── solver_tolerance_test.py
│   └── weak_excitation_test.py
│
├── figures/
│   ├── detuning_g2_comparison.png
│   ├── detuning_g2_sweep.png
│   ├── detuning_population_comparison.png
│   ├── detuning_population_sweep.png
│   ├── g2_constant_area_comparison.png
│   ├── g2_detuning_maps.png
│   ├── g2_detuning_normalized_profiles.png
│   ├── g2_detuning_profiles.png
│   ├── g2_detuning_time_dependence.png
│