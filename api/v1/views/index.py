#!/usr/bin/python3
"""
This module contains route
to check status of API
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """Method to check API Status"""
    return jsonify({"status": "OK"})


if __name__ == "__main__":
    pass
