# Hybrid Classical–Quantum Branch-and-Bound Algorithm for Solving Integer Linear Problems

**Authors:** Andrea Sanavio, Davide Tignone, Francesco Ercolessi  
**Year:** 2024  
**Venue:** Entropy, 26(4), 345  
**DOI:** https://doi.org/10.3390/e26040345  
**arXiv:** https://arxiv.org/abs/2311.09700

## Summary

The paper proposes a hybrid classical–quantum algorithm combining classical branch-and-bound (B&B) with quantum annealing. The classical algorithm explores partial assignments and reduces the original problem until the remaining subproblem is small enough to be submitted to a D-Wave quantum annealer. The authors test the approach on the knapsack problem (KP) and the traveling salesman problem (TSP).

For the TSP, the classical B&B constructs partial tours by sequentially selecting edges. When the remaining problem reaches a chosen size threshold, it is formulated as a QUBO using the index-position formulation, with \(M^2\) binary variables for \(M\) remaining cities, and solved using D-Wave.

The experiments show that quantum annealing can produce better solutions than random baselines on the tested instances, but the method does not consistently recover the optimum. The experiments are small and use highly structured instances, so they do not establish a quantum speedup. The paper is primarily an example of **using classical search to control the size of quantum subproblems**.

## Paper Notes

### 1. Hybrid branch-and-bound

- Classical B&B explores partial assignments, maintaining an incumbent solution and pruning branches that cannot improve it.
- The hybrid variant stops branching when the residual problem reaches a chosen size threshold.
- The residual problem is encoded as a QUBO and submitted to D-Wave.
- The threshold controls the trade-off: larger residual problems require less classical branching but are harder for the annealer; smaller residual problems require more classical work.
- The authors use different B&B procedures for KP and TSP.

### 2. Knapsack problem

- Formulation: maximize item value subject to a weight capacity.
- The QUBO encodes the capacity constraint using a penalty term and slack variables.
- Experiments investigate the effect of residual QUBO size on solution quality and classical search effort.
- Larger residual problems reduce the number of classical B&B operations but do not necessarily produce better quantum solutions.
- The hybrid method generally improves on random baselines in aggregate, but does not consistently recover the optimum.

### 3. TSP formulation and experiments

- The classical B&B builds a partial tour by sequentially selecting edges and reducing the remaining TSP.
- The quantum subproblem uses the **index-position formulation**:
  \[
  x_{i,t} =
  \begin{cases}
  1 & \text{if city } i \text{ occupies position } t,\\
  0 & \text{otherwise}.
  \end{cases}
  \]
- For \(M\) remaining cities, the QUBO has \(M^2\) binary variables, plus quadratic objective and constraint penalties.
- The experiment uses a synthetic 10-city asymmetric cost matrix,
  \[
  C_{ij}=(i-j)\bmod N,
  \]
  whose optimal tour follows the city-label order. This is a highly structured instance, not a standard TSPLIB benchmark.
- Residual problems range from 3 to 9 cities, corresponding to 9–81 binary variables.
- The annealer obtains better tour costs than the random baseline across the tested residual sizes, but finds the optimum only for residual problems of 3 and 4 cities.
- Hamming distance from the optimal assignment becomes less informative as residual size increases, illustrating that assignment similarity and tour quality need not agree.

### 4. Main limitations

- Experiments use small, highly structured instances.
- The TSP experiment does not establish performance on standard benchmark instances.
- The comparison does not establish an end-to-end speedup over competitive classical solvers.
- Reducing the number of B&B operations does not necessarily reduce total runtime.
- Classical B&B can be exact, but using an approximate quantum solver for the residual problem means the overall method does not automatically retain a guarantee of finding the global optimum.

## Self Notes
