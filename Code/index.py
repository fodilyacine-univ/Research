from tsp.solvers.lns import lns, NeighborhoodConfig
from tsp.solvers.lns_lagrangian import lns_lagrangian
from tsp.problem import TSP
from tsp.solvers.gurobi import gurobi
from qubo.solvers import gurobi as gr, tabu
import json
import math
from tsp.TimeIndex import TimeIndexTSP, QUBOAdapter

instances = []
seeds = 4
sizes = [10, 20, 30]
config = NeighborhoodConfig(
    method="random_variables",
    params={
        "size": 50
    }
)
for i, size in enumerate(sizes):
    for seed in range(seeds):
        tsp = TSP.generate(
            size,
            1000,
            1000,
            seed
        )
        result = lns(
            tsp,
            iterations=30,
            neighborhood_config=config,
            sub_solver=gr
        )
        instances.append({
            "size": size,
            "dimensions": [1000, 1000],
            "seed": seed,
            "result": {
                "qubo_costs": result.qubo_costs,
                "tour": result.tour,
                "feasible": len(result.tour) > 0,
                "route_cost": tsp.tour_cost(result.tour) if len(result.tour) > 0 else None
            }
        })
        print(f"size: {size} | seed: {seed}")

with open("results/random_variables.json", "w") as f:
    json.dump({
        "neighborhood_selection": {
            "method": "random_variables",
            "params": {
                "size": 50
            }
        },
        "sub_solver": "gurobi",
        "instances": instances
    }, f, indent=4)

# best_solution = gurobi(tsp)
# best_cost = tsp.tour_cost(best_solution)

# formulation = TimeIndexTSP(tsp)
# qubo_adapter = QUBOAdapter(formulation)
# max_distance = max(
#     tsp.get_distance(i, j)
#     for i in range(tsp.n)
#     for j in range(tsp.n)
# )

# qubo = qubo_adapter.to_qubo({
#     "city_once": max_distance,
#     "time_once": max_distance,
# })
# config = NeighborhoodConfig(
#     method="swap_neighborhood",
#     params={"min_variables": 50}
# )
# best_solution = tabu(qubo)
# best_cost = qubo.evaluate(best_solution)

# initial_solution = {f"x_{i}_{t}": 1 if i == t else 0 for i in range(tsp.n) for t in range(tsp.n)}

result = lns(
    tsp,
    iterations=50,
    neighborhood_config=config,
    sub_solver=gr
)
# cost_gap = [math.ceil((cost - best_cost)/abs(best_cost)*100) for cost in result.qubo_costs]
# print(cost_gap)


# results = lns_lagrangian(
#     tsp,
#     iterations= 150,
#     neighborhood_config=NeighborhoodConfig(
#         method="toggle",
#         params={"min_variables": 50}
#     )
# )