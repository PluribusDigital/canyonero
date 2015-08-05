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

    def parseArgs(self):
        parser = RequestParser()
        parser.add_argument('variantToTransfer', location='args')
        parser.add_argument('transferToCluster', location='args')
        parser.add_argument('newClusterFromVariant', location='args')
        parser.add_argument('setAsCanon', location='args')
        args = parser.parse_args()

        operations = {
                      'transfer': (args['variantToTransfer'] != None and 
                                   args['transferToCluster'] != None),
                      'new': args['newClusterFromVariant'] != None,
                      'canon': args['setAsCanon'] != None
                      }
        return args, operations

    # -------------------------------------------------------------------------
    # Operations
    # -------------------------------------------------------------------------

    def getVariant(self, cluster, s):
        try:
            v = cluster.variations[int(s)]
        except ValueError:
            v = s if s in cluster.variations else None
        except IndexError:
            v = None
        
        if not v:
            abort(400, message="Variant '{}' doesn't exist".format(s))
        return v

    def transferToCluster(self, context, nameSet, cluster, args):
        variant = self.getVariant(cluster, args['variantToTransfer'])
        toCluster = args['transferToCluster']
        if toCluster not in nameSet.clusters:
            abort(400, message="Destination cluster '{}' doesn't \
            exist".format(toCluster))

        print(variant, toCluster)
        return '', 410

    def newCluster(self, context, nameSet, cluster, args):
        variant = self.getVariant(cluster, args['newClusterFromVariant'])
        key = nameSet.makeClusterKey(variant)
        if key in nameSet.clusters:
            abort(409, message="'{}' already exists as a cluster".format(variant))

        print(variant, key)
        return '', 410

    def setAsCanon(self, context, nameSet, cluster, args):
        variant = self.getVariant(cluster, args['setAsCanon'])
        print(variant)
        return '', 410

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

        # get the args
        args, ops = self.parseArgs()
        validOps = sum([1 for v in ops.values() if v])
        if validOps == 0:
            abort(400, message="Need to specify a valid operation")
        elif validOps > 1:
            abort(400, message="Can only perform one operation at a time")

        # route to the operation
        if ops['transfer']:
            return self.transferToCluster(context, nameSet, cluster, args)
        elif ops['new']:
            return self.newCluster(context, nameSet, cluster, args)
        elif ops['canon']:
            return self.setAsCanon(context, nameSet, cluster, args)

        return '', 501