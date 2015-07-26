from flask import request
from flask_restful import abort, Resource
from canyonero.nameSet import *

def linkBuilder(baseUri):
    def build(x):
        return {'link': 
             {'href': baseUri + '/{}'.format(x.id),
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
        return [build(x) for x in context]

    def post(self):
        print(request.data)
        abort(400, message="Name set not in the correct format")
