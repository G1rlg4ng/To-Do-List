from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate

app = Flask(__name__)

#///relative path, ////absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db' #Configures the database connection located in tasks.db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Disables modification tracking

db = SQLAlchemy(app)
#migrate = Migrate(app, db)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)
    complete = db.Column(db.Boolean)
    scheduled_time = db.Column(db.DateTime)
    # reminder_sent = db.Column(db.Boolean, default=False)
    # emoji = db.Column(db.string(255))
    
# A function to initialize the database within the application context
def initialize_database():
    with app.app_context():
        db.create_all()

#Home page to list all the todos
@app.route("/")
def home():
    todo_list = Task.query.all()
    return render_template("base.html", todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task")
    scheduled_time_str = request.form.get("scheduled_time") # Get scheduled time as string
    
    if task and scheduled_time_str:
        # Parse the scheduled_time string and convert it to a datetime object
        scheduled_time = datetime.strptime(scheduled_time_str, "%Y-%m-%dT%H:%M")
         
        new_todo = Task(task=task, complete = False, scheduled_time=scheduled_time)
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for("home"))

# Update route toggles the completion status of a task 
@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo=Task.query.filter_by(id=todo_id).first() #Database query
    
    # This line toggles the complete attribute of the selected task. 
    # If it was True, it becomes False, and vice versa.
    todo.complete = not todo.complete
    
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Task.query.filter_by(id=todo_id).first()
    
    #Delete selected task from the database
    db.session.delete(todo)
    
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    initialize_database()  # Call the function to initialize the database
    app.run(debug=True)
