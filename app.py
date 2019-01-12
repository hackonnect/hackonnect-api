from flask import Flask, render_template, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

intro_dict = {'data1': 'value1', 'data2': 'value2', 'data3': 'value3'}

class Intro2Get(Resource):
    def get(self):
        return intro_dict

class Intro2GetWithId(Resource):
    def get(self, data):
        return {data: intro_dict[data]}

api.add_resource(Intro2Get, '/get')
api.add_resource(Intro2GetWithId, '/get/<string:data>')

class Intro2Post(Resource):
    def post(self, data):
        if data in intro_dict:
            return {'message': 'Data Key already exists.'}
        intro_dict[data] = request.form['data']
        return {data: intro_dict[data]}

api.add_resource(Intro2Post, '/post/<string:data>')

class Intro2Put(Resource):
    def put(self, data):
        intro_dict[data] = request.form['data']
        return {data: intro_dict[data]}
        
api.add_resource(Intro2Put, '/put/<string:data>')

@app.route('/')
def index():
    return render_template('index.html', intro_dict=intro_dict)