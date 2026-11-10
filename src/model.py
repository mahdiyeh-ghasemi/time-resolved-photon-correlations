
import numpy as np
from qutip import basis, ket2dm


# Two-level basis states
g = basis(2, 0)  # Ground state
e = basis(2, 1)  # Excited state

# Atomic operators
sigma_minus = g * e.dag()
sigma_plus = e * g.dag()
sigma_z = e * e.dag() - g * g.dag()
projector_e = e * e.dag()


def gaussian_pulse(t, omega_0, t_0, sigma):
    """Gaussian pulse envelope."""
    return omega_0 * np.exp(-((t - t_0) ** 2) / (2 * sigma**2))


def hamiltonian(t, **args):
    """Time-dependent Hamiltonian in the rotating frame (hbar = 1)."""
    delta = args["delta"]
    omega = gaussian_pulse(
        t,
        args["omega_0"],
        args["t_0"],
        args["sigma"],
    )

    return (
        delta * projector_e
        + (omega / 2) * (sigma_plus + sigma_minus)
    )


def collapse_operators(gamma, gamma_phi):
    """Collapse operators for spontaneous emission and pure dephasing."""
    c_ops = [np.sqrt(gamma) * sigma_minus]

    if gamma_phi > 0:
        c_ops.append(np.sqrt(gamma_phi / 2) * sigma_z)

    return c_ops


def initial_state():
    """Initial state: the emitter is in its ground state."""
    return ket2dm(g)
