# Optimizing the optimizer: decomposition techniques for quantum annealing

**Authors:** Gideon Bass, Maxwell Henderson, Joshua Heath, Joseph Dulny III
**Year:** 2021
**Venue:** *Quantum Machine Intelligence*, 3, Article 10
**DOI / arXiv:** 10.1007/s42484-021-00039-9 / arXiv:2001.06079

## Summary

The paper studies how large QUBO problems can be decomposed into smaller sub-QUBOs that can be solved on quantum annealers. The authors compare several heterogeneous decomposition strategies across problems with very different graph structures: artificial time-structured QUBOs (DBG), TSP, satellite sub-constellation assignment (SCA), and military maintenance planning (MWP).

The main result is that **Qbsolv performs best overall** among the tested approaches, generally producing the best solution quality across the problem classes. ICH is often the second-best method. The experiments also show that decomposition performance depends strongly on QUBO graph structure: methods exploiting a particular structure can work well when that structure exists but degrade when it disappears. Iteratively propagating information from solved subproblems into the remaining QUBO appears particularly important for solution quality. The paper does not demonstrate quantum advantage.

## Paper Notes

The motivation is that practical QUBOs can contain thousands or millions of variables, while quantum annealers have limited qubit counts and restricted connectivity. A heterogeneous approach therefore solves smaller QUBOs on the QPU while performing decomposition, recombination, and other processing classically.

### Problems

**Deep Boltzmann Graph (DBG):**
An artificial family of QUBOs with variables arranged in layers representing time. Couplings initially occur only between nearby layers, with the connectivity range progressively increased to produce less structured and eventually random/dense graphs. This tests how decomposition methods behave under different graph structures.

**TSP:**
Symmetric TSP using the Lucas time-indexed QUBO formulation. They test random fully connected instances with 11, 20, 50, and 100 cities together with TSPLIB instances.

**Satellite Sub-Constellation Assignment (SCA):**
Formulated as a weighted \(k\)-clique problem. The original instance can contain over one million nodes and potentially \(10^{14}\) couplings. For the tested 27-satellite instance, the graph is reduced by thresholding weights at the 99th percentile and restricting candidate sub-constellation sizes to 3–5, producing a 1,013-variable fully connected QUBO.

**Military Maintenance Planning (MWP):**
A job-shop-like scheduling problem. Variables \(x_{(R_i,L_j,T_k)}\) represent assigning repair \(R_i\) to facility \(L_j\) at time \(T_k\), with constraints involving release/due dates, facility capacity, repair type, duration, and costs. The tested reduced instance has 2,280 variables but very low edge density (0.0026).

### Decomposition methods

**Partitioning by Connectedness (PCD):**
Designed for time-structured QUBOs. A spring layout followed by PCA is used to identify a principal spatial/temporal axis, and cuts are made along this axis until the resulting components are small enough to embed. The subproblem solutions are then greedily recombined.

**Freeze-and-Anneal (FA):**
A genetic algorithm identifies variables that are sufficiently stable across a population of solutions. These variables are frozen, reducing the QUBO until the remaining problem can be solved on the QPU.

**Iterative Centrality Heuristic (ICH):**
Repeatedly selects a high-degree central variable and a neighborhood around it, solves that sub-QUBO, fixes the resulting assignments in the global solution, and modifies biases of remaining variables according to the solved assignments' couplings. This propagates information from each subproblem into subsequent ones.

**Qbsolv:**
D-Wave's hybrid decomposition solver, using QPU subproblem solving together with classical tabu-search optimization. The experiments vary `NumRepeats`; larger values generally improve robustness/quality somewhat but substantially increase runtime.

### Experimental setup

The experiments use a D-Wave 2000Q. They evaluate solution quality, runtime, embedding time, and device-response time. A 30-minute runtime limit is imposed for the main experiments.

The dataset contains 104 instances: 88 DBG, 14 TSP, 1 SCA, and 1 MWP. Twelve additional QHOT instances are used for more detailed comparisons of the decomposition methods.

### Results

**DBG:** Qbsolv performs best overall, with ICH generally second. PCD can exploit the temporal structure but becomes increasingly expensive as the graph becomes less locally connected or denser. FA is generally weak and close to the random baseline. The results show that exploiting graph structure does not automatically lead to the best method; the computational cost of identifying and embedding the decomposition also matters.

**TSP:** Qbsolv again performs best overall. Scaling is still difficult despite decomposition: among six tested 100-city instances, only one is solved within the 30-minute limit. Thus decomposition allows larger QUBOs to be attacked but does not remove the underlying optimization difficulty.

**SCA:** The reduced 1,013-variable fully connected instance strongly favors Qbsolv. Qbsolv obtains a feasible solution with 0 broken constraints in about 139 s. ICH is substantially worse and slower; PCD performs particularly poorly because the fully connected graph contains little useful structure for its partitioning mechanism.

**MWP:** Qbsolv again obtains the best overall result in about 40 s. PCD obtains a reasonably competitive solution but requires much longer. ICH eventually obtains a similar energy to Qbsolv but takes roughly 10,500 s, illustrating that its performance deteriorates on the very sparse MWP graph.

Overall, Qbsolv is the most robust across the very different graph structures tested. ICH is generally competitive, while PCD is highly dependent on the presence of exploitable structure and FA is generally weaker.

### Main conclusions

The authors identify **iterative propagation of subproblem information** as an important factor in obtaining good global solutions. Methods that solve subproblems and then modify the remaining QUBO based on those solutions tend to outperform approaches that simply partition the original problem and recombine independent solutions.

They also emphasize the importance of **embedding reuse**, since repeatedly finding embeddings can become a significant part of the runtime.

The paper demonstrates that heterogeneous decomposition can make QUBOs much larger than the physical quantum hardware's capacity approachable, but it does **not** demonstrate quantum advantage. Much of the computation remains classical, and performance depends heavily on decomposition, embedding, and classical processing.

## Self Notes

