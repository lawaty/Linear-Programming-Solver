from flask import Blueprint, request, jsonify
import numpy as np
from core.Simplex import Simplex
from core.BigM import BigM
from core.TwoPhase import TwoPhase
from core.GoalProgramming import GoalProgramming
from sympy import N, Basic, Matrix

def serialize_obj(obj):
    """Converts SymPy and NumPy objects to JSON-friendly types."""
    if isinstance(obj, (list, tuple)):
        return [serialize_obj(item) for item in obj]
    if isinstance(obj, dict):
        return {key: serialize_obj(value) for key, value in obj.items()}
    if isinstance(obj, (int, float, np.number)):
        return obj
    if isinstance(obj, np.ndarray):
        return obj.tolist()  # Convert numpy array to list
    if isinstance(obj, Matrix):
        return obj.tolist()  # Convert SymPy Matrix to list
    if isinstance(obj, Basic):  # SymPy expression
        try:
            return float(N(obj))  # Convert to float using SymPy's N()
        except (TypeError, ValueError):
            return str(obj)  # Fallback to string representation
    return obj  # Return as-is if already JSON serializable

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
    return jsonify(serialize_obj(result))

@api_blueprint.route("/solve/big-m", methods=["POST"])
def solve_big_m():
    data = request.json
    big_m_solver = BigM(
        data["objective"], data["constraints"], data["rhs"], len(data["objective"]), data['constraints_type']
    )
    result = big_m_solver.solve()
    return jsonify(serialize_obj(result))

@api_blueprint.route("/solve/two-phase", methods=["POST"])
def solve_two_phase():
    data = request.json
    two_phase_solver = TwoPhase(
        data["objective"], data["constraints"], data["rhs"], len(data["objective"]), data['constraints_type']
    )
    result = two_phase_solver.solve()
    return jsonify(serialize_obj(result))

@api_blueprint.route("/solve/goal-programming", methods=["POST"])
def solve_goal():
    data = request.json
    print(data, len(data["goals_lhs"][0]))
    goal_solver = GoalProgramming(
        np.array(data['goals']), np.array(data["goals_lhs"]), np.array(data['priorities']), 
        np.array(data["constraints"]), np.array(data["rhs"]), np.array(data['constraints_type']), 
        len(data["goals_lhs"][0])
    )
    result = goal_solver.solve()
    return jsonify(serialize_obj(result))
