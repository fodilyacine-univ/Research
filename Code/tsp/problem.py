import math, random

class TSP:

    def __init__(self, distance_matrix: list[list[float, float]]) -> None:
        self.n = len(distance_matrix)
        self.distance_matrix = distance_matrix

    @staticmethod
    def generate(
            n: int,
            max_w: float,
            max_h: float | None = None,
            seed: int | None = None
        ) -> "TSP":
            if max_h is None:
                max_h = max_w

            rng = random.Random(seed)

            coordinates = [
                (
                    rng.uniform(0, max_w),
                    rng.uniform(0, max_h)
                )
                for _ in range(n)
            ]

            return TSP.from_coordinates(coordinates)

    @staticmethod
    def from_coordinates(coordinates: list[tuple[float, float]]):
        n = len(coordinates)
        distance_matrix = [
            [0.0 for _ in range(n)]
            for _ in range(n)
        ]

        for i, a in enumerate(coordinates):
            for j in range(i + 1, n):
                b = coordinates[j]
                dist = math.dist(a, b)

                distance_matrix[i][j] = dist
                distance_matrix[j][i] = dist
        
        return TSP(distance_matrix)

    def get_distance(self, i: int, j: int) -> float:
        return self.distance_matrix[i][j]

    def tour_cost(self, tour: list[int]) -> float:
        s: float = 0
        for i in range(self.n):
            s += self.distance_matrix[tour[i]][tour[(i + 1) % self.n]]
        return s

class TSPVisualizer:
    def __init__(self, tsp: TSP):
        self.tsp = tsp

    def visualize_map(self):
        import matplotlib.pyplot as plt

        x = [coord[0] for coord in self.tsp.coordinates]
        y = [coord[1] for coord in self.tsp.coordinates]

        plt.figure(figsize=(8, 8))
        plt.scatter(x, y)

        for i, (xi, yi) in enumerate(self.tsp.coordinates):
            plt.annotate(
                str(i),
                (xi, yi),
                xytext=(5, 5),
                textcoords="offset points"
            )

        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title(f"TSP — {self.tsp.n} cities")
        plt.grid(True)
        plt.show()

    def visualize_solution(self, tour: list[int]):
        import matplotlib.pyplot as plt

        x = [coord[0] for coord in self.tsp.coordinates]
        y = [coord[1] for coord in self.tsp.coordinates]

        plt.figure(figsize=(10, 10))
        plt.scatter(x, y)

        # City labels
        for i, (xi, yi) in enumerate(self.tsp.coordinates):
            plt.annotate(
                str(i),
                (xi, yi),
                xytext=(5, 5),
                textcoords="offset points"
            )

        total_distance = 0.0

        # Tour edges
        for i in range(len(tour)):
            current = tour[i]
            next_city = tour[(i + 1) % len(tour)]

            x1, y1 = self.tsp.coordinates[current]
            x2, y2 = self.tsp.coordinates[next_city]

            distance = self.tsp.get_distance(current, next_city)
            total_distance += distance

            plt.plot([x1, x2], [y1, y2])

            # Distance label
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2

            plt.annotate(
                f"{distance:.2f}",
                (mid_x, mid_y),
                xytext=(0, 5),
                textcoords="offset points",
                ha="center"
            )

        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title(
            f"TSP Solution — Total distance: {total_distance:.2f}"
        )
        plt.grid(True)
        plt.show()
