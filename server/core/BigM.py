from .interfaces import ISolver
from .Solver import Solver
import numpy as np

class BigM(Solver, ISolver):
    def __init__(self, objective, constraints, rhs, num_variables , constraints_type):
        self.M = 1e6  # Large M value
        self.constraints_type = constraints_type
        super().__init__(objective, constraints, rhs, num_variables)

    def _initialize_tableau(self):
        rows, cols = self.constraints.shape
        num_artificial = sum(1 for type in self.constraints_type if type in ['=' , '>='])  # Count artificial variables
        num_surplus = sum(1 for type in self.constraints_type if type == '>=')  # Count surplus variables
        num_slacks = sum(1 for type in self.constraints_type if type == '<=' )  # Count slack variables
        # print(f"rows = {rows}, cols = {cols}, num_slacks = {num_slacks}, num_surplus = {num_surplus}, num_artificial = {num_artificial}")
        tableau = np.zeros((rows + 1, cols + num_slacks + num_surplus + num_artificial + 1))
        
        # Constraints Rows
        tableau[:-1, :cols] = self.constraints  # Decision variables
        tableau[:-1, cols:cols + rows] = np.eye(rows)  # Slack variables
        tableau[:-1, -1] = self.rhs  # RHS column
        # print(tableau)
        
        # Identify artificial and surplus variables and modify constraints accordingly
        artificial_idx = cols + num_slacks
        surplus_idx = cols + num_slacks + num_artificial
        artificial_vars = []
        artificial_rows = []
        for i , type in zip(range(len(self.rhs)) , self.constraints_type):
            if type == '=':  # Handle equality constraints
                tableau[i, artificial_idx] = 1  # Add artificial variable
                artificial_vars.append(artificial_idx)
                artificial_rows.append(i)
                artificial_idx += 1
        
            elif type == '>=':  # ##Flip inequality## for >= constraints
                # tableau[i, :cols] *= -1
                
                # tableau[i, cols:cols + rows] *= -1
                print(f"i = {i} , surplus_idx = {surplus_idx} , tableau[i] = {tableau[i]}")
                tableau[i, surplus_idx] = -1  # Add surplus variable
                # print(tableau)
                surplus_idx += 1
                tableau[i, artificial_idx] = 1  # Add artificial variable
                artificial_vars.append(artificial_idx)
                artificial_rows.append(i)
                artificial_idx += 1

        # print()
        # print(tableau.astype(int))
        # Objective function row
        tableau[-1, :cols] = -self.objective  # Standard objective
        tableau[-1, artificial_vars] = self.M  # Penalize artificial variables
        print()
        print(tableau.astype(int))
        for row in artificial_rows:
            tableau[-1, :] -= self.M * tableau[row , :]  # Penalize artificial variables
        
        # print()
        # print(tableau.astype(int))
        return tableau
    
    def _is_equality_constraint(self, rhs_value):
        """Helper function to check if a constraint is an equality."""
    # Add logic to identify equality constraints (e.g., based on input format)
        if isinstance(rhs_value, str):
            return True
        return False  # Placeholder: Replace with actual condition
    
    def solve(self):
        """Implements the Big-M method using the base Solver utilities."""
        while not self._is_optimal():
            pivot_col = self._get_pivot_column()
            pivot_row = self._get_pivot_row(pivot_col)
            self._apply_gauss(pivot_row, pivot_col)
            self._store_tableau()
        
        solution, optimal_value = self._extract_solution()
        return {"solution": solution.tolist(), "optimal_value": optimal_value, "history": self.history}


if __name__ == "__main__":
    # Example problem: Maximize z = 3x + 4y
    # Subject to:
    # 2x + y <= 600
    # x  + y <= 225
    # 5x + 4y <= 1000
    # x + 2y >= 150
    objective = np.array([3, 4])
    constraints = np.array([
        [2, 1],
        [1, 1],
        [5, 4],
        [1, 2]
    ])
    rhs = np.array([600, 225, 1000, 150])
    constraints_type = ['<=', '<=', '<=', '>=']
    num_variables = 2

    bigm_solver = BigM(objective, constraints, rhs, num_variables , constraints_type)
    result = bigm_solver.solve()

    print("Optimal Solution:", result["solution"])
    print("Optimal Value:", result["optimal_value"])
    # print("History of Tableaus:\n", result["history"])