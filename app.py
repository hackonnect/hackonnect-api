from flask import Flask, render_template, request
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
db = SQLAlchemy(app)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('key')
parser.add_argument('value')

class Database(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    key = db.Column(db.String(120), nullable = False)
    value = db.Column(db.String(120), nullable = False)

db.create_all()
db.session.query(Database).delete()
db.session.add(Database(key = 'data1', value = 'value1'))
db.session.add(Database(key = 'data2', value = 'value2'))
db.session.add(Database(key = 'data3', value = 'value3'))
db.session.commit()

class API(Resource):
    def get(self):
        args = parser.parse_args()
        key = args['key']
        if key:
            entry = Database.query.filter_by(key=key).first()
            result = {entry.key, entry.value}
        else:
            database = Database.query.all()
            result = {}
            for entry in database:
                result[entry.key] = entry.value
        return result, 200

    def post(self):
        args = parser.parse_args()
        key, value = args['key'], args['value']
        if Database.query.filter_by(key=key).first():
            return {'error': 'Entry already exists.'}, 404
        entry = Database(key = key, value = value)
        db.session.add(entry)
        db.session.commit()
        result = {key, value}
        return result, 201

    def put(self):
        args = parser.parse_args()
        key, value = args['key'], args['value']
        entry = Database.query.filter_by(key=key).first()
        if not entry:
            return {'error': 'Entry does not exist.'}, 404
        entry.value = value
        db.session.commit()
        result = {key, value}
        return result, 200

    def delete(self):
        args = parser.parse_args()
        key = args['key']
        entry = Database.query.filter_by(key=key).first()
        if not entry:
            return {'error': 'Entry does not exist.'}, 404
        db.session.delete(entry)
        db.session.commit()
        return self.get()

api.add_resource(API, '/api')

@app.route('/')
def index():
    return render_template('index.html', database=Database.query.all())