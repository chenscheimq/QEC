import numpy as np
import matplotlib.pyplot as plt
from qutip import *

# parameters
omega1 = 1.0  # frequency of the first level
omega2 = 0.9  # frequency of the second level
B_values = np.linspace(-2, 2, 200)  # Magnetic field strength values (extended to negative values)

eigvals1 = []
eigvals2 = []

for B in B_values:
    # Hamiltonian
    H0 = omega1 * sigmaz() + B * sigmax()
    H1 = 0.1 * sigmax()
    H = [H0, [H1, 't']]

    # Calculate eigenvalues
    eigvals = H[0].eigenenergies()

    eigvals1.append(eigvals[0])
    eigvals2.append(eigvals[1])

# Plot the energy eigenvalues as a function of the magnetic field strength
plt.plot(B_values, eigvals1, label='Eigenvalue 1')
plt.plot(B_values, eigvals2, label='Eigenvalue 2')
plt.xlabel('Magnetic Field Strength')
plt.ylabel('Energy')
plt.title('Energy vs Magnetic Field Strength')
plt.legend()
plt.show()