from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# initial value
intro2get = {'data1': 'value1', 'data2': 'value2', 'data3': 'value3'}

class Intro2Get(Resource):
    def get(self):
        return intro2get

class Intro2GetWithId(Resource):
    def get(self, data_name):
        return {data_name: intro2get[data]}

api.add_resource(Intro2Get, '/get')
api.add_resource(Intro2GetWithId, '/get/<string:data_name>')

