# New Hybrid Quantum Annealing Algorithms for Solving Vehicle Routing Problem

**Authors:** Michał Borowski, Paweł Gora, Katarzyna Karnas, Mateusz Błajda, Krystian Król, Artur Matyjasek, Damian Burczyk, Miron Szewczyk, Michał Kutwin
**Year:** 2020
**Venue:** Computational Science – ICCS 2020, LNCS 12142, pp. 546–561
**DOI / arXiv:** 10.1007/978-3-030-50433-5_42

## Summary

The paper develops quantum-annealing approaches for VRP/CVRP using D-Wave. It first investigates two monolithic QUBO approaches, **Full QUBO Solver (FQS)** and **Average Partition Solver (APS)**, as prototypes. Their main limitation is QUBO size and therefore scalability.

The authors then introduce two decomposition-based hybrid algorithms: **DBSCAN Solver (DBSS)** and **Solution Partitioning Solver (SPS)**. DBSS clusters customers classically and solves the resulting TSP subproblems with quantum annealing. SPS first obtains a global TSP solution and then classically partitions it into vehicle routes while respecting capacity constraints. Experiments on standard CVRP benchmarks and realistic road-network instances show that the hybrid methods can obtain competitive solutions, with decomposition becoming particularly important for larger instances.

## Paper Notes

* **FQS:** represents the complete VRP as one QUBO using variables (x_{i,j,k}), where a variable indicates that vehicle (i) visits location (j) at position (k). The direct formulation becomes too large for practical QPU use.
* **APS:** reduces the QUBO size by assuming that vehicles serve approximately the same number of customers. If there are (N) customers and (M) vehicles, the average is (N/M), with a tolerance (L).
* **Solvers:** FQS/APS were tested through CPU/QPU approaches and D-Wave's Hybrid Solver. The “Hybrid” label here refers to the solver mode, whereas DBSS/SPS are hybrid at the algorithmic level.
* **DBSS:** recursively applies DBSCAN clustering, then solves each cluster as a TSP using the quantum annealer. Equal vehicle capacities can be incorporated through cluster-demand constraints. It scales better than the monolithic approaches but can produce worse solutions than APS on small/medium instances.
* **SPS:** starts from a global TSP tour and partitions its ordered customers into vehicle routes. A dynamic-programming procedure searches for a feasible partition under vehicle-capacity constraints. The optimized partitioning procedure has complexity (O(NMR)), where (R) is the number of sampled vehicle permutations.
* On the larger self-generated instances, **DBSS substantially outperformed APS**, showing the importance of decomposition for scaling.
* SPS was generally competitive with or better than DBSS on the large instances, although some configurations produced invalid solutions.
* Compared with classical simulated annealing, bee algorithm, evolutionary annealing, and recursive DBSCAN-based methods, SPS was competitive on several instances but was not consistently superior.
* The experiments therefore demonstrate **promising hybrid quantum-classical heuristics, not quantum advantage**. The authors explicitly identify further comparisons with classical algorithms and larger/more realistic VRP variants as future work.
* A major methodological point is that the paper compares quantum/hybrid methods against **classical methods of related algorithmic families**, rather than treating “classical algorithms” as one homogeneous baseline.

## Self Notes

* Further understand the **dynamic-programming approach in SPS**
