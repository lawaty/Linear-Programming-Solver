from core.Solver import Solver
import numpy as np

class Simplex(Solver):
    def __init__(self, objective, constraints, rhs, num_variables):
        super().__init__(objective, constraints, rhs, num_variables)

    def _initialize_tableau(self):
        """Tableau has an extra raw for the obj. function and columns = #variables + #slack variables + 1 (RHS)
        """

        rows, cols = self.constraints.shape
        tableau = np.zeros((rows + 1, cols + rows + 1))
        
        # Constraints Rows
        tableau[:-1, :cols] = self.constraints # DV Cells
        tableau[:-1, cols:cols + rows] = np.eye(rows) # Slack Cells
        tableau[:-1, -1] = self.rhs

        # Obj. Fun in the standard form (Last Row)
        # print(tableau[-1, :cols], -self.objective)
        tableau[-1, :cols] = -self.objective  # Objective function
        return tableau

    def solve(self):
        """Implements the simplex algorithm using the base Solver utilities."""
        if not self._is_feasible(self.tableau):
            return {"feasible" : False , "solution": None, "optimal_value": None, "history": self.history}
        while not self._is_optimal():
            pivot_col = self._get_pivot_column()
            pivot_row = self._get_pivot_row(pivot_col)
            self._apply_gauss(pivot_row, pivot_col)
            self._store_tableau()  # Store tableau after each iteration

        solution, optimal_value = self._extract_solution()
        return {"feasible" : True ,"solution": solution.tolist(), "optimal_value": optimal_value, "history": self.history}

    def _is_feasible(self, tableau):
        """Checks if the initial tableau is feasible."""
        return np.all(tableau[:-1, -1] >= 0)  # All RHS values must be non-negative
if __name__ == "__main__":
    # Example problem: Maximize z = 3x + 5y
    # Subject to:
    # 2x + y <= 6
    # x + 2y <= 6

    objective = np.array([3, 5])
    constraints = np.array([
        [2, 1],
        [1, 2]
    ])
    rhs = np.array([6, 6])
    num_variables = 2

    simplex_solver = Simplex(objective, constraints, rhs, num_variables)
    result = simplex_solver.solve()

    print("Optimal Solution:", result["solution"])
    print("Optimal Value:", result["optimal_value"])
    # print("History of Tableaus:\n", result["history"])