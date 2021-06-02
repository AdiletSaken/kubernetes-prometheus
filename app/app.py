import os
import json

from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

config = {
    'DATABASE_URI': os.environ.get('DATABASE_URI', ''),
    'HOSTNAME': os.environ.get('HOSTNAME', ''),
    'GREETING': os.environ.get('GREETING', 'Hello')
}

app = Flask(__name__)

@app.route('/')
def hello():
    return config['GREETING'] + ' from ' + config['HOSTNAME'] + '!'

@app.route('/config')
def configuration():
    return json.dumps(config)

app.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE_URI']

db = SQLAlchemy(app)

class Student(db.Model):
   __tablename__ = "students"
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(20))

   def create(self):
       db.session.add(self)
       db.session.commit()
       return self

   def __init__(self, name):
       self.name = name

   def __repr__(self):
       return f"{self.id}"

db.create_all()

class StudentSchema(ModelSchema):
   class Meta(ModelSchema.Meta):
       model = Student
       sqla_session = db.session
   id = fields.Integer(dump_only=True)
   name = fields.String(required=True)

@app.route('/student', methods=['POST'])
def create_student():
   data = request.get_json()
   student_schema = StudentSchema()
   student = student_schema.load(data)
   result = student_schema.dump(student.create())
   return make_response(jsonify({"student": result}))

@app.route('/student', methods=['GET'])
def index():
   get_students = Student.query.all()
   student_schema = StudentSchema(many=True)
   students = student_schema.dump(get_students)
   return make_response(jsonify({"students": students}))

@app.route('/student/<id>', methods=['GET'])
def get_student_by_id(id):
   get_student = Student.query.get(id)
   student_schema = StudentSchema()
   student = student_schema.dump(get_student)
   return make_response(jsonify({"student": student}))

@app.route('/student/<id>', methods=['PUT'])
def update_student_by_id(id):
   data = request.get_json()
   get_student = Student.query.get(id)
   if data.get('name'):
       get_student.name = data['name']
   db.session.add(get_student)
   db.session.commit()
   student_schema = StudentSchema(only=['id', 'name'])
   student = student_schema.dump(get_student)
   return make_response(jsonify({"student": student}))

@app.route('/student/<id>', methods=['DELETE'])
def delete_student_by_id(id):
   get_student = Student.query.get(id)
   db.session.delete(get_student)
   db.session.commit()
   return make_response("")

@app.route('/metrics')
def metrics():
    from prometheus_client import generate_latest
    return generate_latest()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80', debug=True)
