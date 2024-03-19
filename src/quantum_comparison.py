from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
from qiskit.circuit.library import GroverOperator
from qiskit.quantum_info import Statevector
from qiskit.circuit.library import Diagonal  # Diagonal gates are used to create phase oracles
import numpy as np
import matplotlib.pyplot as plt

def less_than_k_qc(k, list_n):
    # Calculate the number of qubits needed to represent the list
    max_val = max(max(list_n), k)
    num_qubits = int(np.ceil(np.log2(max_val + 1)))
    print(f"Searching with Grover's Algorithm using {num_qubits} qubits")

    # Create a list of phases for the oracle
    phases = [1 if i < k else -1 for i in range(2**num_qubits)]
    
    # Create the oracle circuit
    oracle = Diagonal(phases)
    
    # Create the Grover operator
    grover_operator = GroverOperator(oracle, insert_barriers=True)
    
    # Initialize a quantum circuit
    qc = QuantumCircuit(num_qubits, num_qubits)
    
    # Prepare the initial state (superposition of all possible states)
    qc.h(range(num_qubits))
    
    # Apply Grover's operator
    qc.append(grover_operator, range(num_qubits))
    
    # Measurement
    qc.measure(range(num_qubits), range(num_qubits))
    
    # Execute the circuit
    backend = Aer.get_backend('qasm_simulator')
    tqc = transpile(qc, backend)
    job = backend.run(tqc, shots=1024)
    result = job.result()
    
    # Get counts and plot the histogram
    counts = result.get_counts()

    # Process the counts to find the numbers less than k
    found_numbers = process_counts(counts, num_qubits, k)
    
    print(f"Numbers less than {k}:", found_numbers)

    histogram_fig = plot_histogram(counts)

    # Return the list of found numbers and the histogram figure
    return found_numbers, histogram_fig, num_qubits


def process_counts(counts, num_qubits, k):
    # Convert the counts to integers and filter those that are less than k
    found_numbers = []
    for bitstring in counts:
        number = int(bitstring, 2)
        if number < k:
            found_numbers.append(number)
    return found_numbers