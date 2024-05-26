from qutip import basis, tensor
from qutip.qip.operations import cnot
from qiskit import QuantumRegister
from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit

q = QuantumRegister(3,'q')
c = ClassicalRegister(1,'c')

circuit = QuantumCircuit(q,c)

circuit.cx(q[0],q[1])
circuit.cx(q[0],q[2])
circuit.x(q[0]) #Add this to simulate a bit flip error
circuit.cx(q[0],q[1])
circuit.cx(q[0],q[2])
circuit.ccx(q[2],q[1],q[0])
circuit.measure(q[0],c[0])

print(circuit)

def encode_single_qubit_state(single_qubit_state):
    """
    Encodes a single qubit state into a qubit state.
    :param single_qubit_state:
    :return:
    """
    # Define the three-qubit bit flip code circuit
    cnot_gate_1 = cnot(3, control=0, target=1)
    cnot_gate_2 = cnot(3, control=0, target=2)

    # Define the initial two-qubit state where the first qubit is the provided single qubit state
    initial_state = tensor(single_qubit_state, basis(2, 0),  basis(2, 0))

    # Apply the CNOT gate to the initial state
    encoded_state = cnot_gate_1 * cnot_gate_2 * initial_state
    return encoded_state


if __name__ == "__main__":
    # Define the coefficients a and b
    a = 3/5
    b = 4/5
    # Define the single qubit state
    single_qubit_state = a * basis(2, 0) + b * basis(2, 1)
    print("Single qubit state after before applying the encoding circuit:")
    print(single_qubit_state)

    # Encoding the data
    encoded_state = encode_single_qubit_state(single_qubit_state)
    print("Encoded state after applying the encoding circuit to the single qubit state:")
    print(encoded_state)

    from qutip import *
    import random
    from qutip.qip.operations import cnot, snot

    # Define the coefficients a and b
    a = 3/5
    b = 4/5
    # Define the single qubit state
    psi = a * basis(2, 0) + b * basis(2, 1)

    # Physical qubits
    qubit1, qubit2 = basis(2, 0), basis(2, 0)
    # Full state of system
    state = tensor(psi, qubit1, qubit2)

    cnot01 = cnot(N=3, control=0, target=1)
    cnot02 = cnot(N=3, control=0, target=2)

    # Perform encoding logical -> physical
    state = cnot02 * cnot01 * state

    # Syndrome measurements
    A = tensor(sigmaz(), sigmaz(), qeye(2))
    B = tensor(qeye(2), sigmaz(), sigmaz())

    # Flip a random qubit
    flip_ops = [qeye(2), qeye(2), sigmax()]
    random.shuffle(flip_ops)
    print("Flipping qubit {}".format(flip_ops.index(sigmax())))
    flip = tensor(flip_ops)

    state = flip * state

    # Perform syndrome measurement
    a = 1 if (A * state) == state else -1
    b = 1 if (B * state) == state else -1

    # Perform error correction
    correction = None
    if a == 1 and b == 1:
        # No error
        correction = tensor([qeye(2)] * 3)
        print("No error")
    elif a == 1 and b == -1:
        correction = tensor(qeye(2), qeye(2), sigmax())
        print("Error detected: qubit 2 flipped")
    elif a == -1 and b == 1:
        correction = tensor(sigmax(), qeye(2), qeye(2))
        print("Error detected: qubit 0 flipped")
    else:
        correction = tensor(qeye(2), sigmax(), qeye(2))
        print("Error detected: qubit 1 flipped")

    state = correction * state

    # Decode physical -> logical
    state = cnot01 * cnot02 * state
    logical = state.ptrace(0)

    # Check qubit was decoded correctly
    if logical == ket2dm(psi):
        print("Error successfully corrected")
    else:
        print("Error correction failed")