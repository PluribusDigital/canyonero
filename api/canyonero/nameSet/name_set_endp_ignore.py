import json
from flask import request
from flask_restful import abort, Resource
from canyonero.nameSet import *

class NameSetEndpointIgnore(Resource):
    """ Provides the endpoint for the tokens to ignore for one name set
    """

    # -------------------------------------------------------------------------
    # HTTP Methods
    # -------------------------------------------------------------------------

    def get(self, id):
        """Lists all of the tokens to ignore in the name set"""
        context = DataContext()
        if id not in context:
            abort(404, message="'{}' doesn't exist".format(id))

        nameSet = context[id]
        return nameSet.ignore, 200

    def put(self, id):
        """Updates the whole list of tokens to ignore"""
        context = DataContext()
        if id not in context:
            abort(404, message="'{}' doesn't exist".format(id))

        nameSet = context[id]

        if not request.data:
            abort(400, message="Ignore list not in the correct format")        

        s = request.data.decode('utf-8') if request.data else '[]'
        if s[0] != '[':
            abort(400, message="Ignore list not in the correct format")        

        try:
            ignore = json.loads(s)
        except:
            err = sys.exc_info()[0]
            print(err)
            abort(400, message="Ignore list not in the correct format")

        nameSet.ignore = ignore

        return '', 204 if NameSetEndpointDetail.checkRecalc(nameSet) else 205

    def delete(self, id):
        """Clears all ignore tokens from the name set"""
        context = DataContext()
        if id not in context:
            abort(404, message="'{}' doesn't exist".format(id))

        nameSet = context[id]
        nameSet.ignore = []

        return '', 204 if NameSetEndpointDetail.checkRecalc(nameSet) else 205

