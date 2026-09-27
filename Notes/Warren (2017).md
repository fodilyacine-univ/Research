# Small Traveling Salesman Problems

**Authors:** Richard H. Warren
**Year:** 2017
**Venue:** *Journal of Advances in Applied Mathematics*
**DOI / arXiv:** https://doi.org/10.22606/jaam.2017.22003

## Summary

Warren studies small TSP instances as preparation for solving them on quantum annealers. He investigates the structure of randomly generated TSPs, particularly how many distinct optimal tours they can have, and discusses how these properties could affect repeated quantum-annealing experiments.

The paper mainly provides a **simulation/experimental framework**, rather than demonstrating a TSP solution on quantum hardware.

## Paper Notes

* Uses a **city-position formulation**, where binary variables indicate which city is visited at each tour position.
* Discusses the difficulty of **subtour elimination**, particularly for edge-based formulations.
* Generates random TSP instances and solves them classically to determine their optimal tours.
* Studies **6-, 8-, and 10-city** instances and examines the number of distinct optimal tours.
* Finds that instances with larger optimal tour lengths tend to have more optimal tours in the studied random instances.
* Proposes using repeated quantum-annealing samples to investigate how frequently different optimal tours can be recovered.
* Discusses future experiments on D-Wave hardware and the possibility of reducing larger TSPs to smaller instances that fit the available hardware.
* Main contribution: **characterizing small TSP instances and establishing groundwork for future quantum-annealing experiments**, rather than demonstrating quantum advantage.

## Self Notes

*

