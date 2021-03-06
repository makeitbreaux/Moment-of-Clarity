import os
import re
from logging import raiseExceptions
from re import template
from flask import Flask, render_template, redirect, session, flash, jsonify, g, request
import requests
from flask_debugtoolbar import DebugToolbarExtension
from models import Drink, connect_db, db, User
from forms import UserAddForm, DrinkAddForm, DrinkEditForm, LoginForm, UserEditForm
from sqlalchemy.exc import IntegrityError
from alcoholic import alcoholicIngredients
# from secrets import API_SECRET_KEY

app = Flask(__name__)

uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
# rest of connection code using the connection string `uri`


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'uri', 'postgresql://urjgfrhqkcvgev:8a6a712b66f7bb01f9619561d8eb70ed39803c898c0389783b76b9b46d98dd82@ec2-18-204-101-137.compute-1.amazonaws.com:5432/d1guaubm1orft3')
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///drinks"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
# app.config["SECRET_KEY"] = "abc123"
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'shh')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

CURR_USER_KEY = "user_id" # "curr_user"
API_BASE_URL = "http://www.thecocktaildb.com/api/json/v2/9973533"
toolbar = DebugToolbarExtension(app)
database = "postgresql:///drinks"

connect_db(app)
db.create_all()
db.session.commit()

################################################################
# DISPLAY PAGES, MAKE PAGES FUNCTION
@app.route('/')
def index_page():
    """Displays random drinks in carousel on home page."""
    
    strDrinkThumb = request.get_data("strDrinkThumb")
    res = requests.get(f"{API_BASE_URL}/randomselection.php",
                       params={
                           'strDrinkThumb': strDrinkThumb,
                        })
    data = res.json()
    def transformDrinks(drink):
        image = drink["strDrinkThumb"]
        drink_name = drink["strDrink"]
        randomDrink = {'image': image, 'drink_name': drink_name}
        return randomDrink
    randomDrinks = list(map(transformDrinks, data["drinks"]))
    return render_template('index.html', randomDrinks=randomDrinks)

@app.route('/drink', methods=["POST"])
def get_drink_form():
    drink_name = request.form['strDrink']
    return redirect(f"/drink/{drink_name}")

@app.route('/drink/<string:drink_name>', methods=["GET"])
def get_drink(drink_name):
    """Returns all information for specified drink, filters out alcoholic ingredients, displays information on a page."""
    key = '9973533'
    res = requests.get(f"{API_BASE_URL}/search.php?s={drink_name}",
                       params={'key': key, 'strDrink': drink_name})
    data = res.json()

    id = data["drinks"][0]["idDrink"]
    drink_name = data["drinks"][0]["strDrink"]
    tags = data["drinks"][0]["strTags"]
    category = data["drinks"][0]["strCategory"]
    image = data["drinks"][0]["strDrinkThumb"]
    glass = data["drinks"][0]["strGlass"]
    instructions = data["drinks"][0]["strInstructions"]

    ingredients = []
    numIngredients = 15

    def determine_alcoholic(ingredient):
        return any(alcoholicIngredient['ingredient'].lower() == ingredient.lower() for alcoholicIngredient in alcoholicIngredients)

    for i in range(1, numIngredients):
        ingredient = data["drinks"][0]["strIngredient" + str(i)]
        measure = data["drinks"][0]["strMeasure" + str(i)]
        if (ingredient is not None):
            isAlcoholic = determine_alcoholic(ingredient)
            if (not isAlcoholic):
                ingredients.append(f"{measure or ''} {ingredient}")
        drink = { 'id': id, 'name': drink_name, 'tags':tags, 'category': category, 'image': image, 'glass': glass, 'instructions': instructions, 'ingredients':ingredients} 
            
        return render_template('show_drinks.html', drink=drink, ingredients=ingredients)
    
@app.route('/recipes', methods=["DELETE"])
# I CANNOT SEEM TO GET THIS TO SELECT THE DRINKS PROPERLY IN ORDER TO DELETE THEM
def delete_drink(drink_name):
    """Deletes a particular drink"""
    res = requests('/recipes')
    data = res.json()
    
    id = data["id"]
    if request.method == 'DELETE': 
        # request is from the add_drink button (data from API)

        drink_name = request.json.get("drink_name")
        tags = request.json.get("tags")
        category = request.json.get("category")
        glass = request.json.get("glass")
        instructions = request.json.get("instructions")
        ingredients = request.json.get("ingredients")
        measures = request.json.get("measures")
        imageThumb = request.json.get("image_thumb")
        
        delete_drink = Drink(id = id, user_id=session[CURR_USER_KEY], drink_name=drink_name, tags=tags, category=category, glass=glass, instructions=instructions, ingredients=ingredients, measures=measures, image_thumb=imageThumb)
    
        db.session.delete(delete_drink)
        db.session.commit()
    flash(f"Drink Deleted", "success")
    return redirect('/recipes')
    
@app.route('/recipes', methods=["GET"])
def show_saved_drinks():
    """Shows drinks saved in DB.""" 

    search = request.args.get('drink_name')

    if not search:
        drinks = Drink.query.filter_by(user_id=session[CURR_USER_KEY]).limit(25).all()
    else:
        drinks = Drink.query.filter(Drink.drink_name.like(f"%{search}%")).all()
    return render_template("recipes.html", drinks=drinks)

@app.route('/add_drink', methods=["GET", "POST"])
def add_drink():
    """Using form found in navbar, user enters info into DrinkAddForm and submits a drink to DB. Also handles "Add Drink" button in /show_drinks"""
        
    if request.method == 'GET':
            form = DrinkAddForm(request.form)
            return render_template("add_drink.html", form=form)

    if request.method == 'POST': 
        # request is from the add_drink button (data from API)
        if request.json is not None:
            drink_name = request.json.get("drink_name")
            tags = request.json.get("tags")
            category = request.json.get("category")
            glass = request.json.get("glass")
            instructions = request.json.get("instructions")
            ingredients = request.json.get("ingredients")
            measures = request.json.get("measures")
            imageThumb = request.json.get("image_thumb")

        # request is from the add_drink form (data is manually inputted)
        elif request.form is not None:
            drink_name = request.form.get("drink_name")
            tags = request.form.get("tags")
            category = request.form.get("category")
            glass = request.form.get("glass")
            instructions = request.form.get("instructions")
            ingredients = request.form.get("ingredients")
            measures = request.form.get("measures")
            imageThumb = request.form.get("image_thumb")

        new_drink = Drink(user_id=session[CURR_USER_KEY], drink_name=drink_name, tags=tags, category=category, glass=glass, instructions=instructions, ingredients=ingredients, measures=measures, image_thumb=imageThumb)
        db.session.add(new_drink)
        db.session.commit()
        flash('Drink Added!', "success")
        return redirect('/recipes')

###########################################################
# USER REGISTER, LOGIN, LOGOUT
@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id

def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """Registers a user and authenticates user."""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = UserAddForm()
    
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
            return render_template('users/register.html', form=form)
        do_login(new_user)
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect('/')

    return render_template('users/register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/login")

############################################################
# USER EDIT, DELETE

@app.route('/users/profile', methods=["GET", "POST"])
def edit_profile():
    """Update profile for current user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = g.user
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.email = form.email.data
          
            db.session.commit()
            flash("Profile Changed", 'success')
            return redirect(f"/users/profile")

        flash("Wrong password, please try again.", 'danger')

    return render_template('users/edit_user.html', form=form, user_id=user.id)

@app.route('/users/delete', methods=["POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/register")

@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""

    return render_template('404.html'), 404
