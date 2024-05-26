import numpy as np
from qutip import basis, tensor
from qutip.qip.circuit import QubitCircuit, Gate
from qutip.qip.operations import gate_sequence_product
from qutip.qip.operations import cnot, snot


# Define the coefficients a and b
a = 3/5
b = 4/5

# Define the single qubit state
single_qubit_state = a * basis(2, 0) + b * basis(2, 1)
print("Single qubit state after before applying the encoding circuit:")
print(single_qubit_state)

# Define the three-qubit bit flip code circuit
cnot_gate_1 = cnot(3, control=0, target=1)
cnot_gate_2 = cnot(3, control=0, target=2)

# Adding hadamard gates
snot_gate_1 = snot(3, target=0)
snot_gate_2 = snot(3, target=1)
snot_gate_3 = snot(3, target=2)

circuit = cnot_gate_1 * cnot_gate_2 * snot_gate_1 * snot_gate_2 * snot_gate_3

# Tensor product the single qubit state with two additional |0> states
tensor_state = tensor(single_qubit_state, basis(2, 0), basis(2, 0))

# Apply the encoding circuit to the tensor product state
encoded_state = circuit * tensor_state

print("Encoded state after applying the encoding circuit to the single qubit state:")
print(encoded_state)
