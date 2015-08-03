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
        return args['all'] != None

    def parse(self, encoded):
        if not encoded:
            return None
        
        s = encoded.decode('utf-8')
        try:
            return json.loads(s)
        except:
            err = sys.exc_info()[0]
            print(err)

        return None

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

        # extract the payload
        variant = self.parse(request.data)
        if not variant:
            abort(400, message="Not in the correct format")

        # see if it fits
        nameSet = context[id]
        key = nameSet.makeClusterKey(variant)
        if key in nameSet.clusters:
            abort(409, message="'{}' already exists as a cluster".format(variant))

        # build the cluster
        cluster = NameCluster(key)
        cluster.variations.append(variant)
        cluster.onComplete()
        cluster.validated = False

        nameSet.clusters[key] = cluster
        nameSet.names.append(variant)

        # return the ID and the link to this name set
        result = linkBuilder(request.base_url)(cluster)
        result.update({'key': key})
        return result, 201
