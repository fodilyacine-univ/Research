# GPS: A New TSP Formulation for Its Generalizations Type QUBO

**Authors:** Saúl González-Bermejo, Guillermo Alonso-Linaje, Parfait Atchade-Adelomou
**Year:** 2022
**Venue:** *Mathematics*, 10(3), 416
**DOI:** 10.3390/math10030416
**arXiv:** 2110.12158

## Summary

The paper proposes **GPS**, a QUBO formulation for the TSP designed to reduce the number of binary variables required by previous formulations, particularly MTZ-based QUBOs. Instead of explicitly encoding the position/order of each city with integer variables, GPS represents the **relative ordering of every pair of cities** using three binary states. Actual tour edges are encoded within these states, while quadratic transitivity penalties prevent inconsistent cyclic orderings and therefore subtours.

The authors then generalize the formulation to the **VRP** by adding a vehicle index and additional states distinguishing whether two cities belong to the same vehicle or different vehicles. A shared pairwise ordering variable is used to impose a consistent global ordering across vehicles, allowing the transitivity mechanism to be retained. The paper also discusses further generalizations and evaluates the formulations using classical optimization and simulated quantum annealing rather than demonstrating a large-scale hardware advantage.

## Paper Notes

### TSP formulation

GPS uses three binary variables for each ordered pair of cities:

$$
x_{i,j,0},\quad x_{i,j,1},\quad x_{i,j,2}.
$$

They represent:

* \(r=0\): \(i\) is before \(j\), but \(i\to j\) is not a tour edge.
* \(r=1\): \(i\) is before \(j\) and \(i\to j\) is a tour edge.
* \(r=2\): \(j\) is before \(i\), and \(i\to j\) is not a tour edge.

The formulation enforces:

$$
\sum_r x_{i,j,r}=1
$$

for each pair, together with one incoming and one outgoing tour edge per city.

The distance objective is carried by the \(r=1\) variables:

$$
H_{\mathrm{distance}}
=
\sum_{i,j}d_{ij}x_{i,j,1}.
$$

### Subtour elimination

The central idea is to encode **relative ordering instead of absolute positions**.

For three cities \(i,j,k\), the ordering must satisfy transitivity:

$$
i<j,\quad j<k
\quad\Rightarrow\quad
i<k.
$$

The authors construct a quadratic penalty that is nonzero for the two inconsistent configurations:

$$
(0,0,1)
\quad\text{and}\quad
(1,1,0).
$$

Thus a cycle such as

$$
A<B,\quad B<C,\quad C<A
$$

cannot satisfy the ordering constraints without incurring a penalty.

This provides subtour elimination through **pairwise ordering + transitivity**, rather than MTZ-style explicit order variables.

### Variable count

The paper contrasts GPS with formulations requiring approximately:

$$
O(N^3)
$$

native variables and

$$
O(N^2\log N)
$$

variables for their MTZ QUBO treatment.

GPS uses approximately:

$$
\boxed{3N^2}
$$

binary variables.

The main idea is therefore:

> Do not encode the exact position of every city; encode only the relative order of pairs of cities.

This reduces the binary-variable count, although the resulting transitivity constraints can still create many couplers.

### VRP extension

For the VRP, the variables become vehicle-specific:

$$
x_{i,j,r,q},
$$

where \(q\) identifies the vehicle.

The initial formulation uses five states:

$$
r\in\{0,1,2,3,4\}.
$$

The additional states allow the formulation to distinguish whether two cities belong to the same vehicle or different vehicles.

The formulation imposes:

* one state for every pair/vehicle;
* one incoming and outgoing edge for each customer;
* assignment of each customer to exactly one vehicle;
* route continuity;
* depot/start/end constraints;
* consistency between vehicle-specific pairwise ordering and a shared global ordering;
* transitivity of that global ordering.

A pairwise global-order variable \(a_{ij}\) links the vehicle-specific states to a common ordering. The transitivity constraints then prevent inconsistent cycles.

The initial VRP formulation requires approximately

$$
5N^2Q
$$

binary variables, where \(Q\) is the number of vehicles. The paper subsequently develops a reduced formulation of approximately

$$
\boxed{3N^2Q}.
$$

### Evaluation and Results

The authors test the TSP formulations on small instances using D-Wave's Ocean tools and a simulated quantum annealer, comparing **GPS, native, and MTZ** formulations in qubit count, runtime, and tour length. GPS substantially reduces the number of logical variables; for \(N=12\), it uses **507 qubits**, compared with **1066 for MTZ** and **2028 for the native formulation**. GPS generally produces valid tours with comparable solution quality, although it is not consistently faster or better in tour length.

MTZ performs poorly in some experiments, including failing to obtain a feasible solution for one \(N=12\) instance. The VRP extension is also demonstrated on small instances (e.g. \(N=8,\ Q=3\), requiring 1778 qubits), but no large-scale benchmark or quantum advantage is demonstrated. The experiments therefore mainly validate **formulation feasibility and variable reduction**, rather than demonstrating superior optimization performance.


## Self Notes

Possible alternative to global ordering: The VRP does not naturally define an ordering between cities assigned to different vehicles. Instead of imposing an artificial global order, consider introducing an explicit pairwise state meaning “incomparable / different vehicles.” Pairs would then have a before/after relation when they belong to the same route, and be incomparable otherwise, effectively modeling the VRP as a partial order. This could simplify the conceptual formulation, although its effect on the QUBO size and transitivity constraints remains to be investigated.
