
import numpy as np
from qutip import mesolve

from src.model import (
    hamiltonian,
    collapse_operators,
    initial_state,
    projector_e,
)


def solve_dynamics(
    times,
    omega_0,
    t_0,
    sigma,
    gamma,
    gamma_phi=0.0,
    delta=0.0,
):
    """
    Solve the time-dependent Lindblad master equation
    for a Gaussian-driven two-level emitter.
    """

    args = {
        "omega_0": omega_0,
        "t_0": t_0,
        "sigma": sigma,
        "delta": delta,
    }

    c_ops = collapse_operators(gamma, gamma_phi)

    result = mesolve(
    hamiltonian,
    initial_state(),
    times,
    c_ops,
    e_ops=[projector_e],
    args=args,
    options={"store_states": True},
)
    return result
