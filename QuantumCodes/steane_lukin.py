import numpy as np
from qutip import *

# Define the generator matrix G
G = np.array([[1, 0, 0, 0, 1, 1, 0],
              [0, 1, 0, 0, 1, 1, 1],
              [0, 0, 1, 0, 0, 1, 1],
              [0, 0, 0, 1, 1, 0, 1]])

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
prob_0L = np.sqrt(3/5)
prob_1L = np.sqrt(4/5)
superposition_state = prob_0L * state_0L + prob_1L * state_1L
superposition_state = superposition_state.unit()

# Function to perform a bit flip on the first qubit
def bit_flip_first_qubit(state):
    X = sigmax()  # Pauli-X gate
    I = qeye(2)   # Identity gate
    operators = tensor(X, I, X, X, I, I, I )
    flip_operator = tensor(operators)
    print(flip_operator, state)
    return np.dot(flip_operator, state)

# Apply the bit flip
flipped_state = bit_flip_first_qubit(superposition_state)

# Define the stabilizer X_L = X1 * X2 * X4
def stabilizer_XL():
    X = sigmax()
    I = qeye(2)
    return tensor([X, X, I, X] + [I] * 4)  # X1 * X2 * X4

# Calculate the syndrome
def measure_stabilizer(state, stabilizer):
    return (state.dag() * stabilizer * state).tr().real

# Measure the stabilizer on the flipped state
stabilizer = stabilizer_XL()
syndrome = measure_stabilizer(flipped_state, stabilizer)

# Print results
print("Superposition state |ψ>:")
print(superposition_state)
print("\nFlipped state |ψ'>:")
print(flipped_state)
print("\nStabilizer X_L:")
print(stabilizer)
print("\nSyndrome value (expectation of X_L):")
print(syndrome)
