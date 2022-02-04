#!/usr/bin/python3
"""
New view for State objects
that handles all default
RESTFul API actions
"""
from flask import jsonify, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.state import City


@app_views.route("/states", methods=["GET"])
def all_State():
    """Route that return all States in storage"""
    allStates = storage.all(State)
    allStates = [state.to_dict() for state in allStates.values()]
    return jsonify(allStates)


@app_views.route("/states/<id>", methods=["GET"])
def one_State(id):
    """Method that return a State with specific id"""
    state = storage.get(State, id)
    if not state:
        abort(404, description="State not found")
    return jsonify(state.to_dict())


@app_views.route("/states/<id>", methods=["DELETE"])
def del_state(id):
    state = storage.get(State, id)
    storage.delete(state)
    storage.save()
    return "holi"
