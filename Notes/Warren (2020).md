# Solving the Traveling Salesman Problem on a Quantum Annealer

**Authors:** Richard H. Warren
**Year:** 2020
**Venue:** *SN Applied Sciences*
**DOI / arXiv:** https://doi.org/10.1007/s42452-019-1829-x

## Summary

Warren examines existing approaches for solving the symmetric TSP using D-Wave quantum annealers. Rather than proposing a new formulation, he compares several implementations and investigates their practical limitations, particularly subtours, embedding limits, decomposition, and the difficulty of demonstrating optimality.

The paper argues that existing experiments often show that good tours can be found, but do not necessarily demonstrate that the tours are optimal. Warren therefore proposes a more systematic experimental setup in which quantum-annealing results can be compared against known optimal solutions.

## Paper Notes

* Reviews **four existing TSP implementations** using D-Wave/quantum annealing, ranging from small directly embedded problems to larger problems using classical decomposition.
* Identifies a **7-city formulation** that can produce subtours, showing that satisfying assignment/degree constraints does not necessarily guarantee a single Hamiltonian cycle.
* Examines a **48-city TSP** solved using **QBSolv**, where the large problem is decomposed into smaller subproblems handled classically and/or quantumly.
* Reviews experiments on **14, 16, 22, 29 and 38-city** instances; smaller instances reached optimal solutions while larger ones produced approximate solutions.
* Emphasizes the distinction between finding the **lowest-energy tour observed** and proving the **global optimum**.
* Highlights practical limitations of D-Wave: limited connectivity, embedding overhead, parameter choices, hardware imperfections, and the need for classical decomposition.
* Proposes a more controlled TSP experiment using **known optimal solutions and repeated runs**, allowing success rate and optimality gap to be measured.
* Overall, the paper presents TSP on quantum annealers as a **hybrid classical–quantum computational pipeline**, rather than a purely quantum solution.

## Self Notes

*

