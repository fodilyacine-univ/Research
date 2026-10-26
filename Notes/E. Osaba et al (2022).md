# A Systematic Literature Review of Quantum Computing for Routing Problems

**Authors:** Eneko Osaba et al.  
**Year:** 2022  
**Venue:** IEEE Access, Vol. 10, pp. 55805–55817  
**DOI:** https://doi.org/10.1109/ACCESS.2022.3177790

## Summary

This systematic literature review examines the development of quantum computing applied to routing problems. The authors select 53 publications and analyze research trends, problem types, theoretical versus practical studies, pure quantum versus hybrid approaches, hardware platforms, influential publications, and outstanding research challenges.

The review finds that the Traveling Salesman Problem (TSP) dominates the literature, with the Vehicle Routing Problem (VRP) receiving less attention. Research activity increased substantially between 2019 and 2021, alongside greater access to quantum-computing platforms. D-Wave quantum annealers were the most frequently used hardware in the reviewed practical studies, and hybrid quantum-classical approaches became nearly as common as purely quantum approaches.

The authors identify three major challenges: developing efficient formulations for realistic routing problems, addressing quantum hardware limitations, and improving parameter selection and tuning. The review provides a useful map of early quantum-routing research, but it does not establish that quantum or hybrid algorithms outperform competitive classical optimization methods.

## Paper Notes

### 1. Methodology
- Databases: Google Scholar, Scopus, IEEE Xplore, and Web of Science.
- Search conducted in November 2021.
- Initial searches returned 1,809 records across the databases, before duplicate removal and screening.
- 95 candidate papers remained after initial filtering.
- 42 papers on quantum-inspired evolutionary algorithms were excluded.
- Final corpus: 53 publications.
- Reference-list inspection was used to identify additional relevant work.

### 2. Research trends
- 64.15% of the selected publications appeared between 2019 and 2021.
- Research activity increased as access to quantum-computing platforms improved.
- The review covers 2003/2004–2021, with a minor inconsistency in the reported starting year.

### 3. Routing problems studied
The problem categories overlap because some publications address multiple problems.

| Problem | Publications |
|---|---:|
| Traveling Salesman Problem (TSP) | 32 |
| Vehicle Routing Problem (VRP) | 13 |
| Other routing problems | 11 |

- TSP is the dominant benchmark because it is well studied and has established mathematical formulations and known solutions.
- VRP research addresses more complex constraints, including vehicle capacities, time windows, and scheduling requirements.
- Other studied problems include shortest path, longest path, Hamiltonian cycle, and postman problems.

### 4. Theoretical versus practical research
- Theoretical studies: 26.
- Practical studies: 27.
- Practical research became more common toward the end of the review period.
- Practical studies include different types of implementations, so a classical simulation, a quantum-circuit simulation, and an experiment on physical quantum hardware should not be treated as equivalent evidence.

### 5. Pure quantum versus hybrid approaches
Among the 27 practical publications:
- Pure quantum approaches: 13.
- Hybrid quantum-classical approaches: 14.

Hybrid methods combine classical optimization with quantum computation, often because current quantum hardware cannot efficiently handle the full routing problem.

Examples include:
- Classical clustering followed by quantum TSP optimization.
- Classical search combined with quantum optimization of subproblems.
- Quantum-assisted routing and scheduling algorithms.

The review establishes the prevalence of hybrid approaches, not their superiority over classical methods.

### 6. Hardware platforms
The review identifies:
- D-Wave quantum annealers: 16 publications.
- IBM gate-model quantum computers: 11 publications.
- Fujitsu Digital Annealer: 1 publication.

The device counts are not necessarily mutually exclusive. D-Wave was the most frequently used platform, particularly for QUBO-based optimization.

### 7. Influential publications
The review highlights several influential works:

- **Martoňák, Santoro, and Tosatti (2004):** *Quantum Annealing of the Traveling-Salesman Problem*. An early foundational quantum-annealing formulation of the TSP.
- **Chen and Zhang (2006):** *Optimized Annealing of Traveling Salesman Problem from the nth-Nearest-Neighbor Distribution*. Investigates an alternative annealing formulation.
- **Chen et al. (2011):** Experimental demonstration of a quantum-annealing algorithm for a four-city TSP using a nuclear-magnetic-resonance quantum simulator.
- **Warren (2013):** *Adapting the Traveling Salesman Problem to an Adiabatic Quantum Computer*. Examines how the TSP can be represented for adiabatic quantum computation.
- **Crispin and Syrichas (2013):** *Quantum Annealing Algorithm for Vehicle Scheduling*. Applies quantum-annealing ideas to vehicle scheduling.
- **Mavlet et al. (2017):** *Quantum Speedup of the Traveling-Salesman Problem for Bounded-Degree Graphs*. Investigates a theoretical quantum backtracking approach.
- **Srinivasan et al. (2018):** *Efficient Quantum Algorithm for Solving Travelling Salesman Problem: An IBM Quantum Experience*. An early gate-model implementation on a small TSP.
- **Feld et al. (2019):** *A Hybrid Solution Method for the Capacitated Vehicle Routing Problem Using a Quantum Annealer*. Decomposes CVRP into classical clustering and quantum-assisted TSP routing.
- **Irie et al. (2019):** *Quantum Annealing of Vehicle Routing Problem with Time, State and Capacity*. Extends quantum-annealing formulations to a constrained VRP.
- **Papalitsas et al. (2019):** *A QUBO Model for the Traveling Salesman Problem with Time Windows*. Investigates the incorporation of time-window constraints into a QUBO.

The review ranks publications by citation counts gathered in January 2022. Citation counts indicate influence, not algorithmic effectiveness or quantum advantage.

### 8. Main challenges and future directions

**Problem formulation**
- Develop efficient formulations for realistic routing problems.
- Reduce the number of variables and the cost of embedding logical problems onto quantum hardware.
- Investigate hybrid methods for instances too large for purely quantum approaches.

**Quantum hardware**
- Address noise and decoherence.
- Better understand how hardware limitations affect solution quality.
- Investigate error mitigation and correction.

**Parameter tuning**
- Systematically study QUBO penalty weights, algorithm parameters, and hardware settings.
- Avoid relying solely on parameters selected through intuition or limited experimentation.
- Evaluate how parameter choices affect feasibility, solution quality, and scalability.

## Self Notes
