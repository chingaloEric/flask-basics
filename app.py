from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Task %r>' % self.id

# Hanlder for index
@app.route('/', methods = ['GET', 'POST'])
def index():
    # to check for the http Method:
    if request.method == 'POST':
        # get task content from
        task_content = request.form['content']

        # make a Todo Object
        task = Todo(content = task_content)
  
        # saving into database
        try:
            db.session.add(task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Failure Occured'
        
    else:
        # to get all the tasks from database
        tasks = Todo.query.order_by(Todo.created).all()
        # to pass the tasks to the template
        return render_template('index.html', tasks = tasks)

# Handler for delete  
@app.route('/delete/<int:id>')
def delete(id):
    # to query the todo
    task = Todo.query.get_or_404(id)

    # deelting a todo
    try:
        db.session.delete(task)
        db.session.commit()
        # redirect to main
        return redirect('/')
    except:
        return 'There was Nothing to delete'

# Handler for update
@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        # making the updates
        task.content = request.form['content']

        # commit changes to database
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Failed to update'
    else:
        return render_template('update.html', task=task)


# main function
if __name__ == '__main__':
    app.run(debug=True)