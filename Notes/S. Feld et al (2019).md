# A Hybrid Solution Method for the Capacitated Vehicle Routing Problem Using a Quantum Annealer

**Authors:** Sebastian Feld, Christoph Roch, Thomas Gabor, Christian Seidel, Florian Neukart, Isabella Galter, Wolfgang Mauerer, Claudia Linnhoff-Popien  
**Year:** 2019  
**Venue:** *Frontiers in ICT*, 6, Article 13  
**DOI:** 10.3389/fict.2019.00013

## Summary

The paper investigates how the CVRP can be decomposed so that a D-Wave quantum annealer can solve part of it. The authors use a classical **2-phase heuristic**: first cluster customers into capacity-feasible groups, then solve a TSP for each cluster. They investigate three approaches—Q2Q, Q1Q, and a Hybrid Solution (HS)—and ultimately use classical clustering followed by quantum-annealing-based TSP routing.

The hybrid method is tested on established CVRP/TSP benchmark instances. It produces reasonable approximations and sometimes matches or improves upon the classical construction/2-phase heuristics considered, but does not outperform stronger classical metaheuristics. The experiments also show that the actual QPU computation is small compared with the surrounding hybrid overhead, particularly communication and embedding.

## Paper Notes

- Motivation: full CVRP QUBOs are too large/connectivity-intensive for the available D-Wave hardware.
- Uses the **2-phase heuristic**:
  \[
  \text{CVRP}\rightarrow\text{clustering}\rightarrow\text{TSP routing}.
  \]
- Investigates three approaches:
  - **Q2Q:** quantum clustering + quantum routing.
  - **Q1Q:** combined clustering/routing QUBO.
  - **HS:** classical clustering + quantum TSP routing.
- Q2Q suffers from difficulty choosing the clustering parameter.
- Q1Q suffers from competing clustering and routing objectives.
- HS therefore uses a classical clustering heuristic and sends the resulting TSPs to D-Wave/QBSolv.
- Clustering uses two seed-selection strategies: `max_distance` and `max_request`.
- TSP subproblems use the standard position-based QUBO and are solved through QBSolv/D-Wave.

### Results

**TSP routing:**

| Instance | Size | Avg. deviation from BKS |
|---|---:|---:|
| Burma14 | 14 | 0.00% |
| Ulysses16 | 16 | 0.31% |
| Ulysses22 | 22 | 2.70% |
| WesternSahara29 | 29 | 8.16% |
| Djibouti38 | 38 | 25.91% |

Performance deteriorates as the TSP subproblem grows.

**CVRP:** performance depends strongly on the clustering strategy. Examples:

| Instance | `max_distance` | `max_request` |
|---|---:|---:|
| E-n22-k4 | 2.66% | 8.53% |
| E-n33-k4 | 15.07% | 2.05% |
| E-n51-k5 | 18.75% | 6.91% |
| E-n76-k7 | 9.70% | 19.46% |

On CMT1, classical QBSolv obtained distance **557**, while the remote hybrid version obtained **556**, but the hybrid approach incurred substantially greater total runtime due to overhead around the QPU.

Overall, the HS approach can compete with the classical **construction and 2-phase heuristics** tested, but stronger classical metaheuristics generally obtain better solutions. The paper therefore does not demonstrate a quantum advantage, but demonstrates a possible framework for incorporating quantum annealing into CVRP heuristics.

## Self Notes

- The **first three sections have good references**.
- It uses **already known instances**, not randomly generated ones.
- It gave me the idea that one does not have to compare a hybrid approach to *all* classical approaches: comparing it to **classical approaches from the same family** can show the advantage (or lack thereof) of introducing the quantum component.
