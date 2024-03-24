from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Operator, Pauli, Statevector
from qiskit_aer import Aer
from qiskit_aer.noise import NoiseModel, depolarizing_error
from qiskit_aer import AerSimulator

def fold_circuit(circuit, scale_factor):
    """
    Folds a circuit by a given scale factor. Scale factor <= 1 means no folding.
    Only supports whole-circuit folding for simplicity.

    Parameters:
    circuit (QuantumCircuit): The original quantum circuit.
    scale_factor (float): The factor by which to scale the noise, should be >= 1.

    Returns:
    QuantumCircuit: The folded quantum circuit.
    """
    if scale_factor <= 1:
        return circuit  # No folding needed for scale factor of 1 or less
    
    # Calculate the number of folds needed, rounded down
    num_folds = int(scale_factor - 1)
    
    folded_circuit = circuit.copy()
    
    # Fold the circuit the required number of times
    for _ in range(num_folds):
        # Iterate over the circuit in reverse order and append the inverse
        for gate in reversed(circuit.data):
            # Get the gate name and qubits it acts on
            gate_name = gate[0].name
            qubits = gate[1]
            # Append the inverse gate
            folded_circuit.append(gate[0].inverse(), qubits)
            # Append the original gate again to "cancel out" in an ideal, noise-free scenario
            folded_circuit.append(gate[0], qubits)
            
    return folded_circuit

def build_noise_model(depolarizing_error_prob):
    noise_model = NoiseModel()
    
    # Create depolarizing error models for 1-qubit and 2-qubit gates
    depol_error_1q = depolarizing_error(depolarizing_error_prob, 1)
    depol_error_2q = depolarizing_error(depolarizing_error_prob, 2)
    
    # Apply the single-qubit depolarizing error model to single-qubit gates
    noise_model.add_all_qubit_quantum_error(depol_error_1q, ['u1', 'u2', 'u3'])
    
    # Apply the two-qubit depolarizing error model to two-qubit gates
    noise_model.add_all_qubit_quantum_error(depol_error_2q, ['cx'])
    
    return noise_model

def measure_observable(circuit, observable, backend):
    circuit.save_statevector()
    transpiled_circuit = transpile(circuit, backend)
    job = backend.run(transpiled_circuit)
    result = job.result()
    #statevector = result.get_statevector()
    #expectation_value = Statevector(statevector).expectation_value(observable).real
    state = Statevector(result.get_statevector(circuit))
    expectation_value = state.expectation_value(observable)
    return expectation_value


# Function to simulate the circuit without noise (Ideal Value)
def simulate_ideal(circuit, observable):
    backend = AerSimulator()
    return measure_observable(circuit, observable, backend)

# Function to simulate the circuit with noise (Unmitigated Result)
def simulate_noisy(circuit, observable, noise_model):
    backend = AerSimulator(noise_model=noise_model)
    return measure_observable(circuit, observable, backend)

# Function to apply noise mitigation and simulate (Mitigated Result)
def simulate_mitigated(circuit, observable, noise_model, scale_factors):
    # Implement your ZNE or other noise mitigation technique here
    # This is a placeholder for the actual noise mitigation implementation
    # For simplicity, let's just return the result from the highest scale factor
    backend = AerSimulator(noise_model=noise_model)
    highest_scale_factor = max(scale_factors)
    folded_circuit = fold_circuit(circuit, highest_scale_factor)  # Assuming fold_circuit is defined
    return measure_observable(folded_circuit, observable, backend)
