from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Optional

# Contains class definitions for all forms used
# Chris Weber

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ToDoForm(FlaskForm):
    text = StringField('Add To Do: ', validators=[DataRequired()])
    dueDate = DateField('Due Date (optional): ', validators=[Optional()], format='%Y-%m-%d', render_kw={'placeholder': 'YYYY-MM-DD'})
    submit = SubmitField('Add')

class ToDoEditForm(FlaskForm):
    id = HiddenField('ID')
    priority = HiddenField('priority')
    text = StringField('Edit To Do: ', validators=[DataRequired()])
    dueDate = DateField('Edit Due Date (optional): ', validators=[Optional()], format='%Y-%m-%d', render_kw={'placeholder': 'YYYY-MM-DD'})
    submit = SubmitField('Save')