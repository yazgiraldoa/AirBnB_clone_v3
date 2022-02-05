#!/usr/bin/python3
"""
This module contains route
to check status of API
"""
import models
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """Endpoint to check the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def count_by_class():
    """Endpoint that retrieves the number of each objects by type"""
    classes = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
    }
    count_by_class = {}

    for key, value in classes.items():
        count = models.storage.count(value)
        count_by_class[key] = count
    return count_by_class


if __name__ == "__main__":
    pass
