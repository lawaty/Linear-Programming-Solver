from core.Solver import Solver
# from Solver import Solver
import numpy as np

class BigM(Solver):
    def __init__(self, objective, constraints, rhs, num_variables , constraints_type):
        self.M = 1e6  # Large M value
        self.constraints_type = constraints_type
        super().__init__(objective, constraints, rhs, num_variables)

    def _initialize_tableau(self):
        rows, cols = self.constraints.shape
        num_artificial = sum(1 for type in self.constraints_type if type in ['=' , '>='])  # Count artificial variables
        num_surplus = sum(1 for type in self.constraints_type if type == '>=')  # Count surplus variables
        num_slacks = sum(1 for type in self.constraints_type if type == '<=' )  # Count slack variables
        tableau = np.zeros((rows + 1, cols + num_slacks + num_surplus + num_artificial + 1))
        
        # Constraints Rows
        tableau[:-1, :cols] = self.constraints  # Decision variables
        tableau[:-1, cols:cols + rows] = np.eye(rows)  # Slack variables
        tableau[:-1, -1] = self.rhs  # RHS column
        
        # Identify artificial and surplus variables and modify constraints accordingly
        artificial_idx = cols + num_slacks
        surplus_idx = cols + num_slacks + num_artificial
        self.artificial_vars = []
        artificial_rows = []
        for i , type in zip(range(len(self.rhs)) , self.constraints_type):
            if type == '=':  # Handle equality constraints
                tableau[i, artificial_idx] = 1  # Add artificial variable
                self.artificial_vars.append(artificial_idx)
                artificial_rows.append(i)
                artificial_idx += 1
        
            elif type == '>=':  # ##Flip inequality## for >= constraints
                
                tableau[i, surplus_idx] = -1  # Add surplus variable
                surplus_idx += 1
                tableau[i, artificial_idx] = 1  # Add artificial variable
                self.artificial_vars.append(artificial_idx)
                artificial_rows.append(i)
                artificial_idx += 1

        tableau[-1, :cols] = -self.objective  # Standard objective
        tableau[-1, self.artificial_vars] = self.M  # Penalize artificial variables
        for row in artificial_rows:
            tableau[-1, :] -= self.M * tableau[row , :]  # Penalize artificial variables
        
        print("Initial Tableau:")
        print(tableau.astype(int))
        return tableau
    
    
    def solve(self):
        """Implements the Big-M method using the base Solver utilities."""
        while not self._is_optimal():
            pivot_col = self._get_pivot_column()
            pivot_row = self._get_pivot_row(pivot_col)
            if self.tableau[pivot_row, pivot_col] <= 0:
                print("Unbounded solution detected.")
                return {"feasible": False, "solution": None, "optimal_value": None, "history": self.history}
            self._apply_gauss(pivot_row, pivot_col)
            self._store_tableau()
        
         # Check for infeasibility
        # artificial_values = self.tableau[:-1, self.artificial_vars]
        # if any(artificial_values[:, -1] > 0):  # Check if any artificial variable is non-zero
        # print(self.tableau.astype(int))
        if not np.all(self.tableau[:, -1] >= 0) :
            # print("artificial vars = ", self.artificial_vars)
            return {"feasible" : False , "solution": None, "optimal_value": None, "history": self.history}
        
        solution, optimal_value = self._extract_solution()
        return {"feasible" : True ,"solution": solution.tolist(), "optimal_value": optimal_value, "history": self.history}


if __name__ == "__main__":
    # Example problem: Maximize z = 3x1 + 2x2
    # Subject to:
    # 2x1 + x2 <= 8
    # 2x1 + x2 >= 8

    data = {"objective":[3,2],"constraints":[[2,1],[2,1]],"rhs":[8,8],"constraints_type":["<=",">="]}
    
    big_m_solver = BigM(
        data["objective"], data["constraints"], data["rhs"], len(data["objective"]), data['constraints_type']
    )
    result = big_m_solver.solve()

    print("Optimal Solution:", result["solution"])
    print("Optimal Value:", result["optimal_value"])
   
