from flask import Flask, redirect, url_for, render_template, request
from models import db, User, ToDo
from forms import RegisterForm, LoginForm, ToDoForm, ToDoEditForm
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from datetime import datetime

# Contains the main setup for the app and routes for all pages
# Chris Weber

# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '\x14B~^\x07\xe1\x197\xda\x18\xa6[[\x05\x03QVg\xce%\xb2<\x80\xa4\x00'
app.config['DEBUG'] = True

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db.init_app(app)
db.create_all()

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

# User Loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home Page
@app.route("/")
def home():
    if (current_user.is_authenticated):
        return redirect(url_for('user', username=current_user.username, _external=True, _scheme='http'))
    return render_template('home.html')

# Login Page
@app.route('/login', methods=['GET','POST'])
def login():
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        user = User.query.filter_by(email=loginForm.email.data).first()
        if user and user.password==loginForm.password.data:
            login_user(user)
            return redirect(url_for('user', username=user.username, _external=True, _scheme='http'))
        else:
            return redirect(url_for('login', _external=True, _scheme='http'))
    return render_template('login.html', form=loginForm)

# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    registerForm = RegisterForm()
    if registerForm.validate_on_submit():
        user = User(email=registerForm.email.data, firstName=registerForm.firstName.data, lastName=registerForm.lastName.data, username=registerForm.username.data, password=registerForm.password )
        user.password = registerForm.password.data
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('user', username=user.username, _external=True, _scheme='http'))
    return render_template('register.html', form=registerForm)

# Logout Page
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# User To Do Page
@app.route('/user-<username>', methods=['GET', 'POST'])
def user(username):
    try:
        if (current_user.username != username):
            return redirect(url_for('home'))
    except:
        return redirect(url_for('home'))
    toDoForm = ToDoForm()
    toDos = current_user.toDos
    toDosList = []
    for i in range(len(toDos)):
        for toDo in toDos:
            if toDo.priority==i:
                toDosList.append(toDo)
    if toDoForm.validate_on_submit():
        toDo = ToDo(text=toDoForm.text.data, priority=len(toDosList), dueDate=toDoForm.dueDate.data, user=current_user.id)
        db.session.add(toDo)
        db.session.commit()
        return redirect(url_for('user', username=username))
    if (request.method=="POST"):
        if len(list(request.form.items()))==4: # Edit form was submitted
            for (label, value) in list(request.form.items()):
                if (label=='id'):
                    id = int(value)
                if (label=='priority'):
                    id = int(value)
                if (label=='text'):
                    text = value
                if (label=='dueDate'):
                    date = value
            toDo = ToDo.query.get(id)
            toDo.text = text
            try:
                toDo.dueDate = datetime.strptime(str(date), '%Y-%m-%d').date()
            except:
                toDo.dueDate = None
            db.session.commit()
            return redirect(url_for('user', username=username))
        [(toDoId, action)] = request.form.items()
        toDo = ToDo.query.get(toDoId)
        if (action=="Remove"):
            priority = toDo.priority
            db.session.delete(toDo)
            for toDoLeft in toDos:
                if toDoLeft.priority > priority:
                    toDoLeft.priority = toDoLeft.priority - 1
            db.session.commit()
            return redirect(url_for('user', username=username))
        if (action=="Edit"):
            editForm = ToDoEditForm(id=toDo.id, priority=toDo.priority, text=toDo.text, dueDate=toDo.dueDate)
            return render_template('user.html', form=toDoForm, toDos=toDosList, editToDo=toDo, editForm=editForm)
        if (action=="↑"):
            priority = toDo.priority
            toDo.priority = priority-1
            for otherToDo in toDos:
                if (otherToDo.priority == priority-1) and (otherToDo.id != toDo.id):
                    otherToDo.priority=priority
                    db.session.commit()
                    return redirect(url_for('user', username=username))
        if (action=="↓"):
            priority = toDo.priority
            toDo.priority = priority+1
            for otherToDo in toDos:
                if (otherToDo.priority == priority+1) and (otherToDo.id != toDo.id):
                    otherToDo.priority=priority
                    db.session.commit()
                    return redirect(url_for('user', username=username))
    return render_template('user.html', form=toDoForm, toDos=toDosList, editToDo=None, editForm=None)
