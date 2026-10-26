# Combinatorial Optimization with Quantum Computers

**Authors:** Francisco Chicano et al.  
**Year:** 2025  
**Venue:** Engineering Optimization, Volume 57, Issue 1, pp. 208–233  
**DOI / arXiv:** [10.1080/0305215X.2024.2435538](https://doi.org/10.1080/0305215X.2024.2435538) / [arXiv:2412.15778](https://arxiv.org/abs/2412.15778)

## Summary

This paper provides a practical introduction to solving combinatorial optimization problems using quantum computers, covering both quantum annealing and gate-based quantum computing. Its central objective is to explain the process of transforming a classical optimization problem into a representation suitable for quantum hardware. The authors discuss binary encodings for different variable types, the incorporation of constraints through penalty functions and slack variables, the reduction of higher-order polynomial terms to quadratic form, and the implementation of the resulting models using D-Wave's quantum annealers and QAOA. Practical examples illustrate the complete workflow, from mathematical formulation to execution and interpretation of results.

The paper emphasizes that successful quantum optimization depends not only on the quantum algorithm but also on the formulation of the original problem. Encoding choices, penalty coefficients, auxiliary variables, and hardware connectivity all influence the resulting implementation. The authors identify several open challenges, including selecting effective penalty coefficients, reducing quadratization overhead, choosing appropriate formulations, and establishing practical quantum advantage. The paper's contribution is primarily educational and methodological: it provides a systematic introduction to quantum optimization without proposing a new algorithm or demonstrating quantum advantage over classical methods.

## Paper Notes

### 1. QUBO and Ising formulations

The paper introduces Quadratic Unconstrained Binary Optimization (QUBO), in which the objective is a quadratic function of binary variables:

\[
\min_{x\in\{0,1\}^n} f(x),
\qquad
f(x)=x^\top Qx+c.
\]

The Ising representation instead uses spin variables \(s_i\in\{-1,+1\}\), with an energy function containing linear biases and pairwise interactions. The two representations are related through

\[
s_i=1-2x_i.
\]

QUBO provides a convenient mathematical representation for constructing optimization models, while Ising Hamiltonians are natural for quantum annealing.

### 2. Encoding optimization problems

The authors explain how to represent different types of decision variables using binary variables:

- **Integer variables:** Binary encodings represent bounded integer values using weighted sums of binary variables.
- **Categorical variables:** One-hot encoding assigns a binary variable to each alternative and imposes a constraint requiring exactly one alternative to be selected.
- **Permutations:** Binary variables \(x_{j,k}\) indicate whether element \(k\) occupies position \(j\). Row and column constraints ensure that each position contains exactly one element and each element appears exactly once.

Permutation encoding is relevant to the Traveling Salesperson Problem (TSP), where \(x_{j,k}\) indicates whether city \(k\) is visited at position \(j\). The assignment constraints ensure a valid permutation, while the objective must separately account for travel costs between consecutive cities.

### 3. Constraint handling through penalties

Constrained optimization problems can be transformed into unconstrained binary objectives by incorporating penalties.

For an equality constraint \(h(x)=0\), the authors use

\[
F(x)=f(x)+Ph(x)^2,
\]

where \(f(x)\) is the original objective and \(P>0\) is a penalty coefficient.

For an inequality constraint \(h(x)\leq 0\), a nonnegative slack variable \(s\) can convert it into an equality:

\[
h(x)+s=0.
\]

The equality can then be enforced through the penalty

\[
P(h(x)+s)^2.
\]

Slack variables must themselves be encoded in binary, potentially increasing the number of variables and interactions.

The authors derive a sufficient penalty bound for a pseudo-Boolean objective

\[
f(x)=\sum_{S\subseteq[n]}a_S\prod_{j\in S}x_j.
\]

Using bounds on the objective's possible variation, they obtain

\[
P=\operatorname{ub}(f)-\operatorname{lb}(f)+1
 =1+\sum_{S\neq\emptyset}|a_S|.
\]

This provides a sufficient bound for the penalty construction, but it is not necessarily the smallest effective penalty. Excessively large coefficients can also create difficulties when representing the problem on quantum hardware.

### 4. Quadratization of higher-order objectives

After binary encoding and constraint incorporation, the objective may contain products of more than two binary variables. Such terms cannot be represented directly by a QUBO.

The authors discuss reducing polynomial degree through auxiliary variables and penalty functions. For example, a cubic term

\[
x_1x_2x_3
\]

can be replaced by \(x_1z\), provided that \(z=x_2x_3\) is enforced.

A Rosenberg penalty for this relationship is

\[
P(x_2x_3-2x_2z-2x_3z+3z).
\]

This converts a higher-order interaction into quadratic interactions, at the cost of introducing an auxiliary variable and additional terms.

The paper also discusses local transformations that reduce polynomial degree. The appropriate method depends on the structure of the original objective.

The central trade-off is that quadratization makes the model compatible with QUBO-based hardware but can increase its variable count and interaction complexity.

### 5. Quantum annealing and hardware embedding

Once a QUBO has been constructed, it can be converted into an equivalent Ising model and mapped onto the connectivity graph of a quantum annealer.

Because the hardware cannot necessarily connect every pair of logical variables directly, minor embedding may represent a logical variable using a chain of physical qubits. Couplings within a chain encourage those qubits to agree.

Embedding can increase the physical-qubit requirements and introduce additional sources of error. The logical size of a QUBO therefore does not fully describe the resources required to solve it on hardware.

The authors demonstrate the workflow using a small MAX-SAT problem and D-Wave's Ocean SDK. Their example illustrates the construction of the QUBO, embedding, execution, and interpretation of the returned samples. It demonstrates feasibility of implementation, not quantum advantage.

### 6. Gate-based optimization and QAOA

The paper also introduces the Quantum Approximate Optimization Algorithm (QAOA), a hybrid quantum-classical algorithm.

Given an objective \(f(x)\), the problem Hamiltonian is constructed so that

\[
H_P|x\rangle=f(x)|x\rangle.
\]

QAOA prepares a parameterized state by alternating problem and mixer unitaries:

\[
U_P(\gamma_k)=e^{-i\gamma_k H_P},
\]

\[
U_M(\beta_k)=e^{-i\beta_k H_M},
\qquad
H_M=\sum_i X_i.
\]

Starting from a uniform superposition, the circuit applies \(p\) alternating layers of these operations. A classical optimizer adjusts the parameters \(\boldsymbol{\gamma}\) and \(\boldsymbol{\beta}\) to improve the expected objective value.

The authors demonstrate this procedure using Qiskit, COBYLA, and a quantum simulator. The example illustrates circuit construction, classical parameter optimization, and the probabilistic distribution of measured solutions. It does not demonstrate performance on physical gate-based hardware.

### 7. Limitations and future directions

The paper identifies several unresolved challenges:

- **Penalty selection:** Sufficient penalty bounds may be unnecessarily conservative, and finding effective coefficients remains important.
- **Quadratization overhead:** Auxiliary variables and additional interactions can make the resulting model more expensive.
- **Formulation selection:** Different encodings of the same problem can produce different implementation costs and optimization performance.
- **Hardware constraints:** Connectivity, embedding, and coefficient scaling affect the practical execution of a QUBO.
- **Quantum advantage:** The examples do not establish that quantum methods outperform classical optimization.
- **Further applications:** The authors discuss black-box objectives, automatic QUBO construction, and multi-objective optimization as areas for further research.

The paper's overall message is that quantum optimization requires careful mathematical modeling and implementation, and that practical quantum advantage remains an open question.

## Self Notes

- they have good section on formulation, on different ways to formulate for different cases (good references)
- code for QAOA
- good references
- more detailed read would be useful
