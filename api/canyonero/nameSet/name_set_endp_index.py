import sys
import datetime
import json
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

    # -------------------------------------------------------------------------
    # POST helpers
    # -------------------------------------------------------------------------

    def defaultTitle(self):
        stamp = datetime.datetime.today()
        return 'Set ' + stamp.strftime("%B %d, %Y %I:%M%p")

    def parse(self, encoded):
        if not encoded:
            return None
        
        s = encoded.decode('utf-8')

        if s[0] == '[':
            return self.parseFromList(s)
        elif s[0] == '{':
            return self.parseFromNameset(s)
        return None

    def parseFromList(self, s):
        try:
            result = json.loads(s)
            title = self.defaultTitle()
            return NameSet(title, result)
        except:
            err = sys.exc_info()[0]
            print(err)

    def parseFromNameset(self, s):
        try:
            o = json.loads(s)
            if 'names' not in o:
                return None

            title = o['title'] if 'abbrev' in o else self.defaultTitle()
            ns = NameSet(title, o['names'])
            if 'abbrev' in o:
                ns.abbrev = o['abbrev']
            if 'ignore' in o:
                ns.ignore = o['ignore']
            return ns
        except:
            err = sys.exc_info()[0]
            print(err)        

    # -------------------------------------------------------------------------
    # HTTP Methods
    # -------------------------------------------------------------------------

    def get(self):
        """Returns a lists of all available name sets"""
        context = DataContext()
        build = linkBuilder(request.base_url)
        return [build(x) for x in context]

    def post(self):
        """Adds a new name set to the list
        Returns the new id and a link record
        """
        ns = self.parse(request.data)
        if not ns:
            abort(400, message="Name set not in the correct format")

        # build the clusters
        ns.buildClusters()

        # save to the database
        context = DataContext()
        context[ns.id] = ns

        # return the ID and the link to this name set
        result = linkBuilder(request.base_url)(ns)
        result.update({'id': ns.id})
        return result, 201
