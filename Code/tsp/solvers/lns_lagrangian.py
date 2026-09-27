from dataclasses import dataclass, field
import random

from tsp.problem import TSP
from tsp.TimeIndex import (
    TimeIndexTSP,
    QUBOAdapter as RefQUBOAdapter
)
from tsp.Lagrangian import (
    TimeIndexAugmentedLagrangian,
    QUBOAdapter,
)

from qubo.solvers import sqa, LNS
from qubo.neighborhood import Neihborhood

import numpy as np

@dataclass
class LNSResult:
    tour: list[int]
    qubo_costs: list[float]
    feasible: bool
    iterations: int


@dataclass
class NeighborhoodConfig:
    method: str
    params: dict = field(default_factory=dict)


def lns_lagrangian(
    tsp: TSP,
    iterations: int = 10,
    neighborhood_config: NeighborhoodConfig = NeighborhoodConfig(
        method="toggle",
        params={"min_variables": 20},
    ),
    sub_solver=sqa,
    seed: int = 0,
) -> LNSResult:

    # ============================================================
    # Problem / formulation
    # ============================================================

    formulation = TimeIndexTSP(tsp)

    lagrangian = TimeIndexAugmentedLagrangian(
        formulation
    )

    qubo_adapter = QUBOAdapter(
        lagrangian
    )

    max_distance = max(
        tsp.get_distance(i, j)
        for i in range(tsp.n)
        for j in range(tsp.n)
    )
    ref_adapter = RefQUBOAdapter(formulation)
    qubo_ref = ref_adapter.to_qubo({
        "city_once": max_distance,
        "time_once": max_distance,
    })
    # Initial QUBO
    qubo = qubo_adapter.to_qubo()

    qubo_neighborhood = Neihborhood(qubo)

    # ============================================================
    # Initial solution
    # ============================================================

    lns_solver = LNS(qubo)

    initial_solution = {f"x_{i}_{t}": (i+t)%2 for i in range(tsp.n) for t in range(tsp.n)}

    lns_solver.set_current_solution(
        initial_solution
    )

    # ============================================================
    # Neighborhood selector
    # ============================================================

    def neighborhood_selector():

        config = neighborhood_config

        # --------------------------------------------------------
        # Generic QUBO neighborhoods
        # --------------------------------------------------------

        if config.method == "random_variables":
            return qubo_neighborhood.random(
                lns_solver.current_solution,
                **config.params,
            )

        if config.method == "variable_energy":
            return qubo_neighborhood.energy(
                lns_solver.current_solution,
                **config.params,
            )

        if config.method == "variable_energy_bfs":
            return qubo_neighborhood.energy_bfs(
                lns_solver.current_solution,
                **config.params,
            )

        if config.method == "variable_energy_pfs":
            return qubo_neighborhood.energy_pfs(
                lns_solver.current_solution,
                **config.params,
            )

        # --------------------------------------------------------
        # TSP neighborhoods
        # --------------------------------------------------------

        from tsp.neighborhood import (
            random_removal,
            segment_removal,
            related_removal,
            worst_removal,
            exchange_impact_removal,
            toggle_neighborhood,
            relocate_neighborhood,
            swap_neighborhood,
        )

        if config.method == "random_removal":
            return random_removal(
                lns_solver.current_solution,
                **config.params,
            )

        if config.method == "segment_removal":
            return segment_removal(
                lns_solver.current_solution,
                **config.params,
            )

        if config.method == "related_removal":
            return related_removal(
                tsp,
                lns_solver.current_solution,
                **config.params,
            )

        if config.method == "worst_removal":
            return worst_removal(
                tsp,
                lns_solver.current_solution,
                **config.params,
            )

        if config.method == "exchange_impact_removal":
            return exchange_impact_removal(
                tsp,
                lns_solver.current_solution,
                **config.params,
            )

        if config.method == "toggle":
            return toggle_neighborhood(
                qubo,
                lns_solver.current_solution,
                **config.params,
            )

        if config.method == "relocate":
            return relocate_neighborhood(
                qubo,
                lns_solver.current_solution,
                **config.params,
            )

        if config.method == "swap":
            return swap_neighborhood(
                qubo,
                lns_solver.current_solution,
                **config.params,
            )

        raise ValueError(
            f"Unknown neighborhood method: {config.method}"
        )

    lns_solver.set_neighborhood_selector(
        neighborhood_selector
    )

    # ============================================================
    # Subproblem solver
    # ============================================================

    lns_solver.set_sub_solver(
        sub_solver
    )

    # ============================================================
    # Candidate acceptance
    # ============================================================

    def accept_candidate(candidate):

        return (
            qubo.evaluate(candidate)
            < lns_solver.current_energy
        )

    lns_solver.set_candidate_selection(
        accept_candidate
    )

    # ============================================================
    # Lagrangian LNS loop
    # ============================================================

    qubo_costs = []

    lambda_norm = np.linalg.norm(
        np.concatenate([
            lagrangian.lambda_city,
            lagrangian.lambda_time,
        ])
    )
    print(lambda_norm)
    for iteration in range(iterations):

        # --------------------------------------------------------
        # Solve current QUBO with LNS
        # --------------------------------------------------------

        lns_solver.next_iteration()

        solution = lns_solver.current_solution

        qubo_costs.append(
            lns_solver.current_energy
        )

        # --------------------------------------------------------
        # Update Lagrange multipliers
        # --------------------------------------------------------

        lagrangian.update_lambdas(
            solution
        )

        # --------------------------------------------------------
        # Rebuild QUBO using new multipliers
        # --------------------------------------------------------

        qubo = qubo_adapter.to_qubo()

        qubo_neighborhood = Neihborhood(
            qubo
        )

        # --------------------------------------------------------
        # Update LNS to use the new QUBO
        # --------------------------------------------------------

        lns_solver.set_qubo(qubo)

        lambda_norm = np.linalg.norm(
            np.concatenate([
                lagrangian.lambda_city,
                lagrangian.lambda_time,
            ])
        )
        print(f"norm: {lambda_norm} | ref cost: {qubo_ref.evaluate(lns_solver.current_solution)}")

    # ============================================================
    # Final solution
    # ============================================================

    solution = lns_solver.current_solution

    feasible = formulation.is_feasible(
        solution
    )

    if feasible:
        final_tour = formulation.decode_tour(
            solution
        )
    else:
        final_tour = []

    return LNSResult(
        tour=final_tour,
        qubo_costs=qubo_costs,
        feasible=feasible,
        iterations=iterations,
    )