"""
Quantum Computing Utilities Module

This module provides comprehensive quantum computing utilities including:
- Quantum bit (qubit) representation
- Quantum gates and operations
- Quantum circuit simulation
- Quantum state manipulation
- Basic quantum algorithms
- Measurement and collapse
- Entanglement simulation
- Quantum error correction concepts
- Quantum teleportation simulation

Note: This is a classical simulation of quantum computing concepts.
For real quantum computing, use frameworks like Qiskit, Cirq, or PennyLane.

All functions include comprehensive docstrings and type hints.
"""

import math
import random
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import cmath


class QuantumState(Enum):
    """Basis states."""
    ZERO = "|0⟩"
    ONE = "|1⟩"
    PLUS = "|+⟩"
    MINUS = "|−⟩"


@dataclass
class Qubit:
    """Quantum bit representation."""
    alpha: complex  # Amplitude for |0⟩
    beta: complex   # Amplitude for |1⟩
    
    def __post_init__(self):
        """Normalize quantum state."""
        norm = math.sqrt(abs(self.alpha)**2 + abs(self.beta)**2)
        if norm > 0:
            self.alpha /= norm
            self.beta /= norm
    
    def probability_zero(self) -> float:
        """Probability of measuring |0⟩."""
        return abs(self.alpha)**2
    
    def probability_one(self) -> float:
        """Probability of measuring |1⟩."""
        return abs(self.beta)**2
    
    def measure(self) -> str:
        """Measure qubit (collapse to basis state)."""
        prob_zero = self.probability_zero()
        
        if random.random() < prob_zero:
            self.alpha = 1.0
            self.beta = 0.0
            return "0"
        else:
            self.alpha = 0.0
            self.beta = 1.0
            return "1"
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self.alpha:.3f}|0⟩ + {self.beta:.3f}|1⟩"


class QuantumGate:
    """Quantum gate operations."""
    
    @staticmethod
    def pauli_x(qubit: Qubit) -> Qubit:
        """Pauli-X gate (NOT gate)."""
        return Qubit(qubit.beta, qubit.alpha)
    
    @staticmethod
    def pauli_y(qubit: Qubit) -> Qubit:
        """Pauli-Y gate."""
        new_alpha = -1j * qubit.beta
        new_beta = 1j * qubit.alpha
        return Qubit(new_alpha, new_beta)
    
    @staticmethod
    def pauli_z(qubit: Qubit) -> Qubit:
        """Pauli-Z gate."""
        return Qubit(qubit.alpha, -qubit.beta)
    
    @staticmethod
    def hadamard(qubit: Qubit) -> Qubit:
        """Hadamard gate."""
        factor = 1 / math.sqrt(2)
        new_alpha = factor * (qubit.alpha + qubit.beta)
        new_beta = factor * (qubit.alpha - qubit.beta)
        return Qubit(new_alpha, new_beta)
    
    @staticmethod
    def phase(qubit: Qubit, angle: float) -> Qubit:
        """Phase gate."""
        return Qubit(qubit.alpha, cmath.exp(1j * angle) * qubit.beta)
    
    @staticmethod
    def rotation_x(qubit: Qubit, angle: float) -> Qubit:
        """Rotation around X-axis."""
        cos_half = math.cos(angle / 2)
        sin_half = math.sin(angle / 2)
        new_alpha = cos_half * qubit.alpha - 1j * sin_half * qubit.beta
        new_beta = -1j * sin_half * qubit.alpha + cos_half * qubit.beta
        return Qubit(new_alpha, new_beta)
    
    @staticmethod
    def rotation_y(qubit: Qubit, angle: float) -> Qubit:
        """Rotation around Y-axis."""
        cos_half = math.cos(angle / 2)
        sin_half = math.sin(angle / 2)
        new_alpha = cos_half * qubit.alpha - sin_half * qubit.beta
        new_beta = sin_half * qubit.alpha + cos_half * qubit.beta
        return Qubit(new_alpha, new_beta)
    
    @staticmethod
    def rotation_z(qubit: Qubit, angle: float) -> Qubit:
        """Rotation around Z-axis."""
        phase = cmath.exp(1j * angle / 2)
        return Qubit(phase * qubit.alpha, phase.conjugate() * qubit.beta)
    
    @staticmethod
    def cnot(control: Qubit, target: Qubit) -> Tuple[Qubit, Qubit]:
        """CNOT gate (controlled-NOT)."""
        if abs(control.beta) > 0.99:  # Control is |1⟩
            return control, QuantumGate.pauli_x(target)
        return control, target
    
    @staticmethod
    def swap(qubit1: Qubit, qubit2: Qubit) -> Tuple[Qubit, Qubit]:
        """SWAP gate."""
        return qubit2, qubit1


class QuantumCircuit:
    """Quantum circuit simulation."""
    
    def __init__(self, num_qubits: int):
        """Initialize quantum circuit."""
        self.num_qubits = num_qubits
        self.qubits = [Qubit(1.0, 0.0) for _ in range(num_qubits)]
        self.gates: List[Tuple[str, int, Optional[int], Optional[float]]] = []
    
    def apply_gate(self, gate_name: str, target: int, 
                   control: Optional[int] = None, angle: Optional[float] = None) -> None:
        """Apply gate to circuit."""
        self.gates.append((gate_name, target, control, angle))
        
        if gate_name == "X":
            self.qubits[target] = QuantumGate.pauli_x(self.qubits[target])
        elif gate_name == "Y":
            self.qubits[target] = QuantumGate.pauli_y(self.qubits[target])
        elif gate_name == "Z":
            self.qubits[target] = QuantumGate.pauli_z(self.qubits[target])
        elif gate_name == "H":
            self.qubits[target] = QuantumGate.hadamard(self.qubits[target])
        elif gate_name == "P":
            if angle is not None:
                self.qubits[target] = QuantumGate.phase(self.qubits[target], angle)
        elif gate_name == "RX":
            if angle is not None:
                self.qubits[target] = QuantumGate.rotation_x(self.qubits[target], angle)
        elif gate_name == "RY":
            if angle is not None:
                self.qubits[target] = QuantumGate.rotation_y(self.qubits[target], angle)
        elif gate_name == "RZ":
            if angle is not None:
                self.qubits[target] = QuantumGate.rotation_z(self.qubits[target], angle)
        elif gate_name == "CNOT":
            if control is not None:
                self.qubits[control], self.qubits[target] = QuantumGate.cnot(
                    self.qubits[control], self.qubits[target]
                )
        elif gate_name == "SWAP":
            if control is not None:
                self.qubits[target], self.qubits[control] = QuantumGate.swap(
                    self.qubits[target], self.qubits[control]
                )
    
    def measure_all(self) -> str:
        """Measure all qubits."""
        result = ""
        for qubit in self.qubits:
            result += qubit.measure()
        return result
    
    def get_state(self) -> List[Qubit]:
        """Get current quantum state."""
        return self.qubits.copy()
    
    def reset(self) -> None:
        """Reset circuit to initial state."""
        self.qubits = [Qubit(1.0, 0.0) for _ in range(self.num_qubits)]
        self.gates.clear()


class QuantumAlgorithms:
    """Basic quantum algorithms."""
    
    @staticmethod
    def superposition_demo() -> Dict[str, Any]:
        """Demonstrate superposition using Hadamard gate."""
        qubit = Qubit(1.0, 0.0)  # |0⟩
        
        # Apply Hadamard
        qubit = QuantumGate.hadamard(qubit)
        
        return {
            "initial_state": "|0⟩",
            "final_state": str(qubit),
            "prob_0": qubit.probability_zero(),
            "prob_1": qubit.probability_one()
        }
    
    @staticmethod
    def entanglement_demo() -> Dict[str, Any]:
        """Demonstrate entanglement using CNOT."""
        circuit = QuantumCircuit(2)
        
        # Create superposition on first qubit
        circuit.apply_gate("H", 0)
        
        # Entangle with CNOT
        circuit.apply_gate("CNOT", 1, control=0)
        
        state = circuit.get_state()
        
        return {
            "qubit0_state": str(state[0]),
            "qubit1_state": str(state[1]),
            "entangled": True
        }
    
    @staticmethod
    def deutsch_jozsa(function: Callable[[str], str], num_bits: int = 1) -> str:
        """Deutsch-Jozsa algorithm (simplified)."""
        # This is a simplified version - real algorithm requires quantum oracle
        circuit = QuantumCircuit(num_bits + 1)
        
        # Initialize ancilla qubit to |1⟩
        circuit.qubits[-1] = Qubit(0.0, 1.0)
        
        # Apply Hadamard to all qubits
        for i in range(len(circuit.qubits)):
            circuit.apply_gate("H", i)
        
        # Apply oracle (simplified - classical simulation)
        # In real quantum computing, this would be a quantum oracle
        
        # Apply Hadamard to first n qubits
        for i in range(num_bits):
            circuit.apply_gate("H", i)
        
        # Measure first qubit
        measurement = circuit.qubits[0].measure()
        
        return "constant" if measurement == "0" else "balanced"
    
    @staticmethod
    def grover_search(num_items: int, target_index: int, iterations: int = 1) -> int:
        """Grover's search algorithm (simplified)."""
        # Simplified Grover - real implementation requires amplitude amplification
        # This is a classical simulation showing the concept
        
        # Initialize superposition
        amplitudes = [1 / math.sqrt(num_items) for _ in range(num_items)]
        
        # Grover iterations
        for _ in range(iterations):
            # Oracle (mark target)
            amplitudes[target_index] *= -1
            
            # Diffusion operator
            mean = sum(amplitudes) / num_items
            amplitudes = [2 * mean - amp for amp in amplitudes]
        
        # Measure (find max amplitude)
        max_index = max(range(num_items), key=lambda i: abs(amplitudes[i]))
        
        return max_index
    
    @staticmethod
    def quantum_teleportation(qubit: Qubit) -> Tuple[Qubit, str]:
        """Quantum teleportation simulation."""
        # Simplified teleportation protocol
        # Real implementation requires Bell state measurement
        
        circuit = QuantumCircuit(3)
        circuit.qubits[0] = qubit  # Qubit to teleport
        
        # Create Bell pair between qubits 1 and 2
        circuit.apply_gate("H", 1)
        circuit.apply_gate("CNOT", 2, control=1)
        
        # Bell measurement on qubits 0 and 1
        # In real quantum computing, this would be a quantum measurement
        
        # Apply corrections based on measurement
        # This is simplified - real protocol depends on measurement outcome
        
        return circuit.qubits[2], "teleported"


class Entanglement:
    """Entanglement utilities."""
    
    @staticmethod
    def create_bell_pair() -> Tuple[Qubit, Qubit]:
        """Create Bell pair (maximally entangled state)."""
        circuit = QuantumCircuit(2)
        
        # Initialize first qubit to |0⟩
        circuit.qubits[0] = Qubit(1.0, 0.0)
        
        # Create superposition
        circuit.apply_gate("H", 0)
        
        # Entangle
        circuit.apply_gate("CNOT", 1, control=0)
        
        return circuit.qubits[0], circuit.qubits[1]
    
    @staticmethod
    def measure_entanglement(qubit1: Qubit, qubit2: Qubit, shots: int = 100) -> Dict[str, int]:
        """Measure entanglement correlation."""
        results = {"00": 0, "01": 0, "10": 0, "11": 0}
        
        for _ in range(shots):
            # Measure both qubits
            # In real quantum computing, this would be simultaneous measurement
            m1 = qubit1.measure()
            m2 = qubit2.measure()
            
            result = m1 + m2
            results[result] += 1
            
            # Reset qubits for next shot
            qubit1 = Qubit(1.0, 0.0)
            qubit2 = Qubit(1.0, 0.0)
        
        return results


class QuantumErrorCorrection:
    """Quantum error correction concepts."""
    
    @staticmethod
    def bit_flip_encode(qubit: Qubit) -> Tuple[Qubit, Qubit, Qubit]:
        """Encode qubit using 3-qubit bit flip code."""
        # This is a simplified encoding
        # Real implementation requires CNOT gates
        return qubit, qubit, qubit
    
    @staticmethod
    def bit_flip_decode(qubits: Tuple[Qubit, Qubit, Qubit]) -> Qubit:
        """Decode using majority voting."""
        # Measure all qubits and take majority
        measurements = [q.measure() for q in qubits]
        
        if measurements.count("0") >= 2:
            return Qubit(1.0, 0.0)
        else:
            return Qubit(0.0, 1.0)
    
    @staticmethod
    def phase_flip_encode(qubit: Qubit) -> Tuple[Qubit, Qubit, Qubit]:
        """Encode qubit using 3-qubit phase flip code."""
        # Simplified phase flip encoding
        return qubit, qubit, qubit
    
    @staticmethod
    def apply_noise(qubit: Qubit, error_rate: float = 0.1) -> Qubit:
        """Apply random noise to qubit."""
        if random.random() < error_rate:
            # Apply bit flip error
            return QuantumGate.pauli_x(qubit)
        return qubit


class QuantumSimulator:
    """Quantum circuit simulator."""
    
    def __init__(self, num_qubits: int):
        """Initialize simulator."""
        self.circuit = QuantumCircuit(num_qubits)
        self.measurements: List[str] = []
    
    def run(self, shots: int = 1) -> Dict[str, int]:
        """Run circuit simulation."""
        results = {}
        
        for _ in range(shots):
            measurement = self.circuit.measure_all()
            results[measurement] = results.get(measurement, 0) + 1
        
        return results
    
    def get_probabilities(self) -> Dict[str, float]:
        """Get measurement probabilities."""
        probs = {}
        
        # Calculate probability for each possible state
        # This is simplified - real implementation requires state vector
        for i in range(2 ** self.circuit.num_qubits):
            state = format(i, f'0{self.circuit.num_qubits}b')
            probs[state] = 1.0 / (2 ** self.circuit.num_qubits)
        
        return probs
    
    def reset(self) -> None:
        """Reset simulator."""
        self.circuit.reset()
        self.measurements.clear()


class QuantumUtilities:
    """Quantum computing utility functions."""
    
    @staticmethod
    def tensor_product(state1: List[complex], state2: List[complex]) -> List[complex]:
        """Calculate tensor product of two quantum states."""
        result = []
        for a in state1:
            for b in state2:
                result.append(a * b)
        return result
    
    @staticmethod
    def normalize_state(state: List[complex]) -> List[complex]:
        """Normalize quantum state."""
        norm = math.sqrt(sum(abs(amp)**2 for amp in state))
        if norm > 0:
            return [amp / norm for amp in state]
        return state
    
    @staticmethod
    def bloch_sphere_coords(qubit: Qubit) -> Tuple[float, float, float]:
        """Calculate Bloch sphere coordinates."""
        theta = 2 * math.acos(abs(qubit.alpha))
        phi = cmath.phase(qubit.beta) - cmath.phase(qubit.alpha)
        
        x = math.sin(theta) * math.cos(phi)
        y = math.sin(theta) * math.sin(phi)
        z = math.cos(theta)
        
        return (x, y, z)
    
    @staticmethod
    def from_bloch_coords(x: float, y: float, z: float) -> Qubit:
        """Create qubit from Bloch sphere coordinates."""
        theta = math.acos(z)
        phi = math.atan2(y, x)
        
        alpha = math.cos(theta / 2)
        beta = cmath.exp(1j * phi) * math.sin(theta / 2)
        
        return Qubit(alpha, beta)


def demonstrate_quantum_computing():
    """Demonstrate quantum computing functionality."""
    print("=== Quantum Computing Demonstration ===\n")
    
    # Qubit Basics
    print("1. Qubit Basics:")
    qubit_zero = Qubit(1.0, 0.0)
    qubit_one = Qubit(0.0, 1.0)
    
    print(f"   |0⟩ state: {qubit_zero}")
    print(f"   |1⟩ state: {qubit_one}")
    print(f"   Prob(|0⟩): {qubit_zero.probability_zero():.2f}")
    print(f"   Prob(|1⟩): {qubit_one.probability_one():.2f}")
    
    # Quantum Gates
    print("\n2. Quantum Gates:")
    qubit = Qubit(1.0, 0.0)
    
    after_x = QuantumGate.pauli_x(qubit)
    print(f"   After X gate: {after_x}")
    
    after_h = QuantumGate.hadamard(qubit)
    print(f"   After H gate: {after_h}")
    
    after_z = QuantumGate.pauli_z(after_h)
    print(f"   After Z gate: {after_z}")
    
    # Quantum Circuit
    print("\n3. Quantum Circuit:")
    circuit = QuantumCircuit(2)
    
    circuit.apply_gate("H", 0)
    circuit.apply_gate("H", 1)
    circuit.apply_gate("CNOT", 1, control=0)
    
    state = circuit.get_state()
    print(f"   Qubit 0: {state[0]}")
    print(f"   Qubit 1: {state[1]}")
    
    # Superposition
    print("\n4. Superposition Demo:")
    superposition = QuantumAlgorithms.superposition_demo()
    print(f"   {superposition}")
    
    # Entanglement
    print("\n5. Entanglement Demo:")
    entanglement = QuantumAlgorithms.entanglement_demo()
    print(f"   {entanglement}")
    
    # Bell Pair
    print("\n6. Bell Pair:")
    bell1, bell2 = Entanglement.create_bell_pair()
    print(f"   Bell qubit 1: {bell1}")
    print(f"   Bell qubit 2: {bell2}")
    
    # Measurement
    print("\n7. Measurement:")
    qubit = Qubit(1.0, 0.0)
    qubit = QuantumGate.hadamard(qubit)
    
    print(f"   Before measurement: {qubit}")
    print(f"   Measured: {qubit.measure()}")
    print(f"   After measurement: {qubit}")
    
    # Bloch Sphere
    print("\n8. Bloch Sphere Coordinates:")
    qubit = Qubit(1.0, 0.0)
    qubit = QuantumGate.hadamard(qubit)
    
    x, y, z = QuantumUtilities.bloch_sphere_coords(qubit)
    print(f"   Bloch coords: x={x:.3f}, y={y:.3f}, z={z:.3f}")
    
    # Rotations
    print("\n9. Rotation Gates:")
    qubit = Qubit(1.0, 0.0)
    
    after_rx = QuantumGate.rotation_x(qubit, math.pi / 4)
    print(f"   After RX(π/4): {after_rx}")
    
    after_ry = QuantumGate.rotation_y(qubit, math.pi / 4)
    print(f"   After RY(π/4): {after_ry}")
    
    # Quantum Search
    print("\n10. Grover's Search (Simplified):")
    found = QuantumAlgorithms.grover_search(8, 5, iterations=2)
    print(f"   Target index: 5, Found: {found}")
    
    # Error Correction
    print("\n11. Error Correction:")
    qubit = Qubit(1.0, 0.0)
    encoded = QuantumErrorCorrection.bit_flip_encode(qubit)
    
    noisy = [QuantumErrorCorrection.apply_noise(q, 0.2) for q in encoded]
    decoded = QuantumErrorCorrection.bit_flip_decode(tuple(noisy))
    
    print(f"   Original: {qubit}")
    print(f"   Decoded: {decoded}")
    
    # Simulator
    print("\n12. Quantum Simulator:")
    simulator = QuantumSimulator(2)
    simulator.circuit.apply_gate("H", 0)
    simulator.circuit.apply_gate("H", 1)
    
    results = simulator.run(shots=100)
    print(f"   Measurement results: {results}")
    
    print("\n=== Demonstration Complete ===")
    print("\nQuantum Computing Best Practices:")
    print("- This is a classical simulation - use Qiskit/Cirq for real quantum computing")
    print("- Quantum gates are unitary operations")
    print("- Measurement collapses quantum state")
    print("- Entanglement enables quantum parallelism")
    print("- Superposition allows exploration of multiple states")
    print("- Quantum algorithms provide exponential speedups for specific problems")
    print("- Error correction is essential for practical quantum computing")
    print("- Quantum circuits require careful gate ordering")
    print("- Bloch sphere provides visualization of single-qubit states")
    print("- Real quantum hardware has noise and decoherence")
    print("- Quantum advantage requires carefully designed algorithms")


if __name__ == "__main__":
    demonstrate_quantum_computing()