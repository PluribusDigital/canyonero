import canyonero
import canyonero.nameSet as ns

from flask import Flask
from flask_restful import Api

class App(object):
    """Represents the Flask App"""
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app, prefix='/api/v1')

        self.api.add_resource(canyonero.Root, '/')
        self.api.add_resource(canyonero.NameSetEndpointIndex, '/nameset')
        self.api.add_resource(canyonero.NameSetEndpointDetail, '/nameset/<string:id>')
        self.api.add_resource(canyonero.NameSetEndpointAbbrev, '/nameset/<string:id>/abbrev')
        self.api.add_resource(canyonero.NameSetEndpointIgnore, '/nameset/<string:id>/ignore')
        self.api.add_resource(canyonero.NameSetEndpointCanon, '/nameset/<string:id>/canon')
        self.api.add_resource(canyonero.ClusterEndpointIndex, '/nameset/<string:id>/cluster')

    def run(self, debug):
        self.app.run(debug=debug)

    def absoluteUrl(self, relative):
        f = "{0}{1}" if relative[0] == '/' else "{0}/{1}"
        return f.format(self.api.prefix, relative)

