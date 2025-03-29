from core.Solver import Solver
import numpy as np
import sympy as sp
np.set_printoptions(precision=2, suppress=True)
class GoalProgramming(Solver):
    def __init__(self, goals, goals_lhs, priorities,constraints, constraints_rhs, constraints_type ,num_variables):
        sorted_indices = np.argsort(priorities)  # Sort indices based on priorities 
        print(sorted_indices)
        goals = goals[sorted_indices]
        goals_lhs = goals_lhs[sorted_indices]  # Sort goals_lhs based on sorted indices
        # priorities = priorities[sorted_indices]  # Sort priorities based on sorted indices

        self.Ps = np.array([sp.symbols(f'P{i+1}') for i in range(len(goals))])
        self.goals = np.array(goals, dtype=float)
        self.num_goals = len(goals)
        self.goals_lhs = np.array(goals_lhs, dtype=float)
        self.constraints = np.array(constraints, dtype=float)
        self.num_constraints = len(constraints)
        self.constraints_rhs = np.array(constraints_rhs, dtype=float)
        self.constraints_type = constraints_type
        self.num_variables = num_variables
        self.tableau = self._initialize_tableau()
        if isinstance(self.tableau, tuple) and len(self.tableau) == 2:
            self.tableau, self.artificial = self.tableau 
        self.history = [] 
        self.goals_achived = []
        self._store_tableau() 
        # self.priorities = list(range(1 , num_variables+1))  # Priorities for preemptive goal programming


    def _initialize_tableau(self):
        """Initialize the tableau for preemptive goal programming."""
        # rows, self.cols = self.constraints.shape
        # rows += self.num_goals  # Add rows for goals
        
        # rows
        self.goals_objective_rows = list(range(self.num_goals))  # Rows for goal objective
        goals_constraints_rows = [self.num_goals + i for i in range(self.num_goals)]  # Rows for goal constraints
        constarints_rows = [self.num_goals*2 for i in range(self.num_constraints)]  # Rows for constraints
        self.total_rows_num =  len(self.goals_objective_rows) + len(goals_constraints_rows) + len(constarints_rows) 
        
        #cols
        self.num_deviation = len(self.goals)  # Count deviation variables (d+ and d-)
        self.num_slacks = sum(1 for type in self.constraints_type if type == '<=' )  # Count slack variables
        
        total_cols_num = self.num_variables + self.num_deviation*2 + self.num_slacks  + 1  # Decision variables + slack variables + deviation variables + RHS
        vars_cols = np.arange(self.num_variables)  # Decision variables
        dp_cols = np.arange(self.num_variables, self.num_variables + self.num_deviation)  # d+ variables
        dn_cols = np.arange(self.num_variables + self.num_deviation, self.num_variables + 2*self.num_deviation)  # d- variables
        slack_cols = np.arange(self.num_variables + 2*self.num_deviation, self.num_variables + 2*self.num_deviation + self.num_slacks)  # Slack variables
        
        tableau = np.zeros((self.total_rows_num , total_cols_num) , dtype=object)
        # p_tableau = np.zeros((self.total_rows_num , total_cols_num))
        # self.vars_on_left = np.arange(self.cols, self.cols + self.num_slacks + self.num_deviation)  # Slack variables + artificial variables
        # Constraints Rows


    #filling tableau with goals and constraints
        # goals objective rows
        tableau[np.ix_(self.goals_objective_rows, vars_cols)] = self.goals_lhs  # Decision variables  #BUG *p
        tableau[np.ix_(self.goals_objective_rows, dp_cols)] = -np.eye(self.num_goals)  # d+ variables #BUG *p
        tableau[self.goals_objective_rows, -1] = self.goals  # RHS column #BUG *p

        # goals constraints rows
        tableau[np.ix_(goals_constraints_rows, vars_cols)] = self.goals_lhs  # Decision variables
        tableau[np.ix_(goals_constraints_rows, dp_cols)] = -np.eye(self.num_goals)  # d+ variables
        tableau[np.ix_(goals_constraints_rows, dn_cols)] = np.eye(self.num_goals)  # d- variables
        tableau[goals_constraints_rows, -1] = self.goals  # RHS column

        # constraints rows
        tableau[np.ix_(constarints_rows, vars_cols)] = self.constraints  # Decision variables
        tableau[np.ix_(constarints_rows, slack_cols)] = np.eye(self.num_slacks)  # Slack variables
        tableau[constarints_rows, -1] = self.constraints_rhs  # RHS column

        #P tableau
        for i,p,d in zip(range(self.num_goals) , self.Ps, dp_cols):
    
            tableau[self.goals_objective_rows[i], vars_cols ] *= p  # Set the priority for each goal
            tableau[self.goals_objective_rows[i], d] *= p  # Set the priority for each goal
            tableau[self.goals_objective_rows[i], -1] *= p  # Set the priority for each goal
        

       
       
        return tableau

    def solve(self):
        """Implements the preemptive goal programming algorithm."""
        for i in range(self.num_goals):
            partial_rows = list(range(self.total_rows_num))
            partial_rows = [row for row in partial_rows if row not in self.goals_objective_rows or (row in self.goals_objective_rows and row == i)]
            partial_tableau = self.tableau[partial_rows, :]
            partial_tableau[0 , :] /= self.Ps[i] # remove ps temporarily for calculating pivot row and column
            partial_tableau = partial_tableau.astype(float)  # Convert to float for division


            # Check if all elements in the first row are non-positive
            if all(partial_tableau[0, :-1] <= 0):
                print("All elements in the first row are non-positive. Continuing to the next goal.")
                print(f"goal{i+1} not optimized")
                continue
            
            
            pivot_col = np.argmax(partial_tableau[0, :-1])
            
            # Check if any element in rows from 0 to i in the pivot column is negative
            if any(float(self.tableau[row, pivot_col]) < 0 for row in range(i) if isinstance(self.tableau[row, pivot_col], (int, float))):
                print(f"Negative element found in pivot column {pivot_col} for rows 0 to {i}.")
                print(f"goal{i+1} not optimized")
                continue


            ratios = partial_tableau[1:, -1] / partial_tableau[1:, pivot_col]
            for j in range(len(ratios)):
                if ratios[j] <= 0:
                    ratios[j] = float('inf')
            
            partial_pivot_row = np.argmin(ratios , ) + 1
            pivot_row  = partial_pivot_row + self.num_goals -1 # Adjust for the offset of the original tableau 
          
            # Apply gaussain
            self.tableau[pivot_row, :] /= self.tableau[pivot_row, pivot_col]
            for j in range(self.tableau.shape[0]):
                if j != pivot_row:
                    self.tableau[j, :] -= self.tableau[j, pivot_col] * self.tableau[pivot_row, :]
            self._store_tableau()
            
            partial_tableau = self.tableau[partial_rows, :]
            partial_tableau[0 , :] /= self.Ps[i] # remove ps temporarily for calculating pivot row and column
            partial_tableau = partial_tableau.astype(float)  # Convert to float for division
           
            
            for j in range(partial_tableau.shape[1] ):
                if partial_tableau[0, j] > 1e-10:
                    print(f"goal{i+1} not optimized")
                    break
            else:
                print(f"goal {i+1} optimized.")
                self.goals_achived.append(i)
            
            partial_tableau = partial_tableau.astype(object) # Convert back to object for symbolic operations
            partial_tableau[0 , :] *= self.Ps[i] # restore ps after calculating pivot row and column
            self.tableau[partial_rows, :] = partial_tableau # Update the original tableau with the modified partial tableau
            

            self._store_tableau()
        

        # Remove all Ps from self.tableau and convert it to float
        
        for i in range(self.num_goals):
            self.tableau[self.goals_objective_rows[i], :] /= self.Ps[i]
        self.tableau = self.tableau.astype(float)
        return {"optimized":  [True if i in self.goals_achived else False for i in range(self.num_goals)],
                "optimal_value":self.tableau[self.goals_objective_rows , -1],
                  "history": self.history
                  }



if __name__ == "__main__":
    # Example problem for Preemptive Goal Programming
        # set to: 
        # 7x1 + 3x2 >= 40       # 1st goal
        # 10x1 + 5x2 >= 60      # 2nd goal
        # 5x1 + 4x2 >= 35       # 3rd goal
        # 100x1 + 60x2 <= 600   # constraint

    goals_lhs = np.array([
        [7, 3],
        [5, 4],
        [10, 5],
    ])
    goals = np.array([40, 35,60 ])
    priorities = np.array([1, 3, 2])
    
    constraints = np.array([
        [100, 60]
    ])
    constraints_rhs = np.array([600])
    constraints_type = ['<=']
    
    num_variables = 2

    goal_programming_solver = GoalProgramming(goals, goals_lhs, priorities,constraints, constraints_rhs, constraints_type ,num_variables)
    result = goal_programming_solver.solve()

    print("optimized:", result["optimized"])
    print("Optimal Value:", result["optimal_value"])
    # print("History of Tableaus:\n", result["history"])
