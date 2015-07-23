import canyonero

from flask import Flask
from flask_restful import Api

class App(object):
    """Represents the Flask App"""
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)

        self.api.add_resource(canyonero.Sponge, '/', '/<string:id>')

    def run(self, debug):
        self.app.run()


