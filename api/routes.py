from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from core.containers import container
from core.interfaces import SimplexSolver, BigMSolver, TwoPhaseSolver, GoalProgrammingSolver

api_blueprint = Blueprint("api", __name__)

@api_blueprint.route("/solve/simplex", methods=["POST"])
@inject
def solve_simplex(simplex_solver: SimplexSolver = Provide[container.simplex_solver]):
    data = request.json
    result = simplex_solver.solve(data)
    return jsonify(result)

@api_blueprint.route("/solve/big-m", methods=["POST"])
@inject
def solve_big_m(big_m_solver: BigMSolver = Provide[container.big_m_solver]):
    data = request.json
    result = big_m_solver.solve(data)
    return jsonify(result)

@api_blueprint.route("/solve/two-phase", methods=["POST"])
@inject
def solve_two_phase(two_phase_solver: TwoPhaseSolver = Provide[container.two_phase_solver]):
    data = request.json
    result = two_phase_solver.solve(data)
    return jsonify(result)

@api_blueprint.route("/solve/goal-programming", methods=["POST"])
@inject
def solve_goal(goal_solver: GoalProgrammingSolver = Provide[container.goal_solver]):
    data = request.json
    result = goal_solver.solve(data)
    return jsonify(result)
