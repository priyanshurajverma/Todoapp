from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'  # Don't hardcode full path on Render
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    S_NO = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.S_NO} - {self.title}"

# ✅ Ensure DB tables are created even on Render
with app.app_context():
    db.create_all()

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        if title and description:
            todo = Todo(title=title, description=description)
            db.session.add(todo)
            db.session.commit()
    all_todo = Todo.query.all()
    return render_template("index.html", all_todo=all_todo)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/delete/<int:S_NO>")
def delete(S_NO):
    delete_todo = Todo.query.filter_by(S_NO=S_NO).first()
    db.session.delete(delete_todo)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:S_NO>", methods=['GET', 'POST'])
def update(S_NO):
    todo = Todo.query.filter_by(S_NO=S_NO).first()
    if request.method == "POST":
        todo.title = request.form.get("title")
        todo.description = request.form.get("description")
        db.session.commit()
        return redirect("/")
    return render_template("update.html", todo=todo)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
