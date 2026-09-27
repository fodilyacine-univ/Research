from tsp.problem import TSP

def gurobi(tsp: TSP) -> list[int]:
    import gurobipy as gp
    from gurobipy import GRB

    model = gp.Model("TSP")
    model.setParam("OutputFlag", 0)

    x = {
        (i, j): model.addVar(
            vtype=GRB.BINARY,
            name=f"x_{i}_{j}"
        )
        for i in range(tsp.n)
        for j in range(tsp.n)
        if i != j
    }

    # One outgoing edge per city
    for i in range(tsp.n):
        model.addConstr(
            gp.quicksum(
                x[i, j]
                for j in range(tsp.n)
                if i != j
            ) == 1
        )

    # One incoming edge per city
    for j in range(tsp.n):
        model.addConstr(
            gp.quicksum(
                x[i, j]
                for i in range(tsp.n)
                if i != j
            ) == 1
        )

    model.setObjective(
        gp.quicksum(
            tsp.get_distance(i, j) * x[i, j]
            for i, j in x
        ),
        GRB.MINIMIZE
    )

    # Enable lazy subtour elimination
    model.Params.LazyConstraints = 1

    def callback(model, where):
        if where != GRB.Callback.MIPSOL:
            return

        values = model.cbGetSolution(x)

        successor = {
            i: j
            for (i, j), value in values.items()
            if value > 0.5
        }

        visited = set()

        for start in range(tsp.n):
            if start in visited:
                continue

            tour = []
            current = start

            while current not in visited:
                visited.add(current)
                tour.append(current)
                current = successor[current]

            if len(tour) < tsp.n:
                model.cbLazy(
                    gp.quicksum(
                        x[i, j]
                        for i in tour
                        for j in tour
                        if i != j
                    ) <= len(tour) - 1
                )

    model.optimize(callback)

    if model.Status != GRB.OPTIMAL:
        raise RuntimeError("Gurobi did not find an optimal solution.")

    successor = {
        i: j
        for (i, j), var in x.items()
        if var.X > 0.5
    }

    tour = [0]
    current = 0

    while True:
        current = successor[current]

        if current == 0:
            break

        tour.append(current)

    return tour
