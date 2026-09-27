from dataclasses import dataclass, field

from tsp.problem import TSP
from tsp.TimeIndex import TimeIndexTSP, QUBOAdapter
from tsp.neighborhood import random_removal, segment_removal, related_removal, worst_removal, exchange_impact_removal, toggle_neighborhood, relocate_neighborhood, swap_neighborhood
from qubo.solvers import sqa
from qubo.solvers import LNS
from qubo.neighborhood import Neihborhood
from qubo.index import QUBO
import random

@dataclass
class LNSResult:
    tour: list[int]
    qubo_costs: list[float]
    iterations: int

@dataclass
class NeighborhoodConfig:
    method: str
    params: dict = field(default_factory=dict)
    
def lns(
    tsp: TSP,
    initial_solution: dict[str, int]|None = None,
    iterations: int = 10,
    neighborhood_config: NeighborhoodConfig = NeighborhoodConfig(method="random_positions", params={"k":5}),
    sub_solver=sqa
) -> LNSResult:

    # -------------------------
    # Problem / formulation
    # -------------------------
    formulation = TimeIndexTSP(tsp)
    qubo_adapter = QUBOAdapter(formulation)

    max_distance = max(
        tsp.get_distance(i, j)
        for i in range(tsp.n)
        for j in range(tsp.n)
    )

    qubo = qubo_adapter.to_qubo({
        "city_once": max_distance,
        "time_once": max_distance,
    })
    qubo_neighborhood = Neihborhood(qubo)

    # -------------------------
    # LNS
    # -------------------------

    lns_solver = LNS(qubo)
    if initial_solution == None:
        initial_solution = {f"x_{i}_{t}": 1 if i == t else 0 for i in range(tsp.n) for t in range(tsp.n)}

    lns_solver.set_current_solution(initial_solution)

    # Neighborhood
    def neighborhood_selector():
        config = neighborhood_config

        if config.method == "random_variables":
            return qubo_neighborhood.random_variables(
                lns_solver.current_solution,
                **config.params
            )
        
        if config.method == "variable_energy":
            return qubo_neighborhood.energy(
                lns_solver.current_solution,
                **config.params
            )
        
        if config.method == "variable_energy_bfs":
            return qubo_neighborhood.energy_bfs(
                lns_solver.current_solution,
                **config.params
            )
        
        if config.method == "variable_energy_pfs":
            return qubo_neighborhood.energy_pfs(
                lns_solver.current_solution,
                **config.params
            )
        
        if config.method == "random_removal":
            return random_removal(
                lns_solver.current_solution,
                **config.params
            )

        if config.method == "segment_removal":
            return segment_removal(
                lns_solver.current_solution,
                **config.params
            )

        if config.method == "related_removal":
            return related_removal(
                tsp,
                lns_solver.current_solution,
                **config.params
            )
        
        if config.method == "worst_removal":
            return worst_removal(
                tsp,
                lns_solver.current_solution,
                **config.params
            )
        
        if config.method == "exchange_impact_removal":
            return exchange_impact_removal(
                tsp,
                lns_solver.current_solution,
                **config.params
            )
        
        if config.method == "toggle_neighborhood":
            return toggle_neighborhood(
                qubo,
                lns_solver.current_solution,
                **config.params
            )
        
        if config.method == "relocate_neighborhood":
            return relocate_neighborhood(
                qubo,
                lns_solver.current_solution,
                **config.params
            )
        
        if config.method == "swap_neighborhood":
            return swap_neighborhood(
                qubo,
                lns_solver.current_solution,
                **config.params
            )


        raise ValueError(
            f"Unknown neighborhood method: {config.method}"
        )

    lns_solver.set_neighborhood_selector(
        neighborhood_selector
    )

    # Subproblem solver
    lns_solver.set_sub_solver(sub_solver)

    # Candidate acceptance
    def accept_candidate(candidate):
        return (
            qubo.evaluate(candidate)
            < lns_solver.current_energy
        )

    lns_solver.set_candidate_selection(
        accept_candidate
    )
    
    # -------------------------
    # Experiment tracking
    # -------------------------

    qubo_costs = [lns_solver.current_energy]
    print(lns_solver.current_energy)
    for _ in range(iterations):
        lns_solver.next_iteration()
        solution = lns_solver.current_solution
        qubo_costs.append(lns_solver.current_energy)
        print(lns_solver.current_energy)

    # -------------------------
    # Final result
    # -------------------------

    solution = lns_solver.current_solution

    feasible = formulation.is_feasible(solution)

    if feasible:
        final_tour = formulation.decode_tour(solution)
    else:
        final_tour = []

    return LNSResult(
        tour=final_tour,
        qubo_costs=qubo_costs,
        iterations=iterations,
    )