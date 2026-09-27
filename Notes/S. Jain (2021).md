# Solving the Traveling Salesman Problem on the D-Wave Quantum Computer

**Authors:** Siddharth Jain
**Year:** 2021
**Venue:** *Frontiers in Physics*
**DOI / arXiv:** https://doi.org/10.3389/fphy.2021.760783

## Summary

Jain develops and experimentally tests a compact QUBO formulation for the symmetric TSP on a D-Wave Advantage quantum annealer. The formulation uses binary variables representing selected edges and exploits symmetry to reduce the number of variables. The quantum-annealing approach is compared with a classical 2-opt solver.

## Paper Notes

* Uses an **edge-based formulation**:

  $$
  x_{ij}=1 \iff \text{edge }(i,j)\text{ is selected}.
  $$
* Exploits symmetry to use

  $$
  \frac{n(n-1)}2
  $$

  variables instead of \(n(n-1)\).
* Objective minimizes the total distance of selected edges.
* Enforces **degree-2 constraints** through quadratic penalties.
* Subtours remain a central issue: degree constraints alone can produce multiple disconnected cycles.
* Implements the QUBO on **D-Wave Advantage 1.1** and compares it with a classical **2-opt** solver.
* The tested quantum implementation handles only **up to 8 cities** and does not outperform the classical approach in solution quality or runtime.
* Shows that reducing the number of logical variables does not eliminate **embedding and hardware-connectivity limitations**.
* Extends the formulation to the **asymmetric TSP**, where symmetry can no longer be exploited.
* Main conclusion: current D-Wave hardware and this formulation do not provide a practical advantage for the tested TSP instances.

## Self Notes

*

