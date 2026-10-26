# The Travelling Salesperson Problem and the Challenges of Near-Term Quantum Advantage

**Authors:** Kate A. Smith-Miles, Holger H. Hoos, Hao Wang, Thomas Bäck, Tobias J. Osborne  
**Year:** 2025  
**Venue:** Quantum Science and Technology, 10(3), 033001  
**DOI:** https://doi.org/10.1088/2058-9565/add61d

## Summary

This review critically examines whether quantum computing can deliver near-term quantum advantage for the Traveling Salesperson Problem (TSP). The authors argue that, despite approximately two decades of research, general-purpose quantum optimization approaches based on QUBO formulations have not demonstrated competitiveness with state-of-the-art classical TSP solvers. The difficulty is not simply limited quantum hardware capacity: it also stems from the structure of TSP formulations, constraint encoding, penalty-weight sensitivity, and the ability of specialized classical algorithms to exploit the problem's combinatorial structure.

The authors distinguish between general-purpose quantum optimization, which encodes the TSP as a QUBO and searches for a low-energy solution, and specialized hybrid approaches that integrate quantum computation into classical optimization algorithms. They argue that the latter is a more promising direction for future research. Their central recommendation is to identify specific computational bottlenecks in strong classical algorithms that might benefit from quantum acceleration, rather than assuming that solving the entire TSP through a generic QUBO will produce quantum advantage.

## Paper Notes

### 1. Why the TSP is a challenging benchmark for quantum advantage

- The TSP is NP-hard, but classical solvers do not rely on brute-force enumeration.
- Specialized exact methods, including branch-and-bound and cutting-plane algorithms, exploit mathematical structure to prove optimality.
- High-performance heuristics, such as Lin–Kernighan–Helsgaun (LKH) and edge-assembly crossover (EAX), find high-quality tours efficiently.
- Consequently, outperforming brute-force enumeration is insufficient evidence of quantum advantage.

The authors evaluate the prospects for quantum advantage through four questions:
- **Ability:** Can the method reliably find feasible, near-optimal solutions?
- **Competitiveness:** Does it outperform strong classical methods?
- **Scalability:** How does performance change as instance size grows?
- **Hardware competitiveness:** Does performance remain useful on noisy physical hardware?

### 2. TSP formulations for quantum optimization

#### Edge-based formulation
- Binary variables \(x_{ij}\) indicate whether edge \((i,j)\) belongs to the tour.
- The objective minimizes total edge cost, subject to degree constraints.
- Degree constraints alone permit disconnected subtours.
- Subtour-elimination constraints are required, but their number can grow exponentially.
- Special constructions used in early quantum-annealing studies do not provide a general, scalable QUBO formulation for arbitrary TSP instances.

#### Node-based / position-indexed formulation
- Binary variables \(x_{i,t}\) indicate whether city \(i\) occupies tour position \(t\).
- Requires \(N^2\) binary variables.
- The objective minimizes the distance between consecutive cities.
- Exactly-one-city-per-position and exactly-one-position-per-city constraints are encoded using quadratic penalties.
- Satisfying both sets of constraints produces a valid cyclic tour without separate subtour-elimination constraints.

**Main limitation:** Although the position-indexed formulation is straightforward to express as a QUBO, it introduces a large binary model, dense interactions, penalty-weight sensitivity, and an energy landscape that can be difficult to optimize. A mathematically valid QUBO is not necessarily an effective optimization representation.

### 3. Evidence from quantum TSP studies

The review examines approximately two decades of quantum-annealing and gate-model research.

- Early studies established TSP energy formulations but often relied on very small instances or classical simulations.
- Physical-hardware experiments demonstrated that quantum optimization procedures could be executed, but frequently struggled with feasibility, optimality, or scalability.
- Gate-model approaches such as QAOA face additional challenges from circuit depth, parameter optimization, and hardware noise.
- Hybrid approaches can address larger overall instances through classical preprocessing and decomposition, but their results do not automatically establish a quantum contribution.

#### Domain-specific formulation improvements
Villar-Rodriguez et al. (2022) modify the TSP Hamiltonian by penalizing very long edges more strongly, incorporating domain knowledge into the energy function.

The review reports improved feasibility on small instances and feasible solutions with reported optimality gaps of 0–4% for decomposed instances of up to 14 cities. These results depend on specific instances, parameter tuning, and decomposition.

The example illustrates that incorporating problem-specific knowledge can improve performance, but such biases are not universally valid for every TSP instance.

#### Hybrid methods
- Warren (2021) combines quantum annealing with simulated annealing and decomposes a 22-city TSP, reporting an optimality gap of approximately 16.5%.
- Osaba et al. (2021) combine clustering, tabu-search ideas, and QUBO-based subproblem solving, reporting an optimality gap of approximately 27% on asymmetric TSP instances of up to 48 cities.

These methods demonstrate the feasibility of quantum-assisted workflows, not quantum advantage over equivalent classical approaches.

### 4. Why QUBO-based quantum methods struggle

**Lack of combinatorial knowledge**
- Generic QUBO optimizers do not automatically exploit the problem-specific knowledge used by specialized TSP algorithms.

**Inefficient formulations**
- The position-indexed formulation requires \(O(N^2)\) variables and a substantial interaction structure.
- Compactness alone does not guarantee an easy energy landscape or reliable optimization.

**Penalty-weight sensitivity**
- Penalties that are too weak permit infeasible solutions.
- Excessively large penalties can distort the energy landscape.
- Useful parameter ranges can be difficult to identify as problem size grows.

**Instance dependence**
- TSP instances differ in structure and difficulty.
- Small or unusually structured instances may not represent realistic optimization challenges.
- Instance-space analysis can help determine which problem characteristics affect algorithm performance.

**Hardware limitations**
- Noise, decoherence, measurement errors, and limited resources can undermine results obtained in idealized simulations.
- Performance in simulation cannot automatically be extrapolated to physical quantum hardware.

These factors interact: formulation difficulties can create an unfavorable energy landscape, which increases parameter sensitivity and makes reliable optimization more difficult, especially on noisy hardware.

### 5. Historical comparison: Hopfield–Tank neural networks

- Hopfield and Tank (1985) proposed an energy-based neural-network approach to the TSP using city-position variables and constraint penalties.
- Subsequent work identified severe parameter sensitivity, undesirable configurations, and difficulties with subtours.
- Despite modifications, the approach did not establish competitiveness with conventional TSP heuristics.

The authors draw parallels between these difficulties and modern QUBO-based quantum optimization. Both approaches use an energy function to represent the TSP and must contend with the landscape created by that representation.

The analogy does not prove that quantum optimization cannot succeed, but it warns that an elegant energy formulation does not guarantee practical competitiveness.

### 6. Fair benchmarking

The authors argue that quantum methods should be compared against strong classical algorithms rather than brute-force enumeration.

Important requirements include:
- Fair parameter tuning.
- Comparable computational budgets.
- Multiple independent runs and statistical reporting.
- Feasibility rates, solution quality, and optimality gaps.
- Diverse and challenging benchmark instances.
- Appropriate accounting for the costs of preprocessing, embedding, repeated solver calls, and postprocessing.

They recommend two complementary comparisons:

1. **Same-formulation comparison:** Compare quantum and classical optimizers on the same QUBO to isolate the effectiveness of the optimization mechanism.
2. **End-to-end comparison:** Compare the complete quantum or hybrid method against competitive classical TSP algorithms using their respective best-suited approaches.

The first helps isolate the quantum contribution; the second determines whether the overall approach is competitive for the original problem.

### 7. Proposed direction: specialized classical–quantum hybridization

The authors regard specialized hybrid algorithms as a more promising research direction than monolithic QUBO optimization.

The proposed strategy is to:
1. Start with a strong classical optimization algorithm.
2. Identify a computationally expensive subroutine.
3. Investigate whether a quantum algorithm can accelerate that subroutine.
4. Replace the classical subroutine with a quantum equivalent.
5. Benchmark the complete algorithm against the original classical method.

The paper also discusses **hybrid benchmarking**, which estimates whether a proposed quantum subroutine could provide a benefit by examining the workloads and resource requirements of classical algorithms before requiring a full-scale quantum implementation.

Decomposition alone does not establish quantum advantage: the quantum component must provide a measurable benefit beyond what an equivalent classical subsolver achieves.

### 8. Conclusions and future directions

- General-purpose QUBO-based quantum optimizers have not demonstrated competitiveness with state-of-the-art classical TSP algorithms.
- The difficulties extend beyond qubit counts to formulation quality, constraint penalties, energy landscapes, and the lack of specialized combinatorial knowledge.
- Domain-specific formulations and hybrid algorithms are promising research directions, but require rigorous benchmarking.
- The authors argue that general-purpose QUBO approaches are unlikely to become competitive with state-of-the-art classical TSP solvers in the foreseeable future.
- This conclusion concerns the approaches reviewed, not a proof that quantum advantage for the TSP is impossible.

## Self Notes
- studied a resume of the paper, further investigating the paper may be needed
