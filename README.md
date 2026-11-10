# Time-Resolved Photon Correlations in Driven Quantum Systems

## Project Overview

This project investigates the time-resolved photon correlations emitted by a driven quantum emitter under pulsed excitation.

The initial study will use a driven two-level quantum system as a minimal theoretical model. Its dynamics will be described using the Lindblad master equation, with particular attention to the temporal structure of second-order photon correlations.

## Research Question

How do the pulse duration and excitation strength affect the time-resolved photon correlations emitted by a driven quantum emitter?

## Methodology

- Model a driven two-level quantum emitter.
- Implement time-dependent pulsed excitation.
- Solve the open-system dynamics using the Lindblad master equation.
- Calculate time-resolved first- and second-order photon correlation functions.
- Investigate the effects of pulse duration and excitation strength.

## Scope

The initial stage focuses on a minimal two-level emitter model. More complex systems and additional physical effects may be considered in later extensions.

## Project Status

Research model and computational framework under development.

## Theoretical Model

The system is modeled as a driven two-level quantum emitter with ground state \(|g\rangle\) and excited state \(|e\rangle\).

In the rotating frame and using \(\hbar=1\), the Hamiltonian is

\[
H(t)=\Delta\sigma_+\sigma_-+
\frac{\Omega(t)}{2}(\sigma_++\sigma_-)
\]

where the Gaussian driving pulse is

\[
\Omega(t)=\Omega_0
\exp\left[-\frac{(t-t_0)^2}{2\sigma^2}\right].
\]

The open-system dynamics are described by the Lindblad master equation:

\[
\dot{\rho}=-i[H(t),\rho]
+\gamma\mathcal{D}[\sigma_-]\rho
+\frac{\gamma_\phi}{2}\mathcal{D}[\sigma_z]\rho.
\]

Here, \(\gamma\) describes spontaneous emission, while \(\gamma_\phi\) is the pure-dephasing rate.

The Lindblad dissipator is defined as

\[
\mathcal{D}[c]\rho=c\rho c^\dagger-\frac{1}{2}\left\{c^\dagger c,\rho\right\}.
\]

## Photon Correlation Function

The emitted field is represented by the collapse operator

\[
L=\sqrt{\gamma}\sigma_-.
\]

The main observable is the time-resolved second-order photon correlation:

\[
G^{(2)}(t,\tau)=
\langle L^\dagger(t)L^\dagger(t+\tau)
L(t+\tau)L(t)\rangle.
\]

It is evaluated using conditional density-matrix evolution following a photon detection at time t.

This approach accounts for the nonstationary dynamics induced by pulsed excitation.

## Numerical Validation

The computational implementation was examined through several numerical tests:

- Population dynamics and spontaneous-emission behavior.
- Zero-delay antibunching of the two-level emitter.
- Positivity of the calculated second-order correlation within numerical tolerance.
- Convergence with respect to temporal grid refinement.
- Weak-excitation scaling of population and photon correlations.

For weak excitation, the numerical results are consistent with:

\[
P_e^{\max}\propto A^2,
\qquad
G_{\max}^{(2)}\propto A^4,
\]

where A is the Gaussian pulse area.

## Results

The simulations generate the following figures:

| Figure | Description |
|---|---|
| `population_dynamics.png` | Excited-state population dynamics |
| `photon_intensity.png` | Time-dependent emission intensity |
| `time_resolved_g2.png` | Time-resolved second-order photon correlation |
| `pulse_duration_comparison.png` | Population response for different pulse durations |
| `g2_pulse_duration_comparison.png` | Photon correlations for different pulse durations |
| `g2_constant_area_comparison.png` | Correlation comparison at constant pulse area |

All numerical simulations are implemented in Python using QuTiP, NumPy, SciPy, and Matplotlib.
