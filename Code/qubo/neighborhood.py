from qubo.index import QUBO
from hybrid import State
from hybrid.decomposers import (
    EnergyImpactDecomposer,
    RandomSubproblemDecomposer,
)

class Neihborhood:

    def __init__(self, qubo: QUBO):
        self.qubo = qubo
        self.bqm = self.qubo.to_bqm()

    def _dwave(
        self,
        solution: dict[str, int],
        size: int,
        traversal: str,
    ) -> list[str]:

        if size <= 0:
            return []

        if size >= len(self.qubo.variables):
            return self.qubo.variables.copy()

        state = State.from_sample(solution, self.bqm)

        decomposer = EnergyImpactDecomposer(
            size=size,
            rolling=False,
            traversal=traversal,
        )

        state = decomposer.run(state).result()

        return list(state.subproblem.variables)

    def energy(
        self,
        solution: dict[str, int],
        size: int,
    ) -> list[str]:

        return self._dwave(
            solution,
            size,
            traversal="energy",
        )

    def energy_bfs(
        self,
        solution: dict[str, int],
        size: int,
    ) -> list[str]:

        return self._dwave(
            solution,
            size,
            traversal="bfs",
        )

    def energy_pfs(
        self,
        solution: dict[str, int],
        size: int,
    ) -> list[str]:

        return self._dwave(
            solution,
            size,
            traversal="pfs",
        )

    def random_variables(
        self,
        solution: dict[str, int],
        size: int,
    ) -> list[str]:

        if size <= 0:
            return []

        if size >= len(self.qubo.variables):
            return self.qubo.variables.copy()

        state = State.from_sample(solution, self.bqm)

        decomposer = RandomSubproblemDecomposer(
            size=size
        )

        state = decomposer.run(state).result()

        return list(state.subproblem.variables)
