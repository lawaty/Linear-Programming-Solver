from core.interfaces import SimplexSolver
from core.Solver import Solver

class Simplex(Solver, SimplexSolver):
    def solve(self, data):
        """Implements the simplex algorithm using the base Solver utilities."""
        while not self._is_optimal():
            pivot_col = self._get_pivot_column()
            pivot_row = self._get_pivot_row(pivot_col)
            self._perform_pivot(pivot_row, pivot_col)
        
        solution, optimal_value = self._extract_solution()
        return {"solution": solution.tolist(), "optimal_value": optimal_value}
