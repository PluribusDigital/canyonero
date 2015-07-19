from flask import request
from flask_restful import abort, Resource
import canyonero
import json

sponges = {}

class Sponge(Resource):
    """Before loading, the cannon would be cleaned with a wet sponge to extinguish any smouldering material from the last shot
    """
    def get(self, id=None):
        if id and id not in sponges:
            abort(404, message="'{}' doesn't exist".format(id))
        if id:
            return {id: sponges[id]}
        else:
            return json.dumps(sorted(sponges.keys()))

    def put(self, id):
        sponges[id] = json.dumps(request.form)
        return {id: sponges[id]}
