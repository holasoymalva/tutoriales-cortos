from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=True)
    done = db.Column(db.Boolean, default=False)

    def __init__(self, title, description, done):
        self.title = title
        self.description = description
        self.done = done

    def __repr__(self):
        return '<Task %r>' % self.title

db.create_all()

@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    tasks = Task.query.all()
    return jsonify([task.serialize() for task in tasks])

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    return jsonify(task.serialize())

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    task = Task(title=data['title'], description=data['description'], done=data['done'])
    db.session.add(task)
    db.session.commit()
