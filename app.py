from flask import Flask, render_template, request
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
db = SQLAlchemy(app)
api = Api(app)

class Database(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    key = db.Column(db.String(120), nullable = False)
    value = db.Column(db.String(120), nullable = False)

db.create_all()
db.session.query(Database).delete()
db.session.commit()
db.session.add(Database(key = 'data1', value = 'value1'))
db.session.add(Database(key = 'data2', value = 'value2'))
db.session.add(Database(key = 'data3', value = 'value3'))
db.session.commit()

class GetAll(Resource):
    def get(self):
        data_all = Database.query.all()
        return_data = {}
        for entry in data_all:
            return_data[entry.key] = entry.value
        return return_data

class Get(Resource):
    def get(self, data):
        data_entry = Database.query.filter_by(key=data).first()
        return {data_entry.key : data_entry.value}

api.add_resource(GetAll, '/get')
api.add_resource(Get, '/get/<string:data>')

class Post(Resource):
    def post(self, data):
        parser = reqparse.RequestParser()
        parser.add_argument(data)
        args = parser.parse_args()
        if Database.query.filter_by(key=data).first():
            return {'error': 'Entry already exists.'}, 404
        new_entry = Database(key = data, value = args[data])
        db.session.add(new_entry)
        db.session.commit()
        return {data: args[data]}

api.add_resource(Post, '/post/<string:data>')

class Put(Resource):
    def put(self, data):
        parser = reqparse.RequestParser()
        parser.add_argument(data)
        args = parser.parse_args()
        data_entry = Database.query.filter_by(key=data).first()
        if not data_entry:
            return {'error': 'Entry does not exist.'}, 404
        data_entry.value = args[data]
        db.session.commit()
        return {data: args[data]}
        
api.add_resource(Put, '/put/<string:data>')

class Delete(Resource):
    def delete(self, data):
        data_entry = Database.query.filter_by(key=data).first()
        if not data_entry:
            return {'error': 'Entry does not exist.'}, 404
        db.session.delete(data_entry)
        data_all = Database.query.all()
        return_data = {}
        for entry in data_all:
            return_data[entry.key] = entry.value
        return return_data

api.add_resource(Delete, '/delete/<string:data>')

@app.route('/')
def index():
    return render_template('index.html', database=Database.query.all())