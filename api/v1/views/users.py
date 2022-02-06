#!/usr/bin/python3
"""
View for User objects that handles
all default RESTFul API actions
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def all_users():
    """Method that retrieves the list of all User objects"""
    users = storage.all(User)
    all_users = [user.to_dict() for user in users.values()]
    return jsonify(all_users)


@app_views.route("/users/<user_id>", methods=["GET"],
                 strict_slashes=False)
def user_by_id(user_id):
    """Method that retrieves a User object by id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user_by_id(user_id):
    """Method that deletes a User object by id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Method that creates a User object"""
    json = request.get_json()
    if not json:
        return "Not a JSON", 400
    if not json.get("email"):
        return "Missing email", 400
    if not json.get("password"):
        return "Missing password", 400

    user = User(**json)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """Method that updates a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    json = request.get_json()
    if not json:
        return "Not a JSON", 400

    not_allowed = ["id", "email", "created_at", "updated_at"]
    for key, value in json.items():
        if key not in not_allowed:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
