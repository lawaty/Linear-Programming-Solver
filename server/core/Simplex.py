from core.interfaces import ISolver
from core.Solver import Solver

class Simplex(Solver, ISolver):
    def __init__(self, objective, constraints, rhs, num_variables):
        super().__init__(objective, constraints, rhs, num_variables)
        self.history = [] 
        self._store_tableau() 

    def _store_tableau(self):
        self.history.append(self.tableau.copy().tolist())

    def solve(self):
        """Implements the simplex algorithm using the base Solver utilities."""
        while not self._is_optimal():
            pivot_col = self._get_pivot_column()
            pivot_row = self._get_pivot_row(pivot_col)
            self._apply_gauss(pivot_row, pivot_col)
            self._store_tableau()  # Store tableau after each iteration

        solution, optimal_value = self._extract_solution()
        return {"solution": solution.tolist(), "optimal_value": optimal_value, "history": self.history}