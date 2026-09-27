# Adapting the Traveling Salesman Problem to an Adiabatic Quantum Computer

**Authors:** Richard H. Warren  
**Year:** 2013  
**Venue:** *Quantum Information Processing*, 12, 1781–1785  
**DOI:** 10.1007/s11128-012-0490-8

## Summary

Warren develops a formulation of the Traveling Salesman Problem (TSP) suitable for an adiabatic quantum computer. The approach represents a tour using binary variables \(V_{it}\), where \(V_{it}=1\) indicates that city \(i\) is visited at position \(t\). This gives \(n^2\) binary variables for an \(n\)-city TSP, while the tour length is expressed as a quadratic function of these variables.

The constraints requiring every city to be visited exactly once and every tour position to contain exactly one city are converted into quadratic penalty terms. The resulting Hamiltonian is therefore a quadratic binary energy function whose ground state corresponds to an optimal feasible tour. Warren also discusses the practical limitations imposed by the number and connectivity of qubits in contemporary adiabatic hardware.

## Paper Notes

- **Problem:** Adapt the classical TSP to the energy-minimization framework required by an adiabatic quantum computer.

- **Binary variables:**
  \[
  V_{it}\in\{0,1\},
  \]
  where \(V_{it}=1\) iff city \(i\) occupies tour position \(t\).

  For \(n\) cities:
  \[
  N=n^2
  \]
  binary variables are required.

- **Objective:** Let \(d_{ij}\) be the distance from city \(i\) to city \(j\). The tour cost is represented by
  \[
  H_{\mathrm{cost}}
  =
  \sum_{i,j,t} d_{ij}V_{it}V_{j,t+1},
  \]
  with \(t+1\) interpreted cyclically. Thus, the quadratic terms encode the travel cost between consecutive positions in the tour.

- **Feasibility constraints:**
  - Exactly one city must occupy each position:
    \[
    \sum_i V_{it}=1
    \qquad \forall t.
    \]
  - Every city must appear exactly once:
    \[
    \sum_t V_{it}=1
    \qquad \forall i.
    \]

- **Penalty formulation:** The equality constraints are incorporated into the objective using squared penalties:
  \[
  \left(\sum_iV_{it}-1\right)^2
  \]
  and
  \[
  \left(\sum_tV_{it}-1\right)^2.
  \]

  The resulting Hamiltonian has the form
  \[
  H =
  H_{\mathrm{cost}}
  +\lambda H_{\mathrm{constraints}},
  \]
  where \(\lambda\) controls the relative weight of feasibility constraints versus tour cost.

- **Resulting model:** The constrained TSP is transformed into a quadratic binary energy-minimization problem compatible with the Ising/adiabatic quantum-computing framework. A ground state satisfying the constraints represents an optimal TSP tour.

- **Hardware limitations:** Although the formulation is mathematically valid for arbitrary \(n\), its implementation is constrained by the available number of qubits and their connectivity. The \(n^2\) logical variables and required couplings make practical implementation increasingly difficult as the problem size grows.

- **Nature of the contribution:** The paper is primarily a **formulation/adaptation study**, establishing how the TSP can be represented as an adiabatic Hamiltonian rather than demonstrating a large-scale quantum computational advantage.

- **Overall transformation:**
  \[
  \boxed{
  \text{TSP}
  \rightarrow
  \text{city-position binary variables}
  \rightarrow
  \text{quadratic penalty formulation}
  \rightarrow
  \text{adiabatic Hamiltonian}
  }
  \]

## Self Notes

