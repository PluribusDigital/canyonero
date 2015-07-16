from flask import Flask
from flask_restful import Api
import canyonero

app = Flask(__name__)
api = Api(app)

api.add_resource(canyonero.Sponge, '/', '/<string:id>')

if __name__ == '__main__':
    app.run(debug=True)
