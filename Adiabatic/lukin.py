import numpy as np

# Define the generator matrix G
G = np.array([[1, 0, 0, 0, 1, 1, 0],
              [0, 1, 0, 0, 1, 1, 1],
              [0, 0, 1, 0, 0, 1, 1],
              [0, 0, 0, 1, 1, 0, 1]])

# Define the parity check matrix H
H = np.array([[1, 1, 0, 1, 1, 0, 0],
              [1, 1, 1, 0, 0, 1, 0],
              [0, 1, 1, 1, 0, 0, 1]])

# Function to calculate the Hamming weight of a binary vector
def hamming_weight(vector):
    return np.sum(vector)

# Function to check if the Hamming weight is even
def is_even_weight(vector):
    return hamming_weight(vector) % 2 == 0

# Function to compute the syndrome
def compute_syndrome(codeword, H):
    return np.dot(H, codeword) % 2

# Function to correct a bit flip error based on the syndrome
def correct_error(codeword, syndrome):
    error_map = {
        (1, 0, 0): 0,
        (0, 1, 0): 1,
        (0, 0, 1): 2,
        (1, 1, 0): 3,
        (1, 0, 1): 4,
        (0, 1, 1): 5,
        (1, 1, 1): 6
    }
    syndrome_tuple = tuple(syndrome)
    if syndrome_tuple in error_map:
        error_position = error_map[syndrome_tuple]
        codeword[error_position] ^= 1
    return codeword

# String to store the superposition state
state_0L = "|0_L> = 1/sqrt{8}["
state_1L = "|1_L> = 1/sqrt{8}["

# Iterate over all 4-bit data vectors
for data_vector in range(16):
    # Convert the integer to a binary vector
    data_vector_bin = np.array([int(x) for x in format(data_vector, '04b')])

    # Multiply the data vector by the generator matrix G
    codeword = np.dot(data_vector_bin, G) % 2  # Mod 2 for binary field

    # Simulate a bit flip error (for demonstration purposes)
    # Uncomment to simulate an error
    # codeword[2] ^= 1  # Flip the third bit (example error)

    # Compute the syndrome
    syndrome = compute_syndrome(codeword, H)

    # Correct the error if detected
    corrected_codeword = correct_error(codeword.copy(), syndrome)

    # Check if the Hamming weight is even or odd
    weight = hamming_weight(corrected_codeword)
    weight_type = "even" if is_even_weight(corrected_codeword) else "odd"

    codeword_str = ''.join(map(str, corrected_codeword))
    if weight_type == "even":
        state_0L += "|" + codeword_str + "> + "
    else:
        state_1L += "|" + codeword_str + "> + "

# Remove the last " + " and add the closing bracket
state_0L = state_0L[:-3] + "]"
state_1L = state_1L[:-3] + "]"

# Print the constructed state
print(state_0L)
print(state_1L)
