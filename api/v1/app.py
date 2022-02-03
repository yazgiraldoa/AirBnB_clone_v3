#!/usr/bin/python3
"""
Module that starts an API for AirBnB_Clone
Running on host: HBNB_API_HOST:HBNB_API_PORT
Or 0.0.0.0:5000 if below env's is not define
"""
from api.v1.views import app_views
from flask import Flask
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    storage.close()


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST") if getenv("HBNB_API_HOST") else "0.0.0.0"
    port = getenv("HBNB_API_PORT") if getenv("HBNB_API_PORT") else 5000
    app.run(host=host, port=port, threaded=True)
