# A Benchmark for Quantum Optimization: The Traveling Salesman Problem

**Authors:** Richard H. Warren  
**Year:** 2021  
**Venue:** *Quantum Information and Computation*, 21(7–8), 557–562  
**DOI / arXiv:** 10.22606/jaam.2018.33002

## Summary

The paper argues that the **symmetric Traveling Salesman Problem (TSP)** should be used as a standard benchmark for quantum optimization algorithms. The motivation is to have a well-defined, widely understood problem with standardized instances, known exact solutions, practical relevance, and applicability across different quantum technologies.

Warren presents seven arguments supporting TSP as a benchmark and discusses why symmetric TSP is preferable to asymmetric TSP for this purpose. The paper is primarily a methodological/position paper: it does not propose a new TSP algorithm or perform a large experimental comparison, but argues that TSP provides a useful common basis for evaluating quantum optimization methods in terms of solution quality, exactness, computational effort, and scaling.

## Paper Notes

- Proposes **symmetric TSP** as a benchmark for quantum optimization.
- Main reasons:
  - TSP is a well-established combinatorial optimization problem.
  - **TSPLIB** provides standardized benchmark instances.
  - Exact optimal solutions are available for benchmark instances, allowing independent verification.
  - TSP has established quantum-annealing formulations and implementations.
  - It has practical applications.
  - Its computational difficulty makes it relevant for studying optimization performance/scaling.
  - It is sufficiently general to be used across different quantum-computing approaches.
- Emphasizes that benchmarking should consider more than simply obtaining a feasible tour:
  - whether the **known optimum** is reached;
  - computational effort/time;
  - scaling with instance size;
  - reproducibility using common instances.
- Focuses on **exact optimization**, where the known TSPLIB optimum provides a clear reference.
- Discusses **asymmetric TSP (ATSP)** but argues that it is less suitable as a common benchmark because of weaker standardized classical infrastructure and additional formulation/connectivity difficulties.
- The paper is an **argument for a benchmark**, not a proposal for a new TSP formulation or optimization algorithm.
- No large-scale experimental comparison between quantum algorithms is performed.

## Self Notes

