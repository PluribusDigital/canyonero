import os
import canyonero
import canyonero.nameSet as ns

from flask import Flask, send_file, redirect
from flask_restful import Api

class App(object):
    """Represents the Flask App"""
    def __init__(self):
        self.dir = os.path.dirname(__file__)

        self.app = Flask(__name__, static_folder='../app')
        self.api = Api(self.app, prefix='/api/v1')

        self.app.add_url_rule('/bower_components/<path:path>', 'bower_components', self.bower)

        self.api.add_resource(canyonero.Root, '/')
        self.api.add_resource(canyonero.NameSetEndpointIndex, 
                              '/nameset')
        self.api.add_resource(canyonero.NameSetEndpointDetail, 
                              '/nameset/<string:id>')
        self.api.add_resource(canyonero.NameSetEndpointAbbrev, 
                              '/nameset/<string:id>/abbrev')
        self.api.add_resource(canyonero.NameSetEndpointIgnore, 
                              '/nameset/<string:id>/ignore')
        self.api.add_resource(canyonero.NameSetEndpointCanon, 
                              '/nameset/<string:id>/canon')
        self.api.add_resource(canyonero.ClusterEndpointIndex, 
                              '/nameset/<string:id>/cluster')
        self.api.add_resource(canyonero.ClusterEndpointDetail, 
                              '/nameset/<string:id>/cluster/<string:key>')

    def bower(self, path):
        fullPath = os.path.join(self.dir, '../bower_components', path)
        return send_file(fullPath)

    def run(self, debug):
        self.app.run(debug=debug)

    def absoluteUrl(self, relative):
        f = "{0}{1}" if relative[0] == '/' else "{0}/{1}"
        return f.format(self.api.prefix, relative)

