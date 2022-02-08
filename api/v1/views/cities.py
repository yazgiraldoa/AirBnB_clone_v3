#!/usr/bin/python3
"""
View for City objects that handles
all default RESTFul API actions
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flasgger import swag_from


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
@swag_from('swagger/cities/all_cities.yml')
def all_cities_in_state(state_id):
    """Method that retrieves the list of all City objects of a State"""
    city_objs = storage.all(City)
    state = storage.get(State, state_id)
    cities_list = []
    if not state:
        abort(404)
    for city in city_objs.values():
        if city.state_id == state_id:
            cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route("/cities/<city_id>", methods=["GET"],
                 strict_slashes=False)
@swag_from('swagger/cities/one_city.yml')
def city_by_id(city_id):
    """Method that retrieves a City object by id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
@swag_from('swagger/cities/del_city.yml')
def delete_city_by_id(city_id):
    """Method that deletes a City object by id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
@swag_from('swagger/cities/new_city.yml')
def create_city(state_id):
    """Method that creates a City object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    json = request.get_json()
    if not json:
        return "Not a JSON", 400
    if not json.get("name"):
        return "Missing name", 400

    json["state_id"] = state_id
    city = City(**json)
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
@swag_from('swagger/cities/update_city.yml')
def update_city(city_id):
    """Method that updates a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    json = request.get_json()
    if not json:
        return "Not a JSON", 400

    not_allowed = ["id", "state_id", "created_at", "updated_at"]
    for key, value in json.items():
        if key not in not_allowed:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
