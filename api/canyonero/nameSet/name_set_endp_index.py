from flask import request
from flask_restful import abort, Resource
from canyonero.nameSet import *

def linkBuilder(baseUri):
    def build(i, x):
        return {'link': 
             {'href': request.base_url + '/{}'.format(i),
              'rel': 'item',
              'title': x.title,
              'type': 'application/json'}
             }
    return build

class NameSetEndpointIndex(Resource):
    """ Provides the collection endpoint for all the known name sets
    """

    def get(self):
        context = DataContext()
        build = linkBuilder(request.base_url)
        return [build(i + 1, x) for i, x in enumerate(context)]

    def post(self):
        print(request.data)
        abort(400, message="Name set not in the correct format")
