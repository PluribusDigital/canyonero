import sys
import datetime
import json
from flask import request, make_response
from flask_restful import abort, Resource
from flask_restful.reqparse import RequestParser
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

        nameSet = context[id]
        
        parser = RequestParser()
        parser.add_argument('recalculate', type=int, default=-1)
        args = parser.parse_args()
        if args['recalculate'] != -1:
            nameSet.threshold = args['recalculate']
            nameSet.buildClusters()

        data = json.dumps(nameSet, cls=ModelEncoder)
        return make_response(data, 200, {})

    def delete(self, id):
        """Deletes the name set"""
        context = DataContext()
        if id not in context:
            abort(404, message="'{}' doesn't exist".format(id))

        del context[id]
        return '', 204
