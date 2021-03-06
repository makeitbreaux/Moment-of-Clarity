from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, TextField
# from wtforms import validators
# from wtforms.fields.core import SelectField
from wtforms.fields.html5 import IntegerField, URLField, EmailField
from wtforms.validators import InputRequired, Length, DataRequired

class UserAddForm(FlaskForm):
    """Form for adding users."""
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=30, message="Does Not Meet Length Requirements")])

    first_name = StringField("First Name", validators=[InputRequired(), Length(min=1, max=20, message="Does Not Meet Length Requirements")])
    
    last_name = StringField("Last Name", validators=[InputRequired(), Length(min=1, max=20, message="Does Not Meet Length Requirements")])
    
    password = PasswordField("Password", validators=[InputRequired(), Length(min=1, max=30, message="Does Not Meet Length Requirements")])
    
    email = EmailField("Email", validators=[InputRequired()])
    
class UserEditForm(FlaskForm):
    """Form for editing users."""
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=30, message="Does Not Meet Length Requirements")])

    first_name = StringField("First Name", validators=[InputRequired(), Length(min=1, max=20, message="Does Not Meet Length Requirements")])
    
    last_name = StringField("Last Name", validators=[InputRequired(), Length(min=1, max=20, message="Does Not Meet Length Requirements")])
    
    password = PasswordField("Password", validators=[InputRequired(), Length(min=1, max=30, message="Does Not Meet Length Requirements")])
    
    email = StringField("Email", validators=[DataRequired()])

# NEED TO FIGURE OUT HOW TO ADD USER_ID WHEN DRINKS ARE ADDED
class DrinkAddForm(FlaskForm):
    """Form for adding drinks."""
    drink_name = StringField("Name", validators=[DataRequired()])
    
    tags = StringField("Tags")
    
    category = StringField("Category")
    
    glass = StringField("Glass")
    
    instructions = TextAreaField("Instructions", validators=[InputRequired(), Length(min=1, max=1000)])
    
    ingredients = TextAreaField("Ingredients", validators=[InputRequired(), Length(min=1, max=500)])
    
    measures = TextAreaField("Measures", validators=[InputRequired(), Length(min=1, max=500)])
    
    image_thumb = URLField('(Optional) Image URL')

class DrinkEditForm(FlaskForm):
    """Form for adding drinks."""
    drink_name = StringField("Name", validators=[DataRequired()])
    
    tags = StringField("Tags")
    
    category = StringField("Category")
    
    glass = StringField("Glass")
    
    instructions = StringField("Instructions", validators=[DataRequired()])
    
    ingredients = TextAreaField("Ingredients", validators=[InputRequired(), Length(min=1, max=500)])
    
    measures = TextAreaField("Measures", validators=[InputRequired(), Length(min=1, max=500)])
    
    image_thumb = StringField('(Optional) Image URL')

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    
    password = PasswordField('Password', validators=[Length(min=4)]) 