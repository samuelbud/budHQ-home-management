from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    assignee = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    done = db.Column(db.Boolean, default=False)
    is_done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.id} {self.assignee}>'


def create_tables():
    with app.app_context():
        db.create_all()


create_tables()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        task_content = request.form['content']
        priority = request.form['priority']
        new_task = Todo(content=task_content, assignee=request.form['assigned_to'], priority=request.form['priority'])

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There is an issue adding your task right now, Ela. Sam is working on it.'
    else:
        tasks = Todo.query.filter_by(done=False).order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There is an issue deleting your task right now, Ela. Sam is working on it.'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    try:
        task = Todo.query.get_or_404(id)
        task.done = request.json['done']
        task.is_done = request.json['done']  # update the is_done attribute

        db.session.commit()

        # Move the task to the "tasks-done" table if it is marked as done and not already in the table
        if task.done and not task.is_done:
            task_row = f"<tr><td>{task.content}</td><td>{task.assignee}</td><td>{task.date_created.date()}</td><td>{task.priority}</td><td><input type='checkbox' id='checkbox_{task.id}' name='done' onclick='taskDone({task.id}, this)' checked></td></tr>"
            script = f"document.getElementById('tasks-done').insertAdjacentHTML('beforeend', '{task_row}');"
            db.session.commit()  # commit the changes after updating the is_done attribute
            return script
        else:
            return ''
    except:
        return 'There is an issue updating your task right now, Ela. Sam is working on it.'



@app.route('/tasks')
def get_tasks():
    tasks = Todo.query.order_by(Todo.date_created).all()
    return {'tasks': [{'id': task.id, 'content': task.content, 'assignee': task.assignee, 'priority': task.priority, 'done': task.done} for task in tasks]}



@app.route('/costs')
def costs():
    return render_template('costs.html')


@app.route('/completed-tasks')
def completed_tasks():
    tasks = Todo.query.filter_by(done=True, is_done=True).order_by(Todo.date_created).all()
    return render_template('completed-tasks.html', tasks=tasks)



if __name__ == '__main__':
    app.run(debug=True)
