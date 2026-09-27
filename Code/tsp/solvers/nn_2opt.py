from tsp.problem import TSP

def nn_2opt(tsp: TSP) -> list[int]:
    tour = nearest_neighbor(tsp)
    return two_opt(tsp, tour)


def nearest_neighbor(tsp: TSP) -> list[int]:
    n = tsp.n

    if n == 0:
        return []

    tour = [0]
    unvisited = set(range(1, n))

    while unvisited:
        current = tour[-1]

        next_city = min(
            unvisited,
            key=lambda city: tsp.get_distance(current, city)
        )

        tour.append(next_city)
        unvisited.remove(next_city)

    return tour


def two_opt(tsp: TSP, tour: list[int]) -> list[int]:
    n = len(tour)

    if n < 4:
        return tour

    while True:
        improved = False

        for i in range(1, n - 1):
            for j in range(i + 1, n):
                a = tour[i - 1]
                b = tour[i]

                c = tour[j - 1]
                d = tour[j] if j < n else tour[0]

                old_cost = (
                    tsp.get_distance(a, b)
                    + tsp.get_distance(c, d)
                )

                new_cost = (
                    tsp.get_distance(a, c)
                    + tsp.get_distance(b, d)
                )

                if new_cost < old_cost:
                    tour[i:j] = reversed(tour[i:j])
                    improved = True
                    break

            if improved:
                break

        if not improved:
            break

    return tour