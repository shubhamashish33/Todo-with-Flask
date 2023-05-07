from flask import Flask, jsonify, render_template, request, redirect, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


from config import Config

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "shubham"

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    desc = db.Column(db.String(100))
    taskStatus = db.Column(db.String)

    def __repr__(self):
        return "<Name %r>" % self.title


class TodoForm(FlaskForm):
    taskname = StringField("Enter your Task Name", validators=[DataRequired()])
    taskdesc = StringField("Enter your Task Description", validators=[DataRequired()])
    task_status = StringField("Enter your Task Status", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/task/add", methods=["GET", "POST"])
def add_task():
    db.create_all()
    title = None
    form = TodoForm()
    if title is None:
        task = Todo(
            title=form.taskname.data,
            desc=form.taskdesc.data,
            taskStatus=form.task_status.data,
        )
        db.session.add(task)
        db.session.commit()
    title = form.taskname.data
    form.taskname.data = " "
    form.taskdesc.data = " "
    form.task_status.data = ""
    task_user = Todo.query.all()

    return render_template("add_task.html", form=form, task_user=task_user)





@app.route("/delete/<int:id>")
def delete(id):
    task = Todo.query.filter_by(id=id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect("/")


@app.route("/update/<int:id>")
def update(id):
    task = Todo.query.filter_by(id=id).first()
    if task.taskStatus == "Not Started":
        task.taskStatus = "Pending"
    elif task.taskStatus == "Pending":
        task.taskStatus = "Completed"
    db.session.commit()
    return redirect("/")


@app.route("/")
def home():
    task_user = Todo.query.all()
    return render_template("index.html", task_user=task_user)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
