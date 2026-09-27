import random
import numpy as np
from qubo.index import QUBO
from tsp.TimeIndex import TimeIndexTSP, QUBOAdapter
from tsp.problem import TSP

def random_removal(solution: dict[str, int], k: int):
    # Extract (city, position) from variables currently set to 1
    tour = [
        (int(var.split("_")[1]), int(var.split("_")[2]))
        for var, value in solution.items()
        if value == 1
    ]

    # Randomly select n positions
    positions = random.sample(
        [t for _, t in tour],
        k
    )

    # Cities currently occupying those positions
    cities = {
        city
        for city, position in tour
        if position in positions
    }

    # Return every city-position variable for the selected
    # cities and selected positions
    return [
        f"x_{city}_{position}"
        for city in cities
        for position in positions
    ]

def segment_removal(solution: dict[str, int], k: int):
    # Extract (city, position) from variables currently set to 1
    tour = [
        (int(var.split("_")[1]), int(var.split("_")[2]))
        for var, value in solution.items()
        if value == 1
    ]

    n = len(tour)

    # Randomly select the start of the segment
    start = random.randrange(n)

    # Select k consecutive positions (cyclically)
    positions = [
        (start + i) % n
        for i in range(k)
    ]

    # Cities currently occupying those positions
    cities = {
        city
        for city, position in tour
        if position in positions
    }

    # Return every city-position variable for the selected
    # cities and selected positions
    return [
        f"x_{city}_{position}"
        for city in cities
        for position in positions
    ]

def related_removal(
    tsp: TSP,
    solution: dict[str, int],
    k: int
) -> list[str]:

    city_count = int(len(solution) ** 0.5)

    tour = sorted(
        (
            (int(var.split("_")[1]), int(var.split("_")[2]))
            for var, value in solution.items()
            if value == 1
        ),
        key=lambda x: x[1]
    )

    # (city, position)
    tour = [city for city, _ in tour]

    # Select a random seed city
    seed = np.random.choice(city_count)

    # Cities geographically related to the seed
    distances = np.array(tsp.distance_matrix[seed], dtype=float)
    distances[seed] = np.inf

    weights = 1.0 / distances
    weights /= weights.sum()

    related_cities = np.random.choice(
        city_count,
        size=k - 1,
        replace=False,
        p=weights
    )

    cities = [seed, *related_cities]

    # Positions currently occupied by the selected cities
    positions = [
        tour.index(city)
        for city in cities
    ]

    # k selected cities × k selected positions
    return [
        f"x_{city}_{position}"
        for city in cities
        for position in positions
    ]

def worst_removal(
    tsp: TSP,
    solution: dict[str, int],
    k: int
) -> list[str]:

    city_count = int(len(solution) ** 0.5)

    tour = sorted(
        (
            (int(var.split("_")[1]), int(var.split("_")[2]))
            for var, value in solution.items()
            if value == 1
        ),
        key=lambda x: x[1]
    )

    tour = [city for city, _ in tour]

    # Removal contribution of each city
    contributions = np.zeros(city_count)

    for pos, city in enumerate(tour):
        prev_city = tour[pos - 1]
        next_city = tour[(pos + 1) % city_count]

        contributions[city] = (
            tsp.distance_matrix[prev_city][city]
            + tsp.distance_matrix[city][next_city]
            - tsp.distance_matrix[prev_city][next_city]
        )

    # Prefer cities with large removal contributions
    epsilon = 0.01
    weights = np.maximum(contributions, 0.0) + epsilon
    weights /= weights.sum()

    cities = np.random.choice(
        city_count,
        size=k,
        replace=False,
        p=weights
    )

    # Positions currently occupied by selected cities
    positions = [
        tour.index(city)
        for city in cities
    ]

    # k cities × k positions = k² variables
    return [
        f"x_{city}_{position}"
        for city in cities
        for position in positions
    ]

def exchange_impact_removal(
    tsp: TSP,
    solution: dict[str, int],
    pair_count: int
) -> list[str]:

    n = int(len(solution) ** 0.5)

    # city at each position
    tour = [0] * n
    for var, value in solution.items():
        if value == 1:
            _, city, position = var.split("_")
            tour[int(position)] = int(city)

    dist = tsp.distance_matrix

    # Current position of every city
    position = [0] * n
    for pos, city in enumerate(tour):
        position[city] = pos

    def swap_delta(i: int, j: int) -> float:
        """New cost - current cost after swapping positions i and j."""

        pi = (i - 1) % n
        ni = (i + 1) % n
        pj = (j - 1) % n
        nj = (j + 1) % n

        a = tour[i]
        b = tour[j]

        # Adjacent positions
        if ni == j:
            return (
                dist[b][a]
                + dist[a][tour[nj]]
                + dist[tour[pi]][b]
                - dist[a][b]
                - dist[b][tour[nj]]
                - dist[tour[pi]][a]
            )

        if nj == i:
            return (
                dist[a][b]
                + dist[b][tour[ni]]
                + dist[tour[pj]][a]
                - dist[b][a]
                - dist[a][tour[ni]]
                - dist[tour[pj]][b]
            )

        old = (
            dist[tour[pi]][a]
            + dist[a][tour[ni]]
            + dist[tour[pj]][b]
            + dist[b][tour[nj]]
        )

        new = (
            dist[tour[pi]][b]
            + dist[b][tour[ni]]
            + dist[tour[pj]][a]
            + dist[a][tour[nj]]
        )

        return new - old

    # (improvement, city_a, city_b)
    exchanges = []

    for i in range(n):
        for j in range(i + 1, n):

            delta = swap_delta(i, j)

            exchanges.append(
                (-delta, tour[i], tour[j])
            )

    # Better exchanges get higher probability
    improvements = np.array(
        [improvement for improvement, _, _ in exchanges],
        dtype=float
    )

    epsilon = 0.01
    weights = np.maximum(improvements, 0.0) + epsilon
    weights /= weights.sum()

    selected_indices = np.random.choice(
        len(exchanges),
        size=min(pair_count, len(exchanges)),
        replace=False,
        p=weights
    )

    selected = [
        exchanges[i]
        for i in selected_indices
    ]

    # Cities participating in selected exchanges
    cities = {
        city
        for _, city_a, city_b in selected
        for city in (city_a, city_b)
    }

    # Their current positions
    positions = [
        position[city]
        for city in cities
    ]

    # m cities × m positions
    return [
        f"x_{city}_{pos}"
        for city in cities
        for pos in positions
    ]

## expansion mechanisms can be further explored
def toggle_neighborhood(
    qubo: QUBO,
    solution: dict[str, int],
    min_variables: int,
) -> list[str]:
    """
    Select a neighborhood of single-variable toggle moves.

    Variables with positive energy impact are sampled proportionally
    to their impact. If there are not enough positive-impact variables,
    the remaining variables are sampled uniformly.

    The selected variables directly form the neighborhood.
    """

    impacts = qubo.energy_impact(solution)

    variables = np.array(list(impacts.keys()))
    impact_values = np.fromiter(
        impacts.values(),
        dtype=float,
    )

    n = min(min_variables, len(variables))

    positive = np.flatnonzero(impact_values > 0)
    non_positive = np.flatnonzero(impact_values <= 0)

    # Select as many improving moves as possible.
    positive_count = min(n, len(positive))

    if positive_count > 0:
        weights = impact_values[positive]
        weights /= weights.sum()

        selected_positive = np.random.choice(
            positive,
            size=positive_count,
            replace=False,
            p=weights,
        )
    else:
        selected_positive = np.empty(0, dtype=int)

    # Fill remaining neighborhood uniformly.
    remaining_count = n - positive_count

    if remaining_count > 0:
        selected_non_positive = np.random.choice(
            non_positive,
            size=remaining_count,
            replace=False,
        )
    else:
        selected_non_positive = np.empty(0, dtype=int)

    selected = np.concatenate([
        selected_positive,
        selected_non_positive,
    ])

    return variables[selected].tolist()

import numpy as np

def relocate_neighborhood(
    qubo: QUBO,
    solution: dict[str, int],
    min_variables: int,
) -> list[str]:

    city_positions = {}

    for variable, value in solution.items():
        if not variable.startswith("x_"):
            continue

        _, city, position = variable.split("_")
        city = int(city)
        position = int(position)

        city_positions.setdefault(city, {})[position] = value

    x = np.array(
        [solution[v] for v in qubo.variables],
        dtype=float,
    )

    field = qubo.linear + 2.0 * (qubo.quadratic @ x)
    index = qubo.index

    moves = []
    impacts = []

    for city, positions in city_positions.items():

        active = [
            p for p, value in positions.items()
            if value == 1
        ]

        inactive = [
            p for p, value in positions.items()
            if value == 0
        ]

        for source in active:
            for target in inactive:

                source_var = f"x_{city}_{source}"
                target_var = f"x_{city}_{target}"

                i = index[source_var]
                j = index[target_var]

                delta = (
                    -field[i]
                    + field[j]
                    - 2.0 * qubo.quadratic[i, j]
                )

                moves.append((city, source, target))
                impacts.append(-delta)

    if not moves:
        return []

    # Highest-impact moves first
    order = np.argsort(impacts)[::-1]

    selected_cities = set()
    selected_positions = set()

    for move_index in order:

        city, source, target = moves[move_index]

        new_cities = selected_cities | {city}
        new_positions = selected_positions | {source, target}

        new_size = len(new_cities) * len(new_positions)

        selected_cities = new_cities
        selected_positions = new_positions

        if new_size >= min_variables:
            break

    return [
        f"x_{city}_{position}"
        for city in selected_cities
        for position in selected_positions
    ]

def swap_neighborhood(
    qubo: QUBO,
    solution: dict[str, int],
    min_variables: int,
) -> list[str]:

    city_positions = {}

    for variable, value in solution.items():
        if not variable.startswith("x_"):
            continue

        _, city, position = variable.split("_")
        city = int(city)
        position = int(position)

        city_positions.setdefault(city, {})[position] = value

    cities = list(city_positions)

    x = np.array(
        [solution[v] for v in qubo.variables],
        dtype=float,
    )

    field = qubo.linear + 2.0 * (qubo.quadratic @ x)
    Q = qubo.quadratic
    index = qubo.index

    moves = []
    impacts = []

    for a_idx in range(len(cities)):
        city_a = cities[a_idx]

        for b_idx in range(a_idx + 1, len(cities)):
            city_b = cities[b_idx]

            for p1, value_a in city_positions[city_a].items():

                if value_a != 1:
                    continue

                for p2, value_b in city_positions[city_b].items():

                    if value_b != 1:
                        continue

                    if city_positions[city_a].get(p2, 0) != 0:
                        continue

                    if city_positions[city_b].get(p1, 0) != 0:
                        continue

                    variables = [
                        f"x_{city_a}_{p1}",
                        f"x_{city_a}_{p2}",
                        f"x_{city_b}_{p1}",
                        f"x_{city_b}_{p2}",
                    ]

                    indices = [index[v] for v in variables]
                    d = np.array([-1., +1., +1., -1.])

                    delta = (
                        np.dot(field[indices], d)
                        + d @ Q[np.ix_(indices, indices)] @ d
                    )

                    moves.append(
                        (city_a, city_b, p1, p2)
                    )
                    impacts.append(-delta)

    if not moves:
        return []

    # Highest-impact swaps first
    order = np.argsort(impacts)[::-1]

    selected_cities = set()
    selected_positions = set()

    for move_index in order:

        city_a, city_b, p1, p2 = moves[move_index]

        new_cities = selected_cities | {
            city_a,
            city_b,
        }

        new_positions = selected_positions | {
            p1,
            p2,
        }

        new_size = len(new_cities) * len(new_positions)

        selected_cities = new_cities
        selected_positions = new_positions

        if new_size >= min_variables:
            break

    return [
        f"x_{city}_{position}"
        for city in selected_cities
        for position in selected_positions
    ]