# import numpy as np
#
#
# # Define the parity matrix H based on stabilizers
# H = np.array([[1, 1, 1, 0, 0, 0, 1],
#               [0, 0, 1, 0, 1, 1, 1],
#               [0, 1, 1, 1, 0, 1, 0]])
#
#
# def calculate_G(H):
#     """
#     Calculates the generator matrix G' from the parity check matrix H.
#     :param H: Parity check matrix (numpy array)
#     :return: G, the generator matrix
#     """
#     r, n = H.shape
#     k = n - r  # The number of information bits
#
#     # Extract columns that do not correspond to the identity matrix columns
#     P = []
#     identity_cols = []
#     for i, col in enumerate(H.T):
#         if np.count_nonzero(col) == 1 and col.sum() == 1:  # Check if column is an identity column
#             identity_cols.append(i)
#         else:
#             P.append(col)
#
#     P = np.array(P)  # Transpose P to have the correct shape
#
#     # Create an identity matrix I of size k x k
#     I = np.eye(k)
#
#     # Concatenate I and P to form G
#     G = np.concatenate((I, P), axis=1)
#
#     return G.astype(int)
#
# # Define the generator matrix G
# G = calculate_G(H)
#
#
# # Function to calculate the Hamming weight of a binary vector
# def hamming_weight(vector):
#     return np.sum(vector)
#
# # Function to check if the Hamming weight is even
# def is_even_weight(vector):
#     return hamming_weight(vector) % 2 == 0
#
# # Function to compute the syndrome
# def compute_syndrome(codeword, H):
#     return np.dot(H, codeword) % 2
#
# # Function to correct a bit flip error based on the syndrome
# def correct_error(codeword, syndrome):
#     error_map = {
#         (1, 0, 0): 0,
#         (0, 1, 0): 4,
#         (0, 0, 1): 3,
#         (1, 1, 0): 6,
#         (1, 0, 1): 1,
#         (0, 1, 1): 5,
#         (1, 1, 1): 2
#     }
#     syndrome_tuple = tuple(syndrome)
#     if syndrome_tuple in error_map:
#         error_position = error_map[syndrome_tuple]
#         codeword[error_position] ^= 1
#     return codeword
#
# # String to store the superposition state
# state_0L = "|0_L> = 1/sqrt{8}["
# state_1L = "|1_L> = 1/sqrt{8}["
#
# # Iterate over all 4-bit data vectors
# for data_vector in range(16):
#     # Convert the integer to a binary vector
#     data_vector_bin = np.array([int(x) for x in format(data_vector, '04b')])
#
#     # Multiply the data vector by the generator matrix G
#     codeword = np.dot(data_vector_bin, G) % 2  # Mod 2 for binary field
#
#     # Simulate a bit flip error
#     error_index = 2
#     # codeword[error_index] ^= 1
#
#     # Compute the syndrome
#     syndrome = compute_syndrome(codeword, H)
#     print(syndrome)
#
#     # Correct the error if detected
#     corrected_codeword = correct_error(codeword.copy(), syndrome)
#
#     # Check if the Hamming weight is even or odd
#     weight = hamming_weight(corrected_codeword)
#     weight_type = "even" if is_even_weight(corrected_codeword) else "odd"
#
#     codeword_str = ''.join(map(str, corrected_codeword))
#     if weight_type == "even":
#         state_0L += "|" + codeword_str + "> + "
#     else:
#         state_1L += "|" + codeword_str + "> + "
#
#
# # Print the constructed state
# state_0L = state_0L[:-3] + "]"
# state_1L = state_1L[:-3] + "]"
#
# print(state_0L)
# print(state_1L)


import numpy as np

# Define the parity matrix H based on stabilizers
H = np.array([[1, 1, 1, 0, 0, 0, 1],
              [0, 0, 1, 0, 1, 1, 1],
              [0, 1, 1, 1, 0, 1, 0]])


def calculate_G(H):
    """
    Calculates the generator matrix G' from the parity check matrix H.
    :param H: Parity check matrix (numpy array)
    :return: G, the generator matrix
    """
    r, n = H.shape
    k = n - r  # The number of information bits

    # Extract columns that do not correspond to the identity matrix columns
    P = []
    for i, col in enumerate(H.T):
        if not (np.count_nonzero(col) == 1 and col.sum() == 1):
            P.append(col)

    P = np.array(P)  # Transpose P to have the correct shape

    # Create an identity matrix I of size k x k
    I = np.eye(k, dtype=int)

    # Concatenate I and P to form G
    G = np.concatenate((I, P), axis=1)

    return G.astype(int)


# Define the generator matrix G
G = calculate_G(H)


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
        (0, 1, 0): 4,
        (0, 0, 1): 3,
        (1, 1, 0): 6,
        (1, 0, 1): 1,
        (0, 1, 1): 5,
        (1, 1, 1): 2
    }
    syndrome_tuple = tuple(syndrome)
    if syndrome_tuple in error_map:
        error_position = error_map[syndrome_tuple]
        codeword[error_position] ^= 1
    return codeword


# String to store the superposition state
state_0L = "|0_L> = 1/sqrt{8}["
state_1L = "|1_L> = 1/sqrt{8}["

# Print the generated states before error
print("Generated states before error:")
for data_vector in range(16):
    # Convert the integer to a binary vector
    data_vector_bin = np.array([int(x) for x in format(data_vector, '04b')])

    # Multiply the data vector by the generator matrix G
    codeword = np.dot(data_vector_bin, G) % 2  # Mod 2 for binary field

    codeword_str = ''.join(map(str, codeword))
    # print(f"Data vector: {data_vector_bin}, Codeword: {codeword_str}")

    # Check if the Hamming weight is even or odd
    weight = hamming_weight(codeword)
    weight_type = "even" if is_even_weight(codeword) else "odd"

    if weight_type == "even":
        state_0L += "|" + codeword_str + "> + "
    else:
        state_1L += "|" + codeword_str + "> + "

state_0L = state_0L[:-3] + "]"
state_1L = state_1L[:-3] + "]"

print(state_0L)
print(state_1L)

# Print the states after introducing the error
print("\nStates after introducing the error:")
error_index = 2  # Simulate a bit flip error at index 2
state_0L_error = "|0_L>_error = 1/sqrt{8}["
state_1L_error = "|1_L>_error = 1/sqrt{8}["

for data_vector in range(16):
    # Convert the integer to a binary vector
    data_vector_bin = np.array([int(x) for x in format(data_vector, '04b')])

    # Multiply the data vector by the generator matrix G
    codeword = np.dot(data_vector_bin, G) % 2  # Mod 2 for binary field

    # Introduce the error
    codeword[error_index] ^= 1

    codeword_str = ''.join(map(str, codeword))
    # print(f"Data vector: {data_vector_bin}, Codeword with error: {codeword_str}")

    # Check if the Hamming weight is even or odd
    weight = hamming_weight(codeword)
    weight_type = "even" if is_even_weight(codeword) else "odd"

    if weight_type == "even":
        state_0L_error += "|" + codeword_str + "> + "
    else:
        state_1L_error += "|" + codeword_str + "> + "

state_0L_error = state_0L_error[:-3] + "]"
state_1L_error = state_1L_error[:-3] + "]"

print(state_0L_error)
print(state_1L_error)

# Print the states after correcting the error
print("\nStates after correcting the error:")
state_0L_corrected = "|0_L>_corrected = 1/sqrt{8}["
state_1L_corrected = "|1_L>_corrected = 1/sqrt{8}["

for data_vector in range(16):
    # Convert the integer to a binary vector
    data_vector_bin = np.array([int(x) for x in format(data_vector, '04b')])

    # Multiply the data vector by the generator matrix G
    codeword = np.dot(data_vector_bin, G) % 2  # Mod 2 for binary field

    # Introduce the error
    codeword[error_index] ^= 1

    # Compute the syndrome
    syndrome = compute_syndrome(codeword, H)

    # Correct the error if detected
    corrected_codeword = correct_error(codeword.copy(), syndrome)

    codeword_str = ''.join(map(str, corrected_codeword))
    # print(f"Data vector: {data_vector_bin}, Corrected codeword: {codeword_str}")

    # Check if the Hamming weight is even or odd
    weight = hamming_weight(corrected_codeword)
    weight_type = "even" if is_even_weight(corrected_codeword) else "odd"

    if weight_type == "even":
        state_0L_corrected += "|" + codeword_str + "> + "
    else:
        state_1L_corrected += "|" + codeword_str + "> + "

state_0L_corrected = state_0L_corrected[:-3] + "]"
state_1L_corrected = state_1L_corrected[:-3] + "]"

print(state_0L_corrected)
print(state_1L_corrected)
