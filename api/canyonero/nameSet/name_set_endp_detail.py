import sys
import datetime
import json
from flask import request
from flask_restful import abort, Resource
from canyonero.nameSet import *

class NameSetEndpointDetail(Resource):
    """ Provides the endpoint for one name set
    """
    # -------------------------------------------------------------------------
    # HTTP Methods
    # -------------------------------------------------------------------------

    def get(self, id):
        """Returns the name set"""
        context = DataContext()
        if id not in context:
            abort(404, message="'{}' doesn't exist".format(id))
        return context[id]
