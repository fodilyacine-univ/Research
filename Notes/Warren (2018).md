# Mathematical Methods for a Quantum Annealing Computer

**Authors:** Richard H. Warren  
**Year:** 2018  
**Venue:** Journal of Advances in Applied Mathematics, 3(3), 82–90  
**DOI / arXiv:** 10.22606/jaam.2018.33002

## Summary

The paper explains how optimization problems and logical operations can be represented as Hamiltonians for quantum annealing. It first develops mappings from binary logic (AND, OR, XOR, implication, etc.) to quadratic energy functions, including the use of ancillary variables when needed. It also shows how a CNOT can be represented as an XOR-type Hamiltonian, illustrating the difference between circuit-based quantum computing and annealing.

It then applies these ideas to the TSP using position-based binary variables. The resulting quadratic formulation is implemented and tested on a D-Wave quantum annealer for small instances. The experiments demonstrate the formulation's validity but also highlight hardware limitations: embedding overhead becomes substantial, with the 9-city instance requiring more than 1200 physical qubits, and valid solutions were not always obtained from 1000 samples.

## Paper Notes

- Starts from the **Ising Hamiltonian** and binary-variable representation used by D-Wave.
- Shows how **Boolean constraints/gates → quadratic Hamiltonians**, using penalty functions and ancillary variables when necessary.
- Demonstrates a **CNOT → XOR Hamiltonian** rather than treating it as a sequential circuit operation.
- TSP formulation uses position variables:
  \[
  V_{it}=1 \iff \text{city }i\text{ is at position }t.
  \]
- Fixes one city as the starting city.
- Uses a quadratic distance objective between consecutive positions.
- Enforces:
  - one city per position;
  - one position per city.
- The TSP constraints are expressed directly as quadratic functions \(F_t\) and \(G_i\), combined with weights \(\lambda_1,\lambda_2\).
- Tested on D-Wave for \(n=6,7,8\); \(n=9\) required **>1200 physical qubits** because of embedding.
- Some experiments produced no valid solution among 1000 samples.
- Shows that a mathematically valid QUBO can still become impractical because of **hardware connectivity and embedding overhead**.

## Self Notes

- **Squaring was not needed for the actual TSP formulation**, contrary to what I have been doing in my own QUBO formulation. Warren directly constructs quadratic constraint functions \(F_t\) and \(G_i\).
- Need to compare Warren's direct quadratic constraints with my squared-penalty formulation and determine their algebraic relationship / difference in penalty coefficients.
