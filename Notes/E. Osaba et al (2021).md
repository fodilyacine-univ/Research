# Hybrid Quantum Computing - Tabu Search Algorithm for Partitioning Problems: Preliminary Study on the Traveling Salesman Problem

**Authors:** Eneko Osaba, Javier Del Ser, Alexander Oregi, Mikel N. Bilbao, Asier I. Sanz, Javier L. M. García
**Year:** 2021
**Venue:** *IEEE Congress on Evolutionary Computation (CEC)*
**DOI / arXiv:** 10.1109/CEC45853.2021.9504923 / arXiv:2012.04984

## Summary

The paper proposes a hybrid quantum-classical method, called **Quantum Tabu Algorithm (QTA)**, for solving the TSP by partitioning the problem into smaller subproblems. A classical evolutionary multitasking procedure generates different city partitions, each cluster is solved as a smaller TSP using QBSolv, and the resulting subroutes are merged into a complete tour. A tabu dictionary stores previously solved subproblems so that repeated partitions do not require another QBSolv call.

The main objective is to reduce the number of quantum/quantum-hybrid solver accesses while maintaining solution quality. On seven benchmark instances, QTA obtains solution quality comparable to QBSolv while using only **40 accesses**, compared with roughly **259–474 accesses** for QBSolv. However, the experiments use **local QBSolv rather than an actual QPU**, so the paper demonstrates a resource-reduction strategy rather than quantum advantage.

## Paper Notes

The method has three main components:

1. **Partitioning:** Cities are divided into clusters using an evolutionary multitasking approach. Different clustering objectives are considered, including modularity, Davies–Bouldin, and Calinski–Harabasz metrics.
2. **Subproblem solving:** Each cluster is formulated as a smaller TSP and solved with QBSolv.
3. **Tabu dictionary:** Solutions to previously encountered clusters/partitions are stored and reused, avoiding repeated solver calls.

After solving the clusters, the independent cycles must be converted into one Hamiltonian cycle. The algorithm breaks selected edges of the subroutes and replaces them with inter-cluster connections. Alternative connection directions are explored recursively, producing candidate complete tours; the shortest resulting tour is selected.

The resulting complete solution is then used to generate another partition through an insertion-based perturbation. This process is repeated with a maximum of 40 solver accesses.

### Results

QTA and QBSolv have similar solution quality across the seven tested instances:

* QTA is better on **Ulysses16, Ulysses22, and wi29**.
* QBSolv is better on **Burma14, P-n16-k8, P-n19-k2, and P-n23-k8**.
* Differences in average objective value are generally small.

The major difference is the number of solver accesses:

$$
\text{QTA}: 40
$$

versus approximately

$$
\text{QBSolv}: 259\text{–}474.
$$

Thus, QTA achieves comparable quality while substantially reducing the number of times the expensive quantum/hybrid solver needs to be accessed.

The experiments use seven benchmark instances and 20 runs per instance. Cluster size is limited to 10 cities.

### Limitations

The study is explicitly preliminary. The experiments were performed with **local QBSolv rather than an actual D-Wave QPU**, so no real quantum speedup or quantum advantage is demonstrated. The tested instances are also small, and the partitioning and route-merging procedures are highly problem-specific.

A fundamental issue is that independently optimizing subroutes does not optimize the edges connecting the clusters. The classical merging procedure therefore has to recover some of the global optimization lost through decomposition.

## Self Notes

* Interesting new optimization area mentioned: **transfer optimization / evolutionary multitasking**, where useful information can be transferred between related optimization tasks rather than optimizing each task independently.

