import canyonero
import canyonero.nameSet as ns

from flask import Flask
from flask_restful import Api

class App(object):
    """Represents the Flask App"""
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)

        self.api.add_resource(canyonero.Root, '/')
        self.api.add_resource(canyonero.NameSetEndpointIndex, '/nameset')
        self.api.add_resource(canyonero.NameSetEndpointDetail, '/nameset/<string:id>')
        self.api.add_resource(canyonero.NameSetEndpointCanon, '/nameset/<string:id>/canon')

    def run(self, debug):
        self.app.run(debug=debug)


