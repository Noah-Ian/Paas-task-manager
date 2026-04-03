import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# PostgreSQL from Railway
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------------- MODEL ----------------
class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return render_template("index.html")

# GET ALL TASKS
@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.order_by(Task.created_at.desc()).all()

    return jsonify([
        {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "completed": t.completed,
            "created_at": t.created_at.strftime("%Y-%m-%d %H:%M")
        }
        for t in tasks
    ])

# CREATE TASK
@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    if not data or not data.get("title"):
        return jsonify({"error": "Title required"}), 400

    task = Task(
        title=data["title"],
        description=data.get("description", "")
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({"message": "Task created"}), 201

# UPDATE TASK
@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()

    task.completed = data.get("completed", task.completed)
    db.session.commit()

    return jsonify({"message": "Updated"})

# DELETE TASK
@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = Task.query.get_or_404(id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Deleted"})

# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)