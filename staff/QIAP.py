import numpy as np
from qutip import basis, tensor, qeye, fidelity
from qutip.qip.operations import cnot, snot
from qutip.operators import sigmax, sigmay, sigmaz

# Step 1: Initialize the quantum state |ψ⟩ and the Bell state |β₀₀⟩
alpha = 3/5
beta = 4/5
psi = alpha * basis(2, 0) + beta * basis(2, 1)
bell_state = (tensor(basis(2, 0), basis(2, 0)) + tensor(basis(2, 1), basis(2, 1))).unit()

# The combined initial state |ψ⟩ ⊗ |β₀₀⟩
initial_state = tensor(psi, bell_state)
print("Initial state |ψ₁⟩ = |ψ⟩ ⊗ |β₀₀⟩:")
print(initial_state)

# Step 2: Apply the CNOT gate to the two qubits which are with Alice
CNOT = cnot(N=3, control=0, target=1)
print(CNOT)
state_after_CNOT = CNOT * initial_state
print("\nState after applying CNOT gate on Alice's qubits:")
print(state_after_CNOT)

# Step 3: Apply the Hadamard gate to Alice's first qubit
H = snot(N=1)
H_alice = tensor(H, qeye(2), qeye(2))
state_after_H = H_alice * state_after_CNOT
print("\nState after applying Hadamard gate on Alice's first qubit:")
print(state_after_H)

# Step 4: Re-write the quantum state in terms of |ij⟩|φ⟩
# (already in the required form, so no additional re-writing needed)

# Step 5: Measure Alice's qubits
# We need to measure the first two qubits, and there are four possible outcomes
measurement_ops = [tensor(basis(2, i), basis(2, j), qeye(2)) * tensor(basis(2, i), basis(2, j), qeye(2)).dag()
                   for i in range(2) for j in range(2)]

# Create a dictionary to map the measurement outcomes to the corresponding operations for Bob
measurement_outcomes = ['00', '01', '10', '11']
operations_for_bob = {
    '00': qeye(2),
    '01': sigmax(),
    '10': sigmaz(),
    '11': sigmay()
}

# Perform the measurements and normalize the state
results = [(m * state_after_H).norm()**2 for m in measurement_ops]
outcome = np.random.choice(range(4), p=results)
measured_state = (measurement_ops[outcome] * state_after_H).unit()
print(f"\nMeasurement outcome: {measurement_outcomes[outcome]}")
print("State after measurement (normalized):")
print(measured_state)

# Extract Bob's qubit state
bob_state = measured_state.ptrace(2)

# Step 6: Bob applies the appropriate operation based on Alice's measurement
operation = operations_for_bob[measurement_outcomes[outcome]]
bob_state_after_operation = operation * bob_state
print("\nBob's state after applying the appropriate operation:")
print(bob_state_after_operation)

# Check if Bob's state matches the initial state |ψ⟩
fidelity_value = fidelity(psi, bob_state_after_operation)
print("\nFidelity between Bob's state and the initial state |ψ⟩:")
print(fidelity_value)
