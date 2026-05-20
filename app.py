from flask import Flask, render_template, request, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class Todo(db.Model):
    SNo = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime. utcnow)

    def __repr__(self):
        return f"{self.SNo} - {self.title}"

# Create Database
with app.app_context():
    db.create_all()

# Main Route
@app.route("/", methods=['GET', 'POST'])
def hello_world():

    if request.method == "POST":

        title = request.form['title']
        desc = request.form['desc']

        todo = Todo(title=title, desc=desc)

        db.session.add(todo)
        db.session.commit()

    # Always fetch data
    allTodo = Todo.query.all()

    return render_template('index.html',allTodo=allTodo)
@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(SNo=sno).first()
    if todo is None:
        abort(404)

    db.session.delete(todo)
    db.session.commit()
    return redirect('/')



@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):

    todo = Todo.query.filter_by(SNo=sno).first()
    if todo is None:
        abort(404)

    if request.method == 'POST':

        title = request.form['title']
        desc = request.form['desc']

        todo.title = title
        todo.desc = desc

        db.session.commit()

        return redirect('/')

    return render_template('update.html', todo=todo)

if __name__ == "__main__":
    app.run(debug="True")
