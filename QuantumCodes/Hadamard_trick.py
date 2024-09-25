import numpy as np
from qutip import *


def hadamard_transform(n):
    """Create an n-qubit Hadamard transform matrix."""
    H = hadamard_transform_single()
    return tensor([H] * n)


def hadamard_transform_single():
    """Create a single-qubit Hadamard gate."""
    H = 1 / np.sqrt(2) * np.array([[1, 1], [1, -1]])
    return Qobj(H)


def create_state_from_codes(codes, n):
    """Create a state from a list of binary codes."""
    state = sum(tensor([basis(2, int(bit)) for bit in code]) for code in codes)
    state = state.unit()  # Normalize the state
    return state


def print_state(state, n):
    """Print the coefficients of the state."""
    states = [format(i, f'0{n}b') for i in range(2 ** n)]
    print("State coefficients:")
    for i, basis_state in enumerate(states):
        coefficient = state.full()[i, 0]
        print(f"|{basis_state}>: {coefficient}")


def main():
    n = 7  # Number of qubits

    # Define the code sets
    C = ['0000000', '1010101', '0110011', '1100110', '0001111', '1011010', '0111100', '1101001']
    C_perp = ['0000000', '1010101', '0110011', '1100110', '0001111', '1011010', '0111100', '1101001',
              '1111111', '0101010', '1001100', '0011001', '1110000', '0100011', '1000011', '0010110']

    # Create the initial state sum_{a in C} |a>
    initial_state = create_state_from_codes(C, n)
    print("Initial state |C>:")
    print_state(initial_state, n)

    # Apply the Hadamard transform
    H_n = hadamard_transform(n)
    transformed_state = H_n * initial_state
    print("\nTransformed state H^{\otimes n} |C>:")
    print_state(transformed_state, n)

    # Create the expected superposition state sum_{b in C_perp} |b>
    expected_state = create_state_from_codes(C_perp, n)
    print("\nExpected superposition state |C_perp>:")
    print_state(expected_state, n)

    # Check if the transformed state is equal to the expected state
    fidelity = fidelity(transformed_state, expected_state)
    print("\nFidelity between transformed state and expected state:", fidelity)
    print("States are equal (up to global phase):", fidelity > 0.9999)


if __name__ == "__main__":
    main()
