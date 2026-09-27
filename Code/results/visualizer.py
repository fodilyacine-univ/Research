import json
import numpy as np
import matplotlib.pyplot as plt


def compare_algorithm_to_baseline(
    algorithm_file,
    baseline_file="results/gurobi.json",
):
    """
    Compare an algorithm against a Gurobi baseline.

    For every problem size found in the algorithm file:
        - Match instances using (size, seed)
        - Use the best-so-far QUBO cost
        - Compute the relative optimality gap:
              (qubo_cost - gurobi_cost) / abs(gurobi_cost)
        - Average over the seeds that actually exist
        - Produce one plot for each problem size

    The number of seeds does NOT need to be fixed.
    """

    # =========================================================
    # Load files
    # =========================================================

    with open(baseline_file, "r") as f:
        baseline_data = json.load(f)

    with open(algorithm_file, "r") as f:
        algorithm_data = json.load(f)

    # =========================================================
    # Index Gurobi results
    # =========================================================

    gurobi = {}

    for instance in baseline_data:
        size = instance["size"]
        seed = instance["seed"]

        gurobi[(size, seed)] = instance["result"]["tour_cost"]

    # =========================================================
    # Group algorithm instances by size
    # =========================================================

    results = {}

    for instance in algorithm_data["instances"]:

        size = instance["size"]
        seed = instance["seed"]

        key = (size, seed)

        # Ignore instances for which we don't have a baseline
        if key not in gurobi:
            print(
                f"Warning: no Gurobi result for "
                f"size={size}, seed={seed}"
            )
            continue

        gurobi_cost = gurobi[key]

        qubo_costs = np.asarray(
            instance["result"]["qubo_costs"],
            dtype=float
        )

        # -----------------------------------------------------
        # Best solution found so far
        # -----------------------------------------------------

        best_qubo_costs = np.minimum.accumulate(qubo_costs)

        # -----------------------------------------------------
        # Positive optimality gap
        # -----------------------------------------------------

        gaps = (
            best_qubo_costs - gurobi_cost
        ) / abs(gurobi_cost)

        # Numerical precision can occasionally produce
        # something like -1e-16 instead of 0.
        gaps = np.maximum(gaps, 0.0)

        results.setdefault(size, {})[seed] = gaps

    # =========================================================
    # Plot one figure per size
    # =========================================================

    for size in sorted(results):

        seed_results = results[size]

        # Seeds actually present
        seeds = sorted(seed_results.keys())

        if not seeds:
            continue

        print(
            f"Size {size}: "
            f"{len(seeds)} seeds -> {seeds}"
        )

        # -----------------------------------------------------
        # Make trajectories the same length
        # -----------------------------------------------------

        max_iterations = max(
            len(seed_results[seed])
            for seed in seeds
        )

        trajectories = []

        for seed in seeds:

            gaps = seed_results[seed]

            if len(gaps) < max_iterations:
                gaps = np.pad(
                    gaps,
                    (0, max_iterations - len(gaps)),
                    mode="edge"
                )

            trajectories.append(gaps)

        trajectories = np.asarray(trajectories)

        # -----------------------------------------------------
        # Average over available seeds
        # -----------------------------------------------------

        mean_gap = np.mean(
            trajectories,
            axis=0
        )

        # =====================================================
        # Plot
        # =====================================================

        iterations = np.arange(
            1,
            max_iterations + 1
        )

        plt.figure(figsize=(9, 5))

        plt.plot(
            iterations,
            mean_gap,
            linewidth=2,
        )

        plt.axhline(
            0,
            linestyle="--",
            linewidth=1,
        )

        plt.xlabel("Iteration")
        plt.ylabel("Optimality Gap")

        plt.title(
            f"Average Optimality Gap — TSP size {size}"
        )

        plt.grid(
            True,
            alpha=0.3
        )

        plt.tight_layout()
        plt.show()

    return results