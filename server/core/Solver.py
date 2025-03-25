import numpy as np

class Solver:
    def __init__(self, objective, constraints, rhs, num_variables):
        self.objective = np.array(objective, dtype=float)
        self.constraints = np.array(constraints, dtype=float)
        self.rhs = np.array(rhs, dtype=float)
        self.num_variables = num_variables
        self.tableau = self._initialize_tableau()
        
    def _initialize_tableau(self):
        """Constructs the initial simplex tableau."""
        rows, cols = self.constraints.shape
        tableau = np.zeros((rows + 1, cols + rows + 1))
        
        tableau[:-1, :cols] = self.constraints  # Constraint coefficients
        tableau[:-1, cols:cols + rows] = np.eye(rows)  # Slack variables
        tableau[:-1, -1] = self.rhs  # RHS values
        tableau[-1, :cols] = -self.objective  # Objective function (negative for maximization)
        return tableau

    def _get_pivot_column(self):
        """Finds the entering variable (column with most negative coefficient in objective row)."""
        return np.argmin(self.tableau[-1, :-1])
    
    def _get_pivot_row(self, pivot_col):
        """Finds the row for the leaving variable using the minimum positive ratio test."""
        ratios = self.tableau[:-1, -1] / self.tableau[:-1, pivot_col]
        ratios[ratios <= 0] = np.inf  # Ignore negative or zero ratios
        return np.argmin(ratios)
    
    def _perform_pivot(self, pivot_row, pivot_col):
        """Performs row operations to pivot on the chosen element."""
        self.tableau[pivot_row, :] /= self.tableau[pivot_row, pivot_col]  # Normalize pivot row
        for i in range(self.tableau.shape[0]):
            if i != pivot_row:
                self.tableau[i, :] -= self.tableau[i, pivot_col] * self.tableau[pivot_row, :]

    def _is_optimal(self):
        """Checks if the solution is optimal (all coefficients in objective row >= 0)."""
        return np.all(self.tableau[-1, :-1] >= 0)
    
    def _extract_solution(self):
        """Extracts the solution from the final tableau."""
        solution = np.zeros(self.num_variables)
        for i in range(self.num_variables):
            col = self.tableau[:-1, i]
            if np.sum(col == 1) == 1 and np.sum(col == 0) == len(col) - 1:
                row = np.where(col == 1)[0][0]
                solution[i] = self.tableau[row, -1]
        return solution, self.tableau[-1, -1]