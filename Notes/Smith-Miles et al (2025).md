# introduction:
- statements about classical computers solving TSP are usually undermining and misleaing, as a classical approache can solve TSP instances of milions of cities in minutes, and prove optimiality for thousands of cities
- grover's parallel search of all possibilities has to be accompanied with a redution of the search space (current quantum computers too small and noisy). (Moylett et al 2017), (Ambainis et al 2019) 
- current approaches dont even use grover, they use QUBO
- evidence of quantum advantage ? two cases: near-term nisq era (Preskill 2018), and future where quantum computers have plenty of qubits and are fault tolerant (Nielsen and Chuang 2010).
- we are in nisq era, much of the test are done on future position of quantum computers
- for provable near-term advantage: ability, competitiveness, scalability, hardware competitiveness.
- survey on ability 
- the challenges for quantum approaches to constrained optimisation problems like the TSP are comprehensively described in a recent survey paper (Abbas et al 2023)
- poorly suitedness to the TSP, drawing analogies from lessons from efforts in the 1980s
- scope is only on TSP, other problems have been shown to be not suited for QC (Jattana et al 2020), while others show promise (Klemm et al 2012, Sathe et al 2023)
# Quantum optimisation of QUBO problems
- Two main quantum-optimization strategies: (i) general-purpose quantum algorithms for QUBO problems, using quantum hardware alone or with a classical outer loop (Warren, 2013; Lucas, 2014; Heim et al., 2017); and (ii) hybrid quantum-classical methods that use quantum computing to accelerate classical optimization heuristics (Ambainis et al., 2019; Montanaro, 2020).
- Research is shifting toward hybridization: General-purpose QUBO solvers are unlikely to achieve quantum advantage without exploiting problem-specific combinatorial structure. Hybrid approaches combine classical methods such as dynamic programming or branch-and-bound with quantum search/amplitude amplification, but these remain largely theoretical and have not yet demonstrated practical applicability or scalability (Ambainis et al., 2019; Montanaro, 2020).
- two competing methods: QA, VQA
- VQAs (Cerezo et al 2021), QAOA (Farhi et al 2014)
- other ideas
# can quantum computers solve the TSP
- (Salehi et al 2022, Villar-Rodriguez et al 2022)
- (Hopfield and Tank 1985), (Wilson and Pawley 1988, Smith 1996, 1999)
- (Srinivasan et al 2018).
- (Ruan et al 2020, Villar-Rodriguez et al 2022)
- results from two decades: 
    - How best to formulate the TSP for QUBO-based quantum approaches?
    - How to find the minimum energy state of the Hamiltonian?
    - How do QA and QAOA compare in terms of effectiveness?
    - How can TSP-specific knowledge be integrated to improve performance?
    - How can larger instances be solved with current hardware limitations?
