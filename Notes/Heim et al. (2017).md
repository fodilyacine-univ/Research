# Designing Adiabatic Quantum Optimization: A Case Study for the Traveling Salesman Problem

**Authors:** Bettina Heim, Ethan W. Brown, Dave Wecker, Matthias Troyer
**Year:** 2017
**Venue:** arXiv (quant-ph)
**DOI / arXiv:** arXiv:1702.06248v1; DOI: 10.48550/arXiv.1702.06248

## Summary

The paper studies how the **choice of TSP encoding and quantum dynamics** affects the suitability of a problem for adiabatic/quantum annealing. Using TSP as a case study, the authors compare the standard city-position (permutation) encoding with an edge-based encoding. Their central argument is that a mathematically valid encoding can nevertheless produce unfavorable quantum dynamics: with a standard transverse-field driver, useful changes between nearby tours can require many single-qubit flips, leading to exponentially suppressed transitions.

The edge-based encoding makes these changes more local, but introduces the problem of subtours and difficult inequality constraints. The authors find that iterative subtour suppression works reasonably with an exact solver but poorly with heuristic annealing because excited-state solutions can lead to inappropriate constraints. They therefore argue that analog quantum annealing faces significant difficulties for this TSP formulation and discuss digital quantum annealing as a way to implement more flexible dynamics and constraints.

## Paper Notes

The paper begins with the standard **city-position formulation**:

$$
a_{ik} =
\begin{cases}
1 & \text{city }i\text{ is visited at position }k,\\
0 & \text{otherwise}.
\end{cases}
$$

The tour-length objective is

$$
H_l=\sum_{i,j,k}d_{ij}a_{ik}a_{j,k+1},
$$

with constraints enforcing exactly one city at each position and exactly one position for each city. These are incorporated as quadratic penalties into

$$
H_P=H_l+\eta H_c.
$$

For an \(N\)-city problem, the formulation requires \(O(N^2)\) logical variables, but the resulting connectivity can lead to \(O(N^3)\) qubits after embedding on hardware with bounded connectivity.

The authors then examine the usual transverse-field driver,

$$
H_D=\Gamma\sum_{i,j}\sigma^x_{ij},
$$

which induces single-spin flips. They use a **2-opt modification** as an example of an important classical change between similar tours. In the position encoding, resolving a crossing can require \(m=O(N)\) variable flips. They argue that the corresponding transition probability is suppressed approximately as

$$
\left(\frac{\Gamma}{\Delta}\right)^m,
$$

so the transition becomes exponentially suppressed with problem size. The point is not that a quantum annealer literally performs a classical 2-opt operation, but that the encoding makes configurations connected by such useful tour changes have large Hamming distance under a local driver.

They therefore propose an **edge-based encoding**,

$$
a_{ij}=1
\quad\text{if edge }(i,j)\text{ belongs to the tour}.
$$

The objective becomes simply

$$
H_l'=\sum_{i,j}d_{ij}a_{ij}.
$$

A 2-opt move then changes only four edge variables, while a \(k\)-opt move changes \(2k\) variables, independently of \(N\). The authors also suggest restricting each city to its \(L\) nearest candidate edges, reducing the number of logical variables from \(O(N^2)\) to \(O(NL)\).

The main difficulty is **subtour elimination**. They impose degree-two constraints,

$$
H_c'=\sum_i
\left(2-\sum_{j\ne i}a_{ij}\right)^2,
$$

which ensure that every city belongs to a closed loop, but do not ensure that all cities belong to the same loop. The resulting solution can therefore consist of multiple subtours.

Their proposed remedy is **iterative subtour suppression**: anneal the minimally constrained problem, identify subtours, add penalties preventing those particular subtour separations, and anneal again. The relevant constraint is an inequality requiring at least one connection between two subsets of cities. Because such inequalities are difficult to implement using only quadratic Ising couplings, they introduce approximate quadratic penalties for the connection counts encountered in their instances.

They test the procedure on random TSP instances with \(N=8,12,16\). For \(N=12\), they use 100 random instances. With the exact CPLEX solver, the iterative procedure finds the optimal TSP solution for 95% of the tested systems after two iterations. However, the procedure performs poorly with simulated annealing, simulated quantum annealing, and quantum annealing. The reason is that heuristic annealers frequently return excited states whose subtours have a different number of connections from the true ground-state subtours; adding constraints based on these states can therefore introduce incorrect restrictions.

Finally, the authors discuss **digital quantum annealing** on gate-model quantum computers. They argue that a programmable digital implementation can support more flexible quantum dynamics, including multi-qubit operations corresponding to 2-opt-like moves, and can implement inequality constraints more efficiently than an analog Ising machine. They conclude that the difficulties encountered with analog quantum annealing arise substantially from the restrictions of local interactions and quadratic penalty functions, rather than simply from the TSP itself.

## Self Notes

* The paper's use of 2-opt is interesting, but I should distinguish **a classical 2-opt neighborhood move** from an actual **quantum transition**. The annealer does not literally execute 2-opt.
* The stronger interpretation seems to be that, under a **local transverse-field driver**, Hamming distance between important configurations affects the order of the tunneling process.
* I should investigate how dependent their argument is on the choice of driver \(H_D\). A different multi-qubit driver could potentially make nonlocal transformations more direct.
* The edge formulation improves locality but creates a difficult global feasibility problem: **subtour elimination**. This illustrates the trade-off between formulation locality and constraint complexity.
* Their iterative constraint-generation method seems particularly vulnerable when the annealer returns excited states: the observed subtours may not reveal the structure of the true optimum.
* Interesting connection to my own work: rather than redesigning the entire formulation, could a classical neighborhood-selection mechanism provide the annealer with a smaller/localized search space?
* Important distinction for later research: the paper studies whether the **encoding itself** makes useful configurations locally connected under quantum dynamics; my approach may instead modify the **search space presented to the annealer**.

