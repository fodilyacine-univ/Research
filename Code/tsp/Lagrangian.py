import numpy as np

from qubo.index import QUBO, QUBOAdapterInterface
from tsp.TimeIndex import TimeIndexTSP


class TimeIndexAugmentedLagrangian:

    def __init__(self, formulation: TimeIndexTSP):
        self.formulation = formulation

        n = formulation.tsp.n

        # Lagrange multipliers
        self.lambda_city = np.zeros(n, dtype=float)
        self.lambda_time = np.zeros(n, dtype=float)

        # Quadratic penalty coefficients
        self.rho_city = np.ones(n, dtype=float)
        self.rho_time = np.ones(n, dtype=float)

    # ------------------------------------------------------------
    # Encoding / decoding
    # ------------------------------------------------------------

    def encode(self, solution: dict[str, int]):
        return solution.copy()

    def decode(self, solution: dict[str, int]):
        return solution.copy()

    # ------------------------------------------------------------
    # Constraint evaluation
    # ------------------------------------------------------------

    def evaluate_city_constraints(
        self,
        solution: dict[str, int],
    ) -> np.ndarray:
        """
        City constraint:

            sum_t x[i,t] = 1

        Returns:

            g_city[i] = sum_t x[i,t] - 1
        """

        n = self.formulation.tsp.n

        return np.array(
            [
                sum(
                    solution[f"x_{i}_{t}"]
                    for t in range(n)
                ) - 1
                for i in range(n)
            ],
            dtype=float,
        )

    def evaluate_time_constraints(
        self,
        solution: dict[str, int],
    ) -> np.ndarray:
        """
        Time/position constraint:

            sum_i x[i,t] = 1

        Returns:

            g_time[t] = sum_i x[i,t] - 1
        """

        n = self.formulation.tsp.n

        return np.array(
            [
                sum(
                    solution[f"x_{i}_{t}"]
                    for i in range(n)
                ) - 1
                for t in range(n)
            ],
            dtype=float,
        )

    # ------------------------------------------------------------
    # Multiplier updates
    # ------------------------------------------------------------

    def update_city_lambdas(
        self,
        solution: dict[str, int],
        indices: list[int] | None = None,
    ):
        """
        Augmented-Lagrangian multiplier update:

            lambda_i <- lambda_i + rho_i * g_i(x)

        If indices is provided, only those city constraints
        are updated.
        """

        violations = self.evaluate_city_constraints(solution)

        if indices is None:
            self.lambda_city += (
                self.rho_city * violations
            )
        else:
            indices = np.asarray(indices, dtype=int)

            self.lambda_city[indices] += (
                self.rho_city[indices]
                * violations[indices]
            )

    def update_time_lambdas(
        self,
        solution: dict[str, int],
        indices: list[int] | None = None,
    ):
        """
        Augmented-Lagrangian multiplier update:

            lambda_t <- lambda_t + rho_t * g_t(x)

        If indices is provided, only those time/position
        constraints are updated.
        """

        violations = self.evaluate_time_constraints(solution)

        if indices is None:
            self.lambda_time += (
                self.rho_time * violations
            )
        else:
            indices = np.asarray(indices, dtype=int)

            self.lambda_time[indices] += (
                self.rho_time[indices]
                * violations[indices]
            )

    def update_lambdas(
        self,
        solution: dict[str, int],
    ):
        """
        Update all Lagrange multipliers.
        """

        self.update_city_lambdas(solution)
        self.update_time_lambdas(solution)

    # ------------------------------------------------------------
    # Penalty coefficients
    # ------------------------------------------------------------

    def set_rho_city(
        self,
        rho_values: dict[int, float],
    ):
        for i, value in rho_values.items():
            self.rho_city[i] = value

    def set_rho_time(
        self,
        rho_values: dict[int, float],
    ):
        for t, value in rho_values.items():
            self.rho_time[t] = value

    def set_rho(
        self,
        rho_city: float | None = None,
        rho_time: float | None = None,
    ):
        """
        Set all city/time penalty coefficients.
        """

        if rho_city is not None:
            self.rho_city.fill(rho_city)

        if rho_time is not None:
            self.rho_time.fill(rho_time)


class QUBOAdapter(QUBOAdapterInterface):

    def __init__(
        self,
        lagrangian: TimeIndexAugmentedLagrangian,
    ):
        self.lagrangian = lagrangian

    # ------------------------------------------------------------
    # QUBO construction
    # ------------------------------------------------------------

    def to_qubo(self) -> QUBO:

        lagrangian = self.lagrangian
        formulation = lagrangian.formulation
        tsp = formulation.tsp

        n = tsp.n

        lambda_city = lagrangian.lambda_city
        lambda_time = lagrangian.lambda_time

        rho_city = lagrangian.rho_city
        rho_time = lagrangian.rho_time

        # --------------------------------------------------------
        # Variables
        # --------------------------------------------------------

        variables = [
            f"x_{i}_{t}"
            for t in range(n)
            for i in range(n)
        ]

        qubo = QUBO(variables)

        # --------------------------------------------------------
        # TSP objective
        #
        # sum_t sum_i,j
        #     d(i,j) x[i,t] x[j,t+1]
        # --------------------------------------------------------

        for t in range(n):

            next_t = (t + 1) % n

            for i in range(n):
                for j in range(n):

                    qubo.add_quadratic(
                        f"x_{i}_{t}",
                        f"x_{j}_{next_t}",
                        tsp.get_distance(i, j),
                    )

        # --------------------------------------------------------
        # City constraints
        #
        # g_i(x) = sum_t x[i,t] - 1
        #
        # lambda_i * g_i(x)
        # + rho_i/2 * g_i(x)^2
        #
        # Expanded:
        #
        # constant:
        #     -lambda_i + rho_i/2
        #
        # linear:
        #     lambda_i - rho_i/2
        #
        # quadratic:
        #     rho_i
        # --------------------------------------------------------

        for i in range(n):

            lam = lambda_city[i]
            rho = rho_city[i]

            qubo.add_offset(
                -lam + rho / 2.0
            )

            linear_coefficient = (
                lam - rho / 2.0
            )

            for t in range(n):

                qubo.add_linear(
                    f"x_{i}_{t}",
                    linear_coefficient,
                )

            for t1 in range(n):
                for t2 in range(t1 + 1, n):

                    qubo.add_quadratic(
                        f"x_{i}_{t1}",
                        f"x_{i}_{t2}",
                        rho,
                    )

        # --------------------------------------------------------
        # Time/position constraints
        #
        # g_t(x) = sum_i x[i,t] - 1
        #
        # Expanded exactly like the city constraints.
        # --------------------------------------------------------

        for t in range(n):

            lam = lambda_time[t]
            rho = rho_time[t]

            qubo.add_offset(
                -lam + rho / 2.0
            )

            linear_coefficient = (
                lam - rho / 2.0
            )

            for i in range(n):

                qubo.add_linear(
                    f"x_{i}_{t}",
                    linear_coefficient,
                )

            for i in range(n):
                for j in range(i + 1, n):

                    qubo.add_quadratic(
                        f"x_{i}_{t}",
                        f"x_{j}_{t}",
                        rho,
                    )

        return qubo

    # ------------------------------------------------------------
    # Encoding / decoding
    # ------------------------------------------------------------

    def encode(
        self,
        solution: dict[str, int],
    ):
        return solution.copy()

    def decode(
        self,
        solution: dict[str, int],
    ):
        return solution.copy()