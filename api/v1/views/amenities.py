#!/usr/bin/python3
"""
View for Amenity objects
that handles all default
RESTFul API actions
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flasgger import swag_from


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
@swag_from('swagger/amenities/all_amenities.yml')
def all_amenities():
    """Method that returns JSON with all amenities"""
    all_amenities = storage.all(Amenity)
    all_amenities = [amenity.to_dict() for amenity in all_amenities.values()]
    return jsonify(all_amenities)


@app_views.route("/amenities/<amenity_id>",
                 methods=["GET"],
                 strict_slashes=False)
@swag_from('swagger/amenities/one_amenity.yml')
def one_amenity(amenity_id):
    """Method that get an Amentity from storage with specific id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
@swag_from('swagger/amenities/del_amenity.yml')
def delete_amenity(amenity_id):
    """Method that deletes an Amenity and save change in storage"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities/", methods=["POST"], strict_slashes=False)
@swag_from('swagger/amenities/new_amenity.yml')
def create_amenity():
    """Method that creates new amenity and save it in storage"""
    json = request.get_json()
    if not json:
        return "Not a JSON", 400
    if not json.get("name"):
        return "Missing name", 400
    new_amenity = Amenity(**json)
    storage.new(new_amenity)
    storage.save()

    return jsonify(storage.get(Amenity, new_amenity.id).to_dict()), 201


@app_views.route("/amenities/<amenity_id>",
                 methods=["PUT"],
                 strict_slashes=False)
@swag_from('swagger/amenities/update_amenity.yml')
def update_amenity(amenity_id):
    """Method that updates an Amenity and save changes in storage"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    json = request.get_json()
    if not json:
        return "Not a JSON", 400

    for key, value in json.items():
        if key != "id" and key != "created_at" and key != "updated_at":
            setattr(amenity, key, value)
    storage.save()
    return jsonify(storage.get(Amenity, amenity.id).to_dict()), 200
