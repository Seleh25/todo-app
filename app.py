# import flask
from crypt import methods
from flask import Flask,render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

# instantiate flask class
app = Flask(__name__)

# instance of DB model
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# creating Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    todo= db.Column(db.String(125), nullable=False)

@app.route('/', methods=['Get' , 'Post'])
def home():
    if request.form:
        #get input from a field name 'todo_input'
        todo_input = request.form.get('todo_input')
        # map the value gotten, to the appropriate field
        todo_item = Todo(todo = todo_input)
        db.session.add(todo_item)  #stages into for commit
        db.session.commit()  #save to DB/ commit to memory
    todos = Todo.query.all()

    return render_template('base.html',  todos=todos)

@app.route('/delete/<int:id>')
def delete(id):
    todo_to_delete = Todo.query.get_or_404(id)
    db.session.delete(todo_to_delete)
    db.session.commit()
    return redirect('/')


@app.route('/update/<int:id>', methods=['Get', 'Post'])
def update(id):
    todo = Todo.query.get_or_404(id)

    if request.method == 'Post':
        todo.input = request.form['todo_input']
        db.session.commit()
        return redirect('/')
    else:
        return render_template('update.html', todo=todo)


@app.route('/about')
def about():
    name = "About"
    return render_template('about.html' , username=name)

@app.route('/contact')
def contact ():
    name = "Contact"
    return render_template('contact.html' , username=name)

@app.route('/services')
def services ():
    name = "Services"
    return render_template('services.html' , username=name)

@app.route('/blog')
def blog ():
    name = "Blog"
    return render_template('blog.html' , username=name)




if __name__ == '__main__':
    app.run(debug=True)
