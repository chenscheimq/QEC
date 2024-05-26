import numpy as np
from qutip import *
from qutip.qip.operations import cnot


# Define the generator matrix G
G = np.array([[1, 0, 0, 0, 0, 1, 1],
              [0, 1, 0, 0, 1, 0, 1],
              [0, 0, 1, 0, 1, 1, 0],
              [0, 0, 0, 1, 1, 1, 1]])


# Function to calculate the Hamming weight of a binary vector
def hamming_weight(vector):
    return np.sum(vector)


# Function to check if the Hamming weight is even
def is_even_weight(vector):
    return hamming_weight(vector) % 2 == 0


# Initialize the superposition states for |0_L> and |1_L>
state_0L = None
state_1L = None

# Iterate over all 4-bit data vectors
for data_vector in range(16):
    # Convert the integer to a binary vector
    data_vector_bin = np.array([int(x) for x in format(data_vector, '04b')])

    # Multiply the data vector by the generator matrix G
    codeword = np.dot(data_vector_bin, G) % 2  # Mod 2 for binary field

    # Check if the Hamming weight is even or odd
    weight_type = "even" if is_even_weight(codeword) else "odd"

    # Create the quantum state for this codeword
    codeword_state = tensor([basis(2, int(bit)) for bit in codeword])

    # Add to the superposition state for |0_L> or |1_L>
    if weight_type == "even":
        if state_0L is None:
            state_0L = codeword_state
        else:
            state_0L += codeword_state
    else:
        if state_1L is None:
            state_1L = codeword_state
        else:
            state_1L += codeword_state

# Normalize the states
state_0L = state_0L.unit()
state_1L = state_1L.unit()

# Create the superposition state with given probabilities
prob_0L = 1
prob_1L = 0
superposition_state = (prob_0L * state_0L + prob_1L * state_1L).unit()


# Function to perform a bit flip on the first qubit
def bit_flip_first_qubit(state):
    X = sigmax()  # Pauli-X gate
    I = qeye(2)  # Identity gate
    operators = [X] + [I] * (len(state.dims[0]) - 1)
    flip_operator = tensor(operators)
    return flip_operator * state


# Function to print the state as a summation of ket states with real coefficients
def print_state_as_ket_summation(state, label):
    coeffs = state.full().flatten()
    ket_strings = []
    for idx, coeff in enumerate(coeffs):
        if np.abs(coeff) > 1e-10:  # Ignore very small coefficients
            bin_str = format(idx, f'0{len(state.dims[0])}b')
            ket_strings.append(f'{coeff.real:.3f}|{bin_str}>')
    ket_sum_str = ' + '.join(ket_strings)
    print(f'{label} = 1/sqrt({len(coeffs)})[{ket_sum_str}]')


# Print the superposition state before bit flip
print_state_as_ket_summation(superposition_state, '|ψ>')

# Apply the bit flip
flipped_state = bit_flip_first_qubit(superposition_state)

# Print the flipped state
print_state_as_ket_summation(flipped_state, "|ψ'>")


# Define the stabilizers
def stabilizer_S1():
    X = sigmax()
    I = qeye(2)
    return tensor([X, I, X, I, X, I, X])  # X1 * X2 * X3 * X7


def stabilizer_S2():
    X = sigmax()
    I = qeye(2)
    return tensor([I, X, X, I, I, X, X])  # X3 * X5 * X6 * X7


def stabilizer_S3():
    X = sigmax()
    I = qeye(2)
    return tensor([I, I, I, X, X, X, X])  # X2 * X3 * X4 * X6


# Function to measure stabilizer using ancilla qubits and CNOT operations
def measure_stabilizer_with_ancilla(state, stabilizer):
    # Create an ancilla qubit initialized to |0>
    ancilla = tensor(basis(2, 0), state)

    # Get the number of qubits in the state
    num_qubits = len(state.dims[0])

    # Apply CNOT gates controlled by the ancilla qubit and targeted by the qubits indicated by the stabilizer
    for i in range(num_qubits):
        if stabilizer.full()[i, i] == 1:  # Check if the stabilizer has a Pauli-X on the i-th qubit
            ancilla = cnot(num_qubits + 1, i,
                           num_qubits) * ancilla  # Apply CNOT with ancilla as control and i-th qubit as target

    # Measure the ancilla qubit
    ancilla_measured = ancilla.ptrace(0).diag()
    return ancilla_measured[0].real, ancilla


# Measure the stabilizers on the flipped state
stabilizer_1 = stabilizer_S1()
stabilizer_2 = stabilizer_S2()
stabilizer_3 = stabilizer_S3()

syndrome_1, ancilla1 = measure_stabilizer_with_ancilla(flipped_state, stabilizer_1)
syndrome_2, ancilla2 = measure_stabilizer_with_ancilla(flipped_state, stabilizer_2)
syndrome_3, ancilla3 = measure_stabilizer_with_ancilla(flipped_state, stabilizer_3)

# Print results
print("\nSyndrome value (expectation of S1):")
print(syndrome_1)
print_state_as_ket_summation(ancilla1, "ancilla1")


print("\nSyndrome value (expectation of S2):")
print(syndrome_2)
print_state_as_ket_summation(ancilla2, "ancilla2")

print("\nSyndrome value (expectation of S3):")
print(syndrome_3)
print_state_as_ket_summation(ancilla3, "ancilla3")