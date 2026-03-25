from pymc_marketing.mmm.budget_optimizer import BudgetOptimizer


def run_optimization(mmm, total_budget, bounds=None):
    optimizer = BudgetOptimizer(mmm)

    result = optimizer.optimize(
        total_budget=total_budget,
        bounds=bounds
    )

    return result