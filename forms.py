from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextField
from wtforms import validators
from wtforms.fields.core import SelectField
from wtforms.validators import InputRequired, Length

class UserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=30, message="Does Not Meet Length Requirements")])

    first_name = StringField("First Name", validators=[InputRequired(), Length(min=1, max=20, message="Does Not Meet Length Requirements")])
    
    last_name = StringField("Last Name", validators=[InputRequired(), Length(min=1, max=20, message="Does Not Meet Length Requirements")])
    
    password = PasswordField("Password", validators=[InputRequired(), Length(min=1, max=30, message="Does Not Meet Length Requirements")])
    
    email = StringField("Email", validators=[InputRequired()])
    

class TodoForm(FlaskForm):
    todo = TextField("To Do", validators=[InputRequired(), Length(min=1, max=200, message="Does Not Meet Length Requirements")])
    
    status = SelectField("Status", choices=[('Complete', 'Complete'), ('In Progress', 'In Progress'), ('Not Started', 'Not Started')])