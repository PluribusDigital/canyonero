from flask_restful import Resource
import json

class Root(Resource):
    """ Return the list of available top-level endpoint
    """
    def get(self):
        links = [
            {'Links': 
             {'href': '/nameset/',
              'rel': 'collection',
              'title': 'Name Sets',
              'type': 'text/json'}
             }]
        return json.dumps(links)
