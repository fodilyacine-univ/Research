from tsp.problem import TSP
from qubo.index import QUBO, QUBOAdapterInterface
import numpy as np

class TimeIndexTSP:

    def __init__(self, tsp: TSP):
        self.tsp = tsp

    def encode_tour(self, tour: list[int]):
        solution = {f"x_{i}_{t}": 0 for i in range(len(tour)) for t in range(len(tour))}

        for t, city in enumerate(tour):
            solution[f"x_{city}_{t}"] = 1

        return solution
        
    def decode_tour(self, solution: dict[str, int]):
        n = self.tsp.n
        tour: list[int] = []
        for t in range(n):
            for i in range(n):
                if solution[f"x_{i}_{t}"] == 1:
                    tour.append(i)
                    break
        return tour

    def is_feasible(self, solution: dict[str, int]):
        n = self.tsp.n
        for t in range(n):
            if sum(solution[f"x_{i}_{t}"] for i in range(n)) != 1:
                return False
        for i in range(n):
            if sum(solution[f"x_{i}_{t}"] for t in range(n)) != 1:
                return False
        return True

class QUBOAdapter(QUBOAdapterInterface):
    def __init__(self, formulation: TimeIndexTSP):
        self.formulation = formulation

    def to_qubo(self, penalties):
        n = self.formulation.tsp.n

        variables = [
            f"x_{i}_{t}"
            for t in range(n)
            for i in range(n)
        ]

        index = {
            variable: k
            for k, variable in enumerate(variables)
        }

        N = n * n

        linear = np.zeros(N, dtype=float)
        Q = np.zeros((N, N), dtype=float)
        offset = 0.0

        def idx(i, t):
            return index[f"x_{i}_{t}"]

        # Objective
        for t in range(n):
            next_t = (t + 1) % n

            for i in range(n):
                for j in range(n):
                    Q[idx(i, t), idx(j, next_t)] += (
                        self.formulation.tsp.get_distance(i, j)
                    )

        # City-once constraints
        P = penalties["city_once"]

        for i in range(n):
            offset += P

            for t in range(n):
                linear[idx(i, t)] -= P

            for t1 in range(n):
                for t2 in range(t1 + 1, n):
                    Q[idx(i, t1), idx(i, t2)] += 2 * P

        # Time-once constraints
        P = penalties["time_once"]

        for t in range(n):
            offset += P

            for i in range(n):
                linear[idx(i, t)] -= P

            for i in range(n):
                for j in range(i + 1, n):
                    Q[idx(i, t), idx(j, t)] += 2 * P

        # Convert upper-triangular QUBO coefficients
        # into the symmetric matrix used by x.T @ Q @ x.
        Q = Q + Q.T
        np.fill_diagonal(Q, 0.0)

        Q /= 2

        return QUBO(
            variables=variables,
            linear=linear,
            quadratic=Q,
            offset=offset
        )
    
    def encode(self, solution: dict[str, int]):
        return solution.copy()
    
    def decode(self, solution: dict[str, int]):
        return solution.copy()
