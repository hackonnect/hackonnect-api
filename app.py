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
    key = db.Column(db.String(120), unique = True, nullable = False)
    value = db.Column(db.String(120), nullable = False)

db.create_all()
for i in range(3):
    db.session.add(Database(key = 'data' + str(i + 1), value = 'value' + str(i + 1)))
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
        data_entry.value = args['value']
        db.session.commit()
        return {data: args[data]}
        
api.add_resource(Put, '/put/<string:data>')

@app.route('/')
def index():
    return render_template('index.html', database=Database.query.all())