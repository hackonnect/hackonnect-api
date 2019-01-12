from flask import Flask, render_template()
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

intro2get = {'data1': 'value1', 'data2': 'value2', 'data3': 'value3'}

class Intro2Get(Resource):
    def get(self):
        return intro2get

class Intro2GetWithId(Resource):
    def get(self, data_name):
        return {data_name: intro2get[data_name]}

api.add_resource(Intro2Get, '/get')
api.add_resource(Intro2GetWithId, '/get/<string:data_name>')

@app.route('/')
def index():
    return render_template('index.html', intro2get=intro2get)