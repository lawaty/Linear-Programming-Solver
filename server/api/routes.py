from flask import Blueprint, request, jsonify
from core.Simplex import Simplex
from core.BigM import BigM
from core.TwoPhase import TwoPhase
from core.GoalProgramming import GoalProgramming

# Create Blueprint
api_blueprint = Blueprint("api", __name__)

@api_blueprint.route("/solve/simplex", methods=["POST"])
def solve_simplex():
    data = request.json
    print(data)
    simplex_solver = Simplex(
        data["objective"], data["constraints"], data["rhs"], len(data["objective"])
    )
    result = simplex_solver.solve()
    return jsonify(result)

@api_blueprint.route("/solve/big-m", methods=["POST"])
def solve_big_m():
    data = request.json
    big_m_solver = BigM(
        data["objective"], data["constraints"], data["rhs"], len(data["objective"]), data['constraints_type']
    )
    result = big_m_solver.solve()
    return jsonify(result)

@api_blueprint.route("/solve/two-phase", methods=["POST"])
def solve_two_phase():
    data = request.json
    two_phase_solver = TwoPhase(
        data["objective"], data["constraints"], data["rhs"], len(data["objective"]), data['constraints_type']
    )
    result = two_phase_solver.solve()
    return jsonify(result)

@api_blueprint.route("/solve/goal-programming", methods=["POST"])
def solve_goal():
    data = request.json
    print(data, len(data["goals_lhs"][0]))
    goal_solver = GoalProgramming(
        data["goals_lhs"], data['goals'], data['priorities'], data["constraints"], data["rhs"], data['constraints_type'], len(data["goals_lhs"][0])
    )
    result = goal_solver.solve()
    return jsonify(result)
