import numpy as np
from qutip import qeye, sigmax, sigmay, sigmaz, basis, tensor

# Basic operators
I = qeye(2)
X = sigmax()
Y = sigmay()
Z = sigmaz()

# Logical operators for 3-qubit code
X_L = tensor(X, X, X)
# Z_L = (tensor(Z, I, I) + tensor(I, Z, I) + tensor(I, I, Z)) / 3
Z_L = tensor(Z, Z, Z)
I_L = tensor(I, I, I)


# Stabilizer generators for 3-qubit code
g1 = [I, Z, Z]
g2 = [Z, Z, I]
gs = [g1, g2]

# Basis states
basis_states = [basis(2, 0), basis(2, 1)]

# Logical states
logical_zero = tensor(basis_states[0], basis_states[0], basis_states[0])
logical_one = tensor(basis_states[1], basis_states[1], basis_states[1])



# RAP time-dependent parameters (default values)
T_max = 20

def time_list(num_points=51):
    """Generate a list of time points from 0 to T_max."""
    return np.linspace(0, T_max, num_points)
t_list = time_list()

sigma = 1
omega_max = 10

# Pulses
# def delta_t(t, T_max=T_max, omega_max=omega_max, sigma=sigma):
#     """Time-dependent detuning for RAP."""
#     return 2 * omega_max * (t / (T_max / 2) - 1)
# def omega_t(t, T_max=T_max, omega_max=omega_max, sigma=sigma):
#     """Time-dependent frequency for RAP."""
#     return omega_max * np.exp(-0.5 * ((t - T_max / 2) / sigma) ** 2)

def omega_t(t, T_max=T_max, omega_max=omega_max):
    """Time-dependent frequency for RAP."""
    return omega_max * np.sin(np.pi * t / T_max)
def delta_t(t, T_max=T_max, omega_max=omega_max):
    """Time-dependent detuning for RAP."""
    return -omega_max * np.cos(np.pi * t / T_max)


def H(t):
    """
    Rapid Adiabatic Hamiltonian
    """
    return  X_L * omega_t(t) + Z_L * delta_t(t)


# Exported variables for import convenience
__all__ = [
    "I", "X", "Y", "Z",
    "X_L", "Z_L", "I_L",
    "g1", "g2", "gs",
    "basis_states",
    "logical_zero", "logical_one",
    "T_max", "t_list", "sigma", "omega_max", "omega_t", "delta_t", "H"
]