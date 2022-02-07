#!/usr/bin/python3
"""
New view for State objects
that handles all default
RESTFul API actions
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from flasgger import swag_from


@app_views.route("/states", methods=["GET"], strict_slashes=False)
@swag_from('swagger/states/all_states.yml')
def all_State():
    """Route that return all States in storage"""
    allStates = storage.all(State)
    allStates = [state.to_dict() for state in allStates.values()]
    return jsonify(allStates)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
@swag_from('swagger/states/one_state.yml')
def one_State(state_id):
    """Method that return a State with specific id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404, description="State not found")
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
@swag_from('swagger/states/del_state.yml')
def del_State(state_id):
    """Method that delete one State and save changes in storage"""
    state = storage.get(State, state_id)

    if not state:
        return abort(404, description="State not found")

    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/", methods=["POST"], strict_slashes=False)
@swag_from('swagger/states/new_state.yml')
def new_State():
    """Method that create new State and save it into storage"""
    json = request.get_json()
    if not json:
        return "Not a JSON", 400
    if not json.get("name"):
        return "Missing name", 400

    new_state = State(**json)
    storage.new(new_state)
    storage.save()
    return jsonify(storage.get(State, new_state.id).to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
@swag_from('swagger/states/update_state.yml')
def update_State(state_id):
    """Method that Updates a State and save changes in storage"""
    json = request.get_json()
    if not json:
        return "Not a JSON", 400

    state = storage.get(State, state_id)
    if not state:
        abort(404)
    for key, value in json.items():
        if key != "id" and key != "created_at" and key != "updated_at":
            setattr(state, key, value)
    storage.save()
    return jsonify(storage.get(State, state.id).to_dict()), 200
