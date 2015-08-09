import sys
import json
from flask import request, make_response
from flask_restful import abort, Resource
from flask_restful.reqparse import RequestParser
from canyonero.nameSet import *

class NameSetEndpointCanon(Resource):
    """ Provides the endpoint for the canon map
    """
    # -------------------------------------------------------------------------
    # HTTP Methods
    # -------------------------------------------------------------------------

    def get(self, id):
        """Returns the canon/variant pairs for the current name set"""
        context = DataContext()
        if id not in context:
            abort(404, message="'{}' doesn't exist".format(id))

        result = []

        nameSet = context[id]
        for k in sorted(nameSet.clusters):
            c = nameSet.clusters[k]
            for v in sorted(c.variations):
                result.append({'canon': c.canon, 'variant': v})

        return result
