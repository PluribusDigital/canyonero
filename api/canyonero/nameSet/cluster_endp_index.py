import sys
import datetime
import json
from flask import request
from flask_restful import abort, Resource
from flask_restful.reqparse import RequestParser
from canyonero.nameSet import *

def linkBuilder(baseUri):
    def build(x):
        return {'link': 
             {'href': baseUri + '/{}'.format(x.key),
              'rel': 'item',
              'title': x.canon,
              'type': 'application/json'}
             }
    return build

class ClusterEndpointIndex(Resource):
    """ The collection endpoint for all the known clusters of a name set
    """
    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------
    @classmethod
    def returnAll(cls):
        parser = RequestParser()
        parser.add_argument('all', type=bool, location='args')
        args = parser.parse_args()
        print(args)
        return args['all'] != None

    # -------------------------------------------------------------------------
    # HTTP Methods
    # -------------------------------------------------------------------------

    def get(self, id):
        """Retrieves the clusters for this name set"""
        context = DataContext()
        if id not in context:
            abort(404, message="'{}' doesn't exist".format(id))

        nameSet = context[id]
        build = linkBuilder(request.base_url)
        all = self.returnAll()
        gen = (nameSet.clusters[k] for k in sorted(nameSet.clusters))

        return [build(x) for x in gen if all or not x.validated]

    def post(self, id):
        """Creates a new cluster from scratch. 
        These will not survive regeneration
        """
        context = DataContext()
        if id not in context:
            abort(404, message="'{}' doesn't exist".format(id))

        return '', 400