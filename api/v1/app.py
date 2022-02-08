#!/usr/bin/python3
"""
Module that starts an API for AirBnB_Clone
Running on host: HBNB_API_HOST:HBNB_API_PORT
Or 0.0.0.0:5000 if below env's is not define
"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import getenv
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
app.config['SWAGGER'] = {'title': 'AirBnB_Clone',
                         'description': 'Application that clones \
                             AirBnB page with all its features',
                         'version': "v3"}
app.register_blueprint(app_views)
cors = CORS(app, resources={r"*": {"origins": "0.0.0.0"}})

swagger = Swagger(app)


@app.errorhandler(404)
def page_not_found(e):
    """Function to handle 404 error"""
    return jsonify({'error': 'Not found'}), 404


@app.teardown_appcontext
def teardown_db(exception):
    """
    Teardown_X() closes or otherwise deallocates
    the resource if it exists. It is
    registered as a teardown_appcontext() handler.
    """
    storage.close()


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST") if getenv("HBNB_API_HOST") else "0.0.0.0"
    port = getenv("HBNB_API_PORT") if getenv("HBNB_API_PORT") else 5000
    app.run(host=host, port=port, threaded=True, debug=True)
