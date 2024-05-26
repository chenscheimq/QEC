from qutip import basis, tensor
from qutip.qip.operations import cnot

# Define the coefficients a and b
a = 3/5
b = 4/5

# Define the single qubit state
single_qubit_state = a * basis(2, 0) + b * basis(2, 1)

# Define the initial two-qubit state where the first qubit is the provided single qubit state
initial_state = tensor(single_qubit_state, basis(2, 0),  basis(2, 0))

# Define the CNOT gate acting on the first and second qubits
cnot_gate_1 = cnot(3, control=0, target=1)
cnot_gate_2 = cnot(3, control=0, target=2)

# Apply the CNOT gate to the initial state
final_state = cnot_gate_1 * cnot_gate_2 * initial_state

print("Final state after applying CNOT gate:")
print(final_state)
