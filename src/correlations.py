import numpy as np
from qutip import mesolve

from src.model import (
    hamiltonian,
    collapse_operators,
    sigma_minus,
)


def time_resolved_g2(
    times,
    rho_states,
    tau_values,
    omega_0,
    t_0,
    sigma,
    gamma,
    gamma_phi=0.0,
    delta=0.0,
    solver_options=None,
):
    """
    Calculate the time-resolved second-order photon correlation
    G2(t, tau) using conditional density-matrix evolution.
    """

    args = {
        "omega_0": omega_0,
        "t_0": t_0,
        "sigma": sigma,
        "delta": delta,
    }

    c_ops = collapse_operators(gamma, gamma_phi)

    L = np.sqrt(gamma) * sigma_minus
    intensity_operator = L.dag() * L

    g2 = np.zeros((len(times), len(tau_values)))

    for i, (t, rho) in enumerate(zip(times, rho_states)):

        # State conditioned on detecting a photon at time t
        rho_cond = L * rho * L.dag()

        # Evolve the conditional state after the first detection
        conditional_result = mesolve(
            hamiltonian,
            rho_cond,
            t + tau_values,
            c_ops,
            e_ops=[intensity_operator],
            args=args,
            options=solver_options,
        )

        g2[i, :] = np.real(conditional_result.expect[0])

    return g2