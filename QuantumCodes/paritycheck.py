import numpy as np

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


# String to store the superposition state
state_0L = "|0_L> = 1/sqrt{8}["
state_1L = "|1_L> = 1/sqrt{8}["

# Iterate over all 4-bit data vectors
for data_vector in range(16):
    # Convert the integer to a binary vector
    data_vector_bin = np.array([int(x) for x in format(data_vector, '04b')])

    # Multiply the data vector by the generator matrix G
    codeword = np.dot(data_vector_bin, G) % 2  # Mod 2 for binary field

    # Check if the Hamming weight is even or odd
    weight = hamming_weight(codeword)
    weight_type = "even" if is_even_weight(codeword) else "odd"

    codeword_str = ''.join(map(str, codeword))
    if weight_type == "even":
        state_0L += "|" + codeword_str + "> + "
    else:
        state_1L += "|" + codeword_str + "> + "
    # Print the results
    print(f"Data vector: {data_vector_bin}, Codeword: {codeword}, Hamming weight: {weight} ({weight_type})")

# Remove the last " + " and add the closing bracket
state_0L = state_0L[:-3] + "]"
state_1L = state_1L[:-3] + "]"

# Print the constructed state
print(state_0L)
print(state_1L)
