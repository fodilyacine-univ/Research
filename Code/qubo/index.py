import dimod
import numpy as np

class QUBO:
    variables: list[str]
    linear: dict[str, float]
    quadratic: dict[tuple[str, str], float]
    offset: float

    def __init__(
        self,
        variables: list[str],
        linear: np.ndarray | None = None,
        quadratic: np.ndarray | None = None,
        offset: float = 0.0,
    ):
        self.variables = variables.copy()
        self.index = {
            variable: i
            for i, variable in enumerate(self.variables)
        }

        n = len(self.variables)

        if linear is None:
            self.linear = np.zeros(n, dtype=float)
        else:
            if linear.shape != (n,):
                raise ValueError(
                    f"linear must have shape ({n},), "
                    f"got {linear.shape}"
                )
            self.linear = linear.copy()

        if quadratic is None:
            self.quadratic = np.zeros((n, n), dtype=float)
        else:
            if quadratic.shape != (n, n):
                raise ValueError(
                    f"quadratic must have shape ({n}, {n}), "
                    f"got {quadratic.shape}"
                )
            self.quadratic = quadratic.copy()

        self.offset = float(offset)

    def add_linear(self, x: str, value: float):
        self.linear[self.index[x]] += value

    def add_quadratic(self, x: str, y: str, value: float):
        i = self.index[x]
        j = self.index[y]

        self.quadratic[i, j] += value / 2
        self.quadratic[j, i] += value / 2
    
    def add_offset(self, value):
        self.offset += value


    def get_linear(self, x: str) -> float:
        return self.linear[self.index[x]]

    def get_offset(self) -> float:
        return self.offset

    def get_quadratic(self, x: str, y: str) -> float:
        i = self.index[x]
        j = self.index[y]

        return self.quadratic[i, j] + self.quadratic[j, i]
    
    def evaluate_vector(self, x: np.ndarray) -> float:
        return float(
            x @ self.quadratic @ x
            + self.linear @ x
            + self.offset
        )

    def evaluate(self, solution: dict[str, int]) -> float:
        x = np.array(
            [solution[v] for v in self.variables],
            dtype=float
        )

        return self.evaluate_vector(x)
    
    def energy_impact(self, solution: dict[str, int]) -> dict[str, float]:
        """
        Energy reduction obtained by flipping each variable.

        Positive value  -> energy decreases
        Negative value  -> energy increases
        """

        x = np.array(
            [solution[var] for var in self.variables],
            dtype=float,
        )

        field = self.linear + 2.0 * (self.quadratic @ x)

        impact = (2.0 * x - 1.0) * field

        return dict(zip(self.variables, impact))

    def fix_variables(self, fixed: dict[str, int]):
        fixed_idx = np.array(
            [self.index[v] for v in fixed],
            dtype=int
        )

        free_idx = np.array(
            [i for i, v in enumerate(self.variables)
            if v not in fixed],
            dtype=int
        )

        x_fixed = np.array(
            [fixed[v] for v in fixed],
            dtype=float
        )

        Q_ff = self.quadratic[np.ix_(free_idx, free_idx)]
        Q_fc = self.quadratic[np.ix_(free_idx, fixed_idx)]

        b_f = self.linear[free_idx]
        b_c = self.linear[fixed_idx]

        new_linear = b_f + 2 * Q_fc @ x_fixed

        new_offset = (
            self.offset
            + b_c @ x_fixed
            + x_fixed @ self.quadratic[np.ix_(fixed_idx, fixed_idx)] @ x_fixed
        )

        new_variables = [
            self.variables[i]
            for i in free_idx
        ]

        return QUBO(
            variables=new_variables,
            linear=new_linear,
            quadratic=Q_ff,
            offset=new_offset
        )           
    
    def to_bqm(self) -> dimod.BinaryQuadraticModel:
        linear = {
            self.variables[i]: self.linear[i]
            for i in range(len(self.variables))
        }

        quadratic = {
            (self.variables[i], self.variables[j]):
                self.quadratic[i, j] + self.quadratic[j, i]
            for i in range(len(self.variables))
            for j in range(i + 1, len(self.variables))
            if self.quadratic[i, j] + self.quadratic[j, i] != 0
        }

        return dimod.BinaryQuadraticModel(
            linear,
            quadratic,
            self.offset,
            dimod.BINARY
        )

from abc import ABC, abstractmethod
class QUBOAdapterInterface(ABC):

    @abstractmethod
    def to_qubo(self, weights) -> QUBO:
        pass

    @abstractmethod
    def encode(self, solution) -> dict[str, int]:
        pass

    @abstractmethod
    def decode(self, solution: dict[str, int]):
        pass
