from core.Solver import Solver
from core.Simplex import Simplex
import numpy as np

class TwoPhase(Solver):
    def __init__(self, objective, constraints, rhs, num_variables , constraints_type):
        self.constraints_type = constraints_type
        super().__init__(objective, constraints, rhs, num_variables)

    def _initialize_tableau(self):
        rows, self.cols = self.constraints.shape
        self.num_artificial = sum(1 for type in self.constraints_type if type in ['=' , '>='])  # Count artificial variables
        num_surplus = sum(1 for type in self.constraints_type if type == '>=')  # Count surplus variables
        self.num_slacks = sum(1 for type in self.constraints_type if type == '<=' )  # Count slack variables
        tableau = np.zeros((rows + 1, self.cols + self.num_slacks+ num_surplus + self.num_artificial + 1))
        self.vars_on_left = np.arange(self.cols, self.cols + self.num_slacks + self.num_artificial)  # Slack variables + artificial variables
        # Constraints Rows
        tableau[:-1, :self.cols] = self.constraints  # Decision variables
        tableau[:-1, self.cols:self.cols + rows] = np.eye(rows)  # Slack variables
        tableau[:-1, -1] = self.rhs  # RHS column
        
        # Identify artificial variables and modify constraints accordingly
        artificial_idx = self.cols + self.num_slacks + num_surplus
        surplus_idx    = self.cols + self.num_slacks
        artificial_vars = []
        self.artificial_rows = []
        surplus_vars = []
        for i , type in zip(range(len(self.rhs)) , self.constraints_type):
            if type == '=':  # Handle equality constraints
                tableau[i, artificial_idx] = 1  # Add artificial variable
                artificial_vars.append(artificial_idx)
                self.artificial_rows.append(i)
                artificial_idx += 1
        
            elif type == '>=':  # ##Flip inequality## for >= constraints
                tableau[i, surplus_idx] = -1  # Add surplus variable
                surplus_vars.append(surplus_idx)
                surplus_idx += 1
                tableau[i, artificial_idx] = 1  # Add artificial variable
                artificial_vars.append(artificial_idx)
                self.artificial_rows.append(i)
                artificial_idx += 1
        
        tableau[-1, :] = 0
        for idx in artificial_vars:
            tableau[-1, idx] = -1
        for row in self.artificial_rows:
            tableau[-1, :] += tableau[row , :]  # Sum artificial variable rows
        tableau[-1, :] *= -1 # Minimize artificial variables
        
        return tableau, artificial_vars

    
    def solve(self, data=None):
        # Phase 1: Solve to remove artificial variables
        self.tableau, artificial_vars = self._initialize_tableau()
        self._store_tableau()
        artificials_exist = set(self.artificial_rows)
        while not self._is_optimal():
            pivot_col = self._get_pivot_column()
            pivot_row = self._get_pivot_row(pivot_col)
            self.vars_on_left[pivot_row] = pivot_col

            if pivot_row in artificials_exist:
                artificials_exist.remove(pivot_row)
            self._apply_gauss(pivot_row, pivot_col)
            self._store_tableau()
        
        # Check for infeasibility
        print(self.tableau.astype(int))
        if any(self.tableau[-1, :] < 0) or (any(self.tableau[-1, artificial_vars] != 0) and self.tableau[-1, -1] != 0) :
            return {"feasible" : False , "solution": None, "optimal_value": None, "history": self.history}
        
        self.tableau = np.delete(self.tableau, artificial_vars, axis=1)
        # Phase 2: Solve original objective
        self.tableau[-1, :] = 0
        self.tableau[-1, :self.num_variables] = -self.objective
        # # Remove artificial columns from tableau

        

        for basic_var in self.vars_on_left:
            pivot_row = np.where(self.vars_on_left == basic_var)[0][0]  # Find the row index of the basic variable
            objective_coeff = self.tableau[-1 , basic_var]  # Get the original coefficient of the basic variable
            self.tableau[-1, :] -= objective_coeff * self.tableau[pivot_row, :]  # Zero out the basic variable in the objective row
        self._store_tableau()

        while not self._is_optimal():
            pivot_col = self._get_pivot_column()
            pivot_row = self._get_pivot_row(pivot_col)
            if self.tableau[pivot_row, pivot_col] <= 0:
                print("Unbounded solution detected.")
                return {"feasible": False, "solution": None, "optimal_value": None, "history": self.history}
            self._apply_gauss(pivot_row, pivot_col)
            self._store_tableau()
            print(self.tableau , "\n")

        
        solution, optimal_value = self._extract_solution()
        return {"feasible" : True ,"solution": solution.tolist(), "optimal_value": optimal_value, "history": self.history}

if __name__ == "__main__":
   # Example problem: Maximize z = x1 -x2 + 3x3
    # Subject to:
    # x1 + x2 <= 20
    # x1 + x3 = 5
    # x2 + x3 >= 10
    objective = np.array([1, -1, 3])
    constraints = np.array([
        [1, 1, 0],
        [1, 0, 1],
        [0, 1, 1]
    ])
    constraints_type = ['<=', '=', '>=']
    rhs = np.array([20, 5, 10])
    num_variables = 3

    two_phase_solver = TwoPhase(objective, constraints, rhs, num_variables , constraints_type)
    result = two_phase_solver.solve()
    print("Optimal Solution:", result["solution"])
    print("Optimal Value:", result["optimal_value"])
