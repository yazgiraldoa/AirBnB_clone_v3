#!/usr/bin/python3
"""
View for Place objects that handles
all default RESTFul API actions
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from flasgger import swag_from


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
@swag_from('swagger/places/all_places.yml')
def all_places_in_city(city_id):
    """Method that retrieves the list of all Place objects of a City"""
    places_objs = storage.all(Place)
    city = storage.get(City, city_id)
    places_list = []
    if not city:
        abort(404)
    for place in places_objs.values():
        if place.city_id == city_id:
            places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
@swag_from('swagger/places/one_place.yml')
def place_by_id(place_id):
    """Method that retrieves a Place object by id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
@swag_from('swagger/places/del_place.yml')
def delete_place_by_id(place_id):
    """Method that deletes a Place object by id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
@swag_from('swagger/places/new_place.yml')
def create_place(city_id):
    """Method that creates a Place object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    json = request.get_json()
    if not json:
        return "Not a JSON", 400
    if not json.get("user_id"):
        return "Missing user_id", 400
    user_id = storage.get(User, json.get("user_id"))
    if not user_id:
        abort(404)
    if not json.get("name"):
        return "Missing name", 400

    json["city_id"] = city_id
    place = Place(**json)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
@swag_from('swagger/places/update_place.yml')
def update_place(place_id):
    """Method that updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    json = request.get_json()
    if not json:
        return "Not a JSON", 400

    not_allowed = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key, value in json.items():
        if key not in not_allowed:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
