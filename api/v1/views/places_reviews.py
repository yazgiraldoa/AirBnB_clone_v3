#!/usr/bin/python3
"""
View for Review object
that handles all default
RESTFul API actions
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from flasgger import swag_from


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET"],
                 strict_slashes=False)
@swag_from('swagger/reviews/all_reviews.yml')
def all_reviews(place_id):
    """
    Method that get all reviews of Place
    that match with passed place_id
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    all_reviews = storage.all(Review)
    reviews = [review.to_dict() for review in all_reviews.values()
               if review.place_id == place.id]

    return jsonify(reviews)


@app_views.route("/reviews/<review_id>",
                 methods=["GET"],
                 strict_slashes=False)
@swag_from('swagger/reviews/one_review.yml')
def get_review(review_id):
    """Method that get Review with specific id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
@swag_from('swagger/reviews/del_review.yml')
def delete_review(review_id):
    """Method that deletes Review with specific id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews",
                 methods=["POST"],
                 strict_slashes=False)
@swag_from('swagger/reviews/new_review.yml')
def create_review(place_id):
    """Method that creates new Review for place with specific id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    json = request.get_json()
    if not json:
        return "Not a JSON", 400
    if not json.get("user_id"):
        return "Missing user_id", 400
    if not json.get("text"):
        return "Missing text", 400

    user = storage.get(User, json.get("user_id"))
    if not user:
        abort(404)

    json["place_id"] = place.id

    review = Review(**json)
    storage.new(review)
    storage.save()

    return jsonify(storage.get(Review, review.id).to_dict()), 201


@app_views.route("/reviews/<review_id>",
                 methods=["PUT"],
                 strict_slashes=False)
@swag_from('swagger/reviews/update_review.yml')
def update_review(review_id):
    """Method that updates Review with specific id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    json = request.get_json()
    if not json:
        return "Not a JSON", 400

    exceptions = ["id", "user_id", "place_id", "created_at", "updated_at"]

    for key, value in json.items():
        if key not in exceptions:
            setattr(review, key, value)

    storage.save()
    return jsonify(storage.get(Review, review.id).to_dict()), 200
