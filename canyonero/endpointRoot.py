from flask import request
from flask_restful import Resource

class Root(Resource):
    """ Return the list of available top-level endpoint
    """
    def get(self):
        return [
            {'link': 
             {'href': request.base_url + 'nameset',
              'rel': 'collection',
              'title': 'Name Sets',
              'type': 'application/json'}
             }]
