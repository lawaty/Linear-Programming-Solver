from flask import Blueprint, request, jsonify
from core.Simplex import Simplex
from core.BigM import BigM
from core.TwoPhase import TwoPhase
from core.GoalProgramming import GoalProgramming
from core.interfaces import SimplexSolver, BigMSolver, TwoPhaseSolver, GoalProgrammingSolver

# Create Blueprint
api_blueprint = Blueprint("api", __name__)

# Directly instantiate solvers, ensuring they implement the interfaces
simplex_solver: SimplexSolver = Simplex()
big_m_solver: BigMSolver = BigM()
two_phase_solver: TwoPhaseSolver = TwoPhase()
goal_solver: GoalProgrammingSolver = GoalProgramming()

@api_blueprint.route("/solve/simplex", methods=["POST"])
def solve_simplex():
    data = request.json
    result = simplex_solver.solve(data)
    return jsonify(result)

@api_blueprint.route("/solve/big-m", methods=["POST"])
def solve_big_m():
    data = request.json
    result = big_m_solver.solve(data)
    return jsonify(result)

@api_blueprint.route("/solve/two-phase", methods=["POST"])
def solve_two_phase():
    data = request.json
    result = two_phase_solver.solve(data)
    return jsonify(result)

@api_blueprint.route("/solve/goal-programming", methods=["POST"])
def solve_goal():
    data = request.json
    result = goal_solver.solve(data)
    return jsonify(result)
