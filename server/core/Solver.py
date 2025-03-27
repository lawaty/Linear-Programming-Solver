import numpy as np

class Solver:
    def __init__(self, objective, constraints, rhs, num_variables):
        self.objective = np.array(objective, dtype=float)
        self.constraints = np.array(constraints, dtype=float)
        self.rhs = np.array(rhs, dtype=float)
        self.num_variables = num_variables
        self.tableau = self._initialize_tableau()
        if isinstance(self.tableau, tuple) and len(self.tableau) == 2:
            self.tableau, self.artificial = self.tableau 
        self.history = [] 
        self._store_tableau() 
        
    def _initialize_tableau(self):
        """To be overriden in subclasses"""
        pass
    
    def _store_tableau(self):
        self.history.append(self.tableau.copy().tolist())
        
    def _get_pivot_column(self):
        return np.argmin(self.tableau[-1, :-1])
    
    def _get_pivot_row(self, pivot_col):
        ratios = self.tableau[:-1, -1] / self.tableau[:-1, pivot_col]
        for i in range(len(ratios)):
            if ratios[i] <= 0:
                ratios[i] = float('inf')
                
        return np.argmin(ratios)
    
    def _apply_gauss(self, pivot_row, pivot_col):
        """Normalize Pivot Row, then apply ERO to the other rows"""
        self.tableau[pivot_row, :] /= self.tableau[pivot_row, pivot_col]
        for i in range(self.tableau.shape[0]):
            if i != pivot_row:
                self.tableau[i, :] -= self.tableau[i, pivot_col] * self.tableau[pivot_row, :]

    def _is_optimal(self):
        return np.all(self.tableau[-1, :-1] >= 0)
    
    def _extract_solution(self):
        """Extracts the solution from the final tableau."""
        solution = np.zeros(self.num_variables)
        for i in range(self.num_variables):
            col = self.tableau[:-1, i]
            if np.sum(col == 1) == 1 and np.sum(col == 0) == len(col) - 1: # Basic Variable
                row = np.where(col == 1)[0][0]
                solution[i] = self.tableau[row, -1]
        return solution, self.tableau[-1, -1]