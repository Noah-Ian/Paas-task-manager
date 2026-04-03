import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

database_url = os.environ.get('DATABASE_URL', 'sqlite:///tasks.db')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    __tablename__ = 'tasks'
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed   = db.Column(db.Boolean, default=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':          self.id,
            'title':       self.title,
            'description': self.description or '',
            'completed':   self.completed,
            'created_at':  self.created_at.strftime('%b %d, %Y %H:%M')
        }

with app.app_context():
    db.create_all()
    if Task.query.count() == 0:
        samples = [
            Task(title='Set up Railway account',        description='Create account at railway.app and connect GitHub',         completed=True),
            Task(title='Deploy Flask app',              description='Push code to GitHub and link to Railway project',           completed=True),
            Task(title='Configure environment variables', description='Set DATABASE_URL in Railway dashboard',                  completed=False),
            Task(title='Test CRUD operations',          description='Create, read, update and delete tasks via the UI',         completed=False),
            Task(title='Write assignment report',       description='Document deployment process and Railway vs Heroku comparison', completed=False),
        ]
        db.session.add_all(samples)
        db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return jsonify([t.to_dict() for t in tasks])

@app.route('/tasks', methods=['POST'])
def create_task():
    # Accept JSON regardless of Content-Type header
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400
    title = data.get('title', '').strip()
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    task = Task(
        title=title,
        description=data.get('description', '').strip()
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json(force=True, silent=True) or {}
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'completed' in data:
        task.completed = bool(data['completed'])
    db.session.commit()
    return jsonify(task.to_dict())

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Deleted'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)