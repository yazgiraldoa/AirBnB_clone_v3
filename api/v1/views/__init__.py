#!/usr/bin/python3
"""
This module has routes to app_views
"""
from flask import Blueprint


app_views = Blueprint('app_views',
                      __name__,
                      template_folder='templates',
                      url_prefix="/api/v1"
                      )

from api.v1.views.index import *
