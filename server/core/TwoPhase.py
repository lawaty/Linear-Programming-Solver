from core.Solver import Solver
import numpy as np

class TwoPhase(Solver):
    def __init__(self, objective, constraints, rhs, num_variables , constraints_type):
        self.constraints_type = constraints_type
        super().__init__(objective, constraints, rhs, num_variables)

    def _initialize_tableau(self):
        rows, cols = self.constraints.shape
        num_artificial = sum(1 for type in self.constraints_type if type in ['=' , '>='])  # Count artificial variables
        num_surplus = sum(1 for type in self.constraints_type if type == '>=')  # Count surplus variables
        num_slacks = sum(1 for type in self.constraints_type if type == '<=' )  # Count slack variables
        tableau = np.zeros((rows + 1, cols + rows + num_artificial + 1))
        
        # Constraints Rows
        tableau[:-1, :cols] = self.constraints  # Decision variables
        tableau[:-1, cols:cols + rows] = np.eye(rows)  # Slack variables
        tableau[:-1, -1] = self.rhs  # RHS column
        
        # Identify artificial variables and modify constraints accordingly
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
        
        # Phase 1 Objective function row
        tableau[-1, :] = 0
        for row in artificial_rows:
            tableau[-1, :] += tableau[row , :]  # Sum artificial variable rows
        
        return tableau, artificial_vars

    
    def solve(self, data=None):
        # Phase 1: Solve to remove artificial variables
        self.tableau, artificial_vars = self._initialize_tableau()
        while not self._is_optimal():
            pivot_col = self._get_pivot_column()
            pivot_row = self._get_pivot_row(pivot_col)
            self._apply_gauss(pivot_row, pivot_col)
            self._store_tableau()
        
        # Check if artificial variables are eliminated
        if any(self.tableau[-1, idx] != 0 for idx in artificial_vars):
            return {"message": "Infeasible solution"}
        
        # Phase 2: Solve original objective
        self.tableau[-1, :] = 0
        self.tableau[-1, :self.num_variables] = -self.objective
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
        [-1, -2]
    ])
    rhs = np.array([600, 225, 1000, -150])
    num_variables = 2

    two_phase_solver = TwoPhase(objective, constraints, rhs, num_variables)
    result = two_phase_solver.solve()

    print("Optimal Solution:", result["solution"])
    print("Optimal Value:", result["optimal_value"])
    # print("History of Tableaus:\n", result["history"])
