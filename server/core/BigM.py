from core.interfaces import ISolver
from core.Solver import Solver
import numpy as np

class BigM(Solver, ISolver):
    def __init__(self, objective, constraints, rhs, num_variables):
        super().__init__(objective, constraints, rhs, num_variables)
        self.M = 1e6  # Large M value

    def _initialize_tableau(self):
        rows, cols = self.constraints.shape
        num_artificial = sum(1 for r in self.rhs if r < 0)  # Counting artificial variables
        tableau = np.zeros((rows + 1, cols + rows + num_artificial + 1))
        
        # Constraints Rows
        tableau[:-1, :cols] = self.constraints  # Decision variables
        tableau[:-1, cols:cols + rows] = np.eye(rows)  # Slack variables
        tableau[:-1, -1] = self.rhs  # RHS column
        
        # Identify artificial variables and modify constraints accordingly
        artificial_idx = cols + rows
        artificial_vars = []
        for i, rhs_value in enumerate(self.rhs):
            if rhs_value < 0:
                tableau[i, :cols] *= -1  # Convert inequality sign
                tableau[i, cols:cols + rows] *= -1
                tableau[i, artificial_idx] = 1  # Artificial variable
                artificial_vars.append(artificial_idx)
                artificial_idx += 1
        
        # Objective function row
        tableau[-1, :cols] = -self.objective  # Standard objective
        for idx in artificial_vars:
            tableau[-1, :] += self.M * tableau[:, idx]  # Penalize artificial variables
        
        return tableau
    
    def solve(self):
        """Implements the Big-M method using the base Solver utilities."""
        while not self._is_optimal():
            pivot_col = self._get_pivot_column()
            pivot_row = self._get_pivot_row(pivot_col)
            self._apply_gauss(pivot_row, pivot_col)
            self._store_tableau()
        
        solution, optimal_value = self._extract_solution()
        return {"solution": solution.tolist(), "optimal_value": optimal_value, "history": self.history}
