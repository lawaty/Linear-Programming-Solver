import numpy as np
from core.Simplex import Simplex
from core.BigM import BigM
from core.TwoPhase import TwoPhase
from core.GoalProgramming import GoalProgramming
import pytest

def test_simplex1():
    # Example problem: Maximize z = 3x + 2y
    objective = np.array([3, 2])
    constraints = np.array([
        [2, 1],
        [1, 1],
        [1, 0]
    ])
    rhs = np.array([100, 80 , 40])
    num_variables = 2

    simplex_solver = Simplex(objective, constraints, rhs, num_variables)
    result = simplex_solver.solve()

    assert result['feasible'] == True
    assert result["optimal_value"] == pytest.approx(180)
    assert result["solution"] == [20.0, 60.0]

def test_simplex2():
    # Example problem: Maximize z = 6x1 + 5x2 + 4x3
    # Subject to:
    # 2x1 + x2 + x3 <= 240
    # 1x1 + 3x2 + 2x3 <= 360
    # 2x1 + 1x2  + 2x3 <= 300
    objective = np.array([6, 5, 4])
    constraints = np.array([
        [2, 1, 1],
        [1, 3, 2],
        [2, 1, 2]
    ])
    rhs = np.array([240, 360, 300])
    num_variables = 3
    
    simplex_solver = Simplex(objective, constraints, rhs, num_variables)
    result = simplex_solver.solve()

    assert result['feasible'] == True
    assert result["optimal_value"] == pytest.approx(912)
    assert result["solution"] == [72.0, 96.0, 0.0]


def test_bigm1():
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

    assert result['feasible'] == True
    assert result["optimal_value"] == pytest.approx(900)
    assert result["solution"] == [ 0.0 , 225.0]

def test_bigm2():
    # Example problem: Maximize z = 1x + 5y
    # Subject to:
    # 3x + 4y <= 6
    #  x + 3y >= 2

    objective = np.array([1, 5])
    constraints = np.array([
        [3, 4],
        [1, 3]
    ])
    rhs = np.array([6, 2])
    constraints_type = ['<=', '>=']
    num_variables = 2

    bigm_solver = BigM(objective, constraints, rhs, num_variables , constraints_type)
    result = bigm_solver.solve()

    assert result['feasible'] == True
    assert result["optimal_value"] == pytest.approx(7.5)
    assert result["solution"] == [ 0.0 , 1.5]

def test_big_m3():
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

    bigm_solver = BigM(objective, constraints, rhs, num_variables, constraints_type)
    result = bigm_solver.solve()

    assert result['feasible'] == True
    assert result["optimal_value"] == pytest.approx(10)
    assert result["solution"] == [0.0, 5.0, 5.0]

#infeasible
def test_big_m4():
    # Example problem: Maximize z = 3x1 + 2x2
    # Subject to:
    # x1 + x2 <= 2
    # 2x1 + 2x2 >= 6
    objective = np.array([3, 2])
    constraints = np.array([
        [1, 1],
        [2, 2]
    ])
    constraints_type = ['<=', '>=']
    rhs = np.array([2, 6])
    num_variables = 2

    bigm_solver = BigM(objective, constraints, rhs, num_variables, constraints_type)
    result = bigm_solver.solve()

    assert result["feasible"] == False

#infeasible
def  test_big_m5():
    # Example problem: Maximize z = 3x1 + 2x2
    # Subject to:
    # 2x1 + x2 <= 8
    # 2x1 + x2 >= 8
    data = {"objective":[3,2],"constraints":[[2,1],[2,1]],"rhs":[8,8],"constraints_type":["<=",">="]}
    
    big_m_solver = BigM(
        data["objective"], data["constraints"], data["rhs"], len(data["objective"]), data['constraints_type']
    )
    result = big_m_solver.solve()

    assert result["feasible"] == False


def test_two_phase1():
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
    constraints_type = ['<=', '<=', '<=', '>=']
    rhs = np.array([600, 225, 1000, -150])
    num_variables = 2

    two_phase_solver = TwoPhase(objective, constraints, rhs, num_variables, constraints_type)
    result = two_phase_solver.solve()

    assert result['feasible'] == True
    assert result["optimal_value"] == pytest.approx(900)
    assert result["solution"] == [0.0 , 225.0]

def test_two_phase2():
    # Example problem: Maximize z = 1x + 5y
    # Subject to:
    # 3x + 4y <= 6
    #  x + 3y >= 2

    objective = np.array([1, 5])
    constraints = np.array([
        [3, 4],
        [1, 3]
    ])
    rhs = np.array([6, 2])
    num_variables = 2
    constraints_type = ['<=', '>=']

    two_phase_solver = TwoPhase(objective, constraints, rhs, num_variables, constraints_type)
    result = two_phase_solver.solve()

    assert result['feasible'] == True
    assert result["optimal_value"] == pytest.approx(7.5)
    assert result["solution"] == [0.0 , 1.5]

def test_two_phase3():
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

    assert result['feasible'] == True
    assert result["optimal_value"] == pytest.approx(10)
    assert result["solution"] == [0.0, 5.0, 5.0]

def test_two_phase4():
    # Example problem: Maximize z = 3x1 + 2x2
    # Subject to:
    # x1 + x2 <= 2
    # 2x1 + 2x2 >= 6
    objective = np.array([3, 2])
    constraints = np.array([
        [1, 1],
        [2, 2]
    ])
    constraints_type = ['<=', '>=']
    rhs = np.array([2, 6])
    num_variables = 2

    two_phase_solver = TwoPhase(objective, constraints, rhs, num_variables, constraints_type)
    result = two_phase_solver.solve()

    assert result["feasible"] == False

def test_two_phase5():
    # Example problem: Maximize z = 3x1 + 2x2
    # Subject to:
    # 2x1 + x2 <= 8
    # 2x1 + x2 >= 8
    data = {"objective":[3,2],"constraints":[[2,1],[2,1]],"rhs":[8,8],"constraints_type":["<=",">="]}
    
    two_phase_solver = TwoPhase(
        data["objective"], data["constraints"], data["rhs"], len(data["objective"]), data['constraints_type']
    )
    result = two_phase_solver.solve()

    assert result["feasible"] == False

def test_goal_programming():
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

    # print("optimized:", result["optimized"])
    # print("Optimal Value:", result["optimal_value"])
    # Since the example is minimal, we just check if the solver runs without errors
    assert result["optimized"] == [True, True, False]
    assert result["optimal_value"] == pytest.approx([0.0, 0.0, 5.0])

