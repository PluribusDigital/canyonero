import json
from flask import request, make_response
from flask_restful import abort, Resource
from flask_restful.reqparse import RequestParser
from canyonero.nameSet import *

class NameSetEndpointAbbrev(Resource):
    """ Provides the endpoint for the abbreviations for one name set
    """
    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    def finish(self, nameSet):
        responseCode = 205

        parser = RequestParser()
        parser.add_argument('recalculate', type=int, default=-1)
        args = parser.parse_args()
        if args['recalculate'] != -1:
            nameSet.threshold = args['recalculate']
            nameSet.buildClusters()
            responseCode = 204

        return '', responseCode

    # -------------------------------------------------------------------------
    # HTTP Methods
    # -------------------------------------------------------------------------

    def get(self, id):
        """Lists all of the abbreviations in the name set"""
        context = DataContext()
        if id not in context:
            abort(404, message="'{}' doesn't exist".format(id))

        nameSet = context[id]
        return nameSet.abbrev, 200

    def put(self, id):
        """Updates the whole list of abbreviations"""
        context = DataContext()
        if id not in context:
            abort(404, message="'{}' doesn't exist".format(id))

        nameSet = context[id]

        if not request.data:
            abort(400, message="Abbreviations not in the correct format")        

        s = request.data.decode('utf-8') if request.data else '{}'
        if s[0] != '{':
            abort(400, message="Abbreviations not in the correct format")        

        try:
            abbrev = json.loads(s)
        except:
            err = sys.exc_info()[0]
            print(err)
            abort(400, message="Abbreviations not in the correct format")

        nameSet.abbrev = abbrev

        return self.finish(nameSet)

    def delete(self, id):
        """Clears all abbreviations from the name set"""
        context = DataContext()
        if id not in context:
            abort(404, message="'{}' doesn't exist".format(id))

        nameSet = context[id]
        nameSet.abbrev = {}

        return self.finish(nameSet)

