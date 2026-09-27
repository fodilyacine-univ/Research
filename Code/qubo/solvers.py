from dwave.samplers import (
    TabuSampler,
    PathIntegralAnnealingSampler
)

from qubo.index import QUBO

def gurobi(qubo: QUBO) -> dict[str, int]:
    import gurobipy as gp
    from gurobipy import GRB

    model = gp.Model("QUBO")
    model.setParam("OutputFlag", 0)

    x = {
        variable: model.addVar(
            vtype=GRB.BINARY,
            name=variable
        )
        for variable in qubo.variables
    }

    objective = qubo.get_offset()

    # Linear terms
    for i, variable in enumerate(qubo.variables):
        objective += qubo.linear[i] * x[variable]

    # Quadratic terms
    for i in range(len(qubo.variables)):
        for j in range(i + 1, len(qubo.variables)):
            coefficient = (
                qubo.quadratic[i, j]
                + qubo.quadratic[j, i]
            )

            if coefficient != 0:
                u = qubo.variables[i]
                v = qubo.variables[j]

                objective += coefficient * x[u] * x[v]

    model.setObjective(objective, GRB.MINIMIZE)

    model.optimize()

    if model.Status != GRB.OPTIMAL:
        raise RuntimeError(
            f"Gurobi did not find an optimal solution. "
            f"Status: {model.Status}"
        )

    return {
        variable: int(x[variable].X > 0.5)
        for variable in qubo.variables
    }

def tabu(
    qubo: QUBO,
    num_reads: int = 100
) -> dict[str, int]:

    bqm = qubo.to_bqm()

    sampler = TabuSampler()

    sampleset = sampler.sample(
        bqm,
        num_reads=num_reads
    )

    return {
        variable: int(value)
        for variable, value in sampleset.first.sample.items()
    }


def sqa(
    qubo: QUBO,
    num_reads: int = 100
) -> dict[str, int]:

    bqm = qubo.to_bqm()

    sampler = PathIntegralAnnealingSampler()

    sampleset = sampler.sample(
        bqm,
        num_reads=num_reads
    )

    return {
        variable: int(value)
        for variable, value in sampleset.first.sample.items()
    }

class LNS:
    def __init__(self, qubo):
        self.qubo = qubo
        self.current_solution = None
        self.current_energy = None
        self.neighborhood_selector = None
        self.sub_solver = None
        self.candidate_selection = None

    def set_qubo(self, qubo: QUBO):
        self.qubo = qubo
        if self.current_solution != None:
            self.current_energy = qubo.evaluate(self.current_solution)

    def set_current_solution(self, solution: dict[str, int]):
        self.current_solution = solution
        self.current_energy = self.qubo.evaluate(solution)

    def set_neighborhood_selector(self, neighborhood_selector):
        self.neighborhood_selector = neighborhood_selector
    
    def set_sub_solver(self, sub_solver):
        self.sub_solver = sub_solver
    
    def set_candidate_selection(self, candidate_selection):
        self.candidate_selection = candidate_selection
    
    def next_iteration(self):
        neighborhood = set(self.neighborhood_selector())
        
        fixed = {
            variable: value
            for variable, value in self.current_solution.items()
            if variable not in neighborhood
        }

        reduced_qubo = self.qubo.fix_variables(fixed)

        reduced_solution = self.sub_solver(reduced_qubo)

        candidate_solution = self.current_solution.copy()
        candidate_solution.update(reduced_solution)

        if self.candidate_selection(candidate_solution):
            self.set_current_solution(candidate_solution)
    