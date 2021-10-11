from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Todo
from forms import UserForm, TodoForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///tbd"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)
# db.drop_all()
db.create_all()
db.session.commit()

toolbar = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        new_user = User.register(username, password, first_name, last_name, email)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('register.html', form=form)
        session['user_id'] = new_user.id
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect('/todos')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session['user_id'] = user.id
            return redirect('/todos')
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_user():
    session.pop('user_id')
    flash("Goodbye!", "info")
    return redirect('/')

@app.route('/todos', methods=['GET', 'POST'])
def show_todos():
    """Show All Todos"""
    if "user_id" not in session:
        flash("Please login first!", "danger")
        return redirect('/')
    form = TodoForm()
    all_todos = Todo.query.all()
    if form.validate_on_submit():
        text = form.todo.data
        new_todo = Todo(text=text, user_id=session['user_id'])
        db.session.add(new_todo)
        db.session.commit()
        flash('Todo Created!', 'success')
        return redirect('/todos')

    return render_template("todos.html", form=form, todos=all_todos)

@app.route('/todos/<int:id>', methods=["POST"])
def delete_todo(id):
    """Delete todo"""
    if 'user_id' not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    todo = Todo.query.get_or_404(id)
    if todo.user_id == session['user_id']:
        db.session.delete(todo)
        db.session.commit()
        flash("Todo deleted!", "info")
        return redirect('/todos')
    flash("You don't have permission to do that!", "danger")
    return redirect('/todos')

@app.route('/todos/<int:id>/edit', methods=["GET", "POST"])
def edit_todos(id):
    todo = Todo.query.get_or_404(id)
    form = TodoForm(obj=todo)
    status = db.session.query(Todo.status)
    form.status.choices = status

    if form.validate_on_submit():
        todo.todo = form.todo.data
        todo.status = form.status.data
        db.session.commit()
        return redirect('/todos')
    else:
        return render_template("edit_todo.html", form=form)