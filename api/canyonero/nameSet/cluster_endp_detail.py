import sys
import json
from flask import request, make_response
from flask_restful import abort, Resource
from flask_restful.reqparse import RequestParser
from canyonero.nameSet import *

class ClusterEndpointDetail(Resource):
    """ Provides the endpoint for one cluster of a name set
    """
    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------
    @classmethod
    def checkRecalc(cls, nameSet):
        calc = False

        parser = RequestParser()
        parser.add_argument('recalculate', type=int, default=-1, location='args')
        args = parser.parse_args()
        if args['recalculate'] != -1:
            nameSet.threshold = args['recalculate']
            nameSet.buildClusters()
            calc = True

        return calc

    # -------------------------------------------------------------------------
    # HTTP Methods
    # -------------------------------------------------------------------------

    def get(self, id, key):
        """The cluster for this name set"""
        context = DataContext()
        if id not in context:
            abort(404, message="'{}' doesn't exist".format(id))

        nameSet = context[id]
        if key not in nameSet.clusters:
            abort(404, message="'{}' cluster doesn't exist".format(key))

        cluster = nameSet.clusters[key]

        data = json.dumps(cluster, cls=ModelEncoder)
        return make_response(data, 200, {})

    def post(self, id, key):
        """Operations on the cluster
        """
        context = DataContext()
        if id not in context:
            abort(404, message="'{}' doesn't exist".format(id))

        nameSet = context[id]
        if key not in nameSet.clusters:
            abort(404, message="'{}' cluster doesn't exist".format(key))

        cluster = nameSet.clusters[key]

        return '', 400