from re import template
from flask import Flask, render_template, redirect, session, flash, jsonify, g, request
import requests
from flask_debugtoolbar import DebugToolbarExtension
from models import Drink, connect_db, db, User, Drink
from forms import UserAddForm, DrinkAddForm, DrinkEditForm, LoginForm
from sqlalchemy.exc import IntegrityError
# from secrets import API_SECRET_KEY

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///drinks"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

CURR_USER_KEY = "curr_user"

API_BASE_URL = "http://www.thecocktaildb.com/api/json/v2/9973533"

connect_db(app)
db.drop_all()
db.create_all()
db.session.commit()

toolbar = DebugToolbarExtension(app)

### API STUFF
# BASE URL FOR SEARCH  http://www.thecocktaildb.com/api/json/v2/9973533/search.php?s=

    # data = res.json()
    # drink = data["results"][0]
    
    # return drink

@app.route('/')
def index_page():
    drinks = Drink.query.all()
    return render_template('index.html', drinks=drinks)

# QUERIES API AND RETURNS SPECIFIED INFO
@app.route('/drink', methods=["GET", "POST"])
def get_drink():
    """Return name, tags, and category for specified drink"""
    key = '9973533'
    name = request.form["name"]
    res = requests.get(f"{API_BASE_URL}/search.php?s={name}",
                       params={'key': key, 'strDrink': name})
    data = res.json()
    
    id = data["drinks"][0]["idDrink"]
    drinkName = data["drinks"][0]["strDrink"]
    tags = data["drinks"][0]["strTags"]
    category = data["drinks"][0]["strCategory"]
    image = data["drinks"][0]["strDrinkThumb"]
    glass = data["drinks"][0]["strGlass"]
    instructions = data["drinks"][0]["strInstructions"]

    ingredient1 = data["drinks"][0]["strIngredient1"]
    ingredient2 = data["drinks"][0]["strIngredient2"]
    ingredient3 = data["drinks"][0]["strIngredient3"]
    ingredient4 = data["drinks"][0]["strIngredient4"]
    ingredient5 = data["drinks"][0]["strIngredient5"]
    ingredient6 = data["drinks"][0]["strIngredient6"]
    ingredient7 = data["drinks"][0]["strIngredient7"]
    ingredient8 = data["drinks"][0]["strIngredient8"]
    ingredient9 = data["drinks"][0]["strIngredient9"]
    ingredient10 = data["drinks"][0]["strIngredient10"]
    ingredient11 = data["drinks"][0]["strIngredient11"]
    ingredient12 = data["drinks"][0]["strIngredient12"]
    ingredient13 = data["drinks"][0]["strIngredient13"]
    ingredient14 = data["drinks"][0]["strIngredient14"]
    ingredient15 = data["drinks"][0]["strIngredient15"]
   
    measure1 = data["drinks"][0]["strMeasure1"]
    measure2 = data["drinks"][0]["strMeasure2"]
    measure3 = data["drinks"][0]["strMeasure3"]
    measure4 = data["drinks"][0]["strMeasure4"]
    measure5 = data["drinks"][0]["strMeasure5"]
    measure6 = data["drinks"][0]["strMeasure6"]
    measure7 = data["drinks"][0]["strMeasure7"]
    measure8 = data["drinks"][0]["strMeasure8"]
    measure9 = data["drinks"][0]["strMeasure9"]
    measure10 = data["drinks"][0]["strMeasure10"]
    measure11 = data["drinks"][0]["strMeasure11"]
    measure12 = data["drinks"][0]["strMeasure12"]
    measure13 = data["drinks"][0]["strMeasure13"]
    measure14 = data["drinks"][0]["strMeasure14"]
    measure15 = data["drinks"][0]["strMeasure15"]
    
    measures = { measure1: measure1, measure2: measure2, measure3: measure3, measure4: measure4, measure5: measure5, measure6: measure6, measure7: measure7, measure8: measure8, measure9: measure9, measure10: measure10, measure11: measure11, measure12: measure12, measure13: measure13, measure14: measure14, measure15: measure15 }
    
   
    ingredients = { ingredient1: ingredient1, ingredient2: ingredient2, ingredient3: ingredient3, ingredient4: ingredient4, ingredient5: ingredient5, ingredient6: ingredient6, ingredient7: ingredient7, ingredient8: ingredient8, ingredient9: ingredient9, ingredient10: ingredient10, ingredient11: ingredient11, ingredient12: ingredient12, ingredient13: ingredient13, ingredient14: ingredient14, ingredient15: ingredient15 } 

    drink = {'id': id, 'name': drinkName, 'tags':tags, 'category': category, 'image': image, 'glass': glass, 'instructions': instructions}
 
    return render_template('show_drinks.html', drink=drink, ingredients=ingredients, measures=measures)

# ****** THESE WERE CREATED WITH ADDING YOUR OWN DRINKS IN MIND, RETURN TO THIS LATER ******
# @app.route('/api/drinks')
# def list_all_drinks():
#     """Return JSON w/ all drinks"""

#     all_drinks = [drink.serialize() for drink in Drink.query.all()]
#     return jsonify(drinks=all_drinks)

# @app.route('/api/drinks/<int:id>')
# def get_drink(id):
#     """Returns JSON for one drink in particular"""
#     drink = Drink.query.get_or_404(id)
#     return jsonify(drink=drink.serialize())

# #THIS CREATE_DRINK ONLY RETURNS JSON
# @app.route('/drink', methods=["GET", "POST"])
# def create_drink():
#     """Creates a new drink from form data and returns JSON of that created drink"""
    
#     name = request.json["name"]
#     ingredients = request.json["ingredients"]
#     image_url = request.json["image_url"]
    
#     new_drink = Drink(name=name, ingredients=ingredients, image_url=image_url)
    
#     db.session.add(new_drink)
#     db.session.commit()

#     response_json = jsonify(drink=new_drink.serialize())
#     return (response_json, 201)

#     # return render_template("add_drink.html")

# @app.route('/api/drinks/<int:id>', methods=["PATCH"])
# def update_drink(id):
#     """Updates a particular drink and responds w/ JSON of that updated drink"""
#     drink = Drink.query.get_or_404(id)
#     # MAY NEED FORM TO EDIT DRINK, HAVE TO CHANGE THIS CODE
#     # form = DrinkEditForm(obj=drink)
#     drink.name = request.json.get('name', drink.name)
#     drink.ingredients = request.json.get('ingredients', drink.ingredients)
#     drink.image = request.json.get('image', drink.image)
#     db.session.commit()
#     return jsonify(drink=drink.serialize())

# @app.route('/api/drinks/<int:id>', methods=["DELETE"])
# def delete_drink(id):
#     """Deletes a particular drink"""
#     drink = Drink.query.get_or_404(id)
#     db.session.delete(drink)
#     db.session.commit()
#     return jsonify(message="deleted")

# # THIS CREATE_DRINK WAS CREATED TO ADD YOUR OWN DRINK TO DB, NEED TO ADJUST
@app.route('/add_drink', methods=["GET", "POST"])
def add_drink():
    form = DrinkAddForm(obj=Drink)
    drinkName = db.session.query(Drink.drinkName)
    tags = db.session.query(Drink.tags)
    category = db.session.query(Drink.category)
    glass = db.session.query(Drink.glass)
    instructions = db.session.query(Drink.instructions)
    ingredients = db.session.query(Drink.ingredients)
    measures = db.session.query(Drink.measures)
    imageThumb = db.session.query(Drink.imageThumb)
    user_id = db.session.query(Drink.user_id)

    new_drink = Drink(drinkName=drinkName, tags=tags, category=category, glass=glass, instructions=instructions, ingredients=ingredients, measures=measures, imageThumb=imageThumb, user_id=user_id)
    
    if form.validate_on_submit():
        Drink.drinkName = form.drinkName.data
        Drink.tags = form.tags.data
        Drink.category = form.category.data
        Drink.glass = form.glass.data
        Drink.instructions = form.instructions.data
        Drink.ingredients = form.ingredients.data
        Drink.measures = form.measures.data
        Drink.imageThumb = form.imageThumb.data
        Drink.user_id = form.user_id.data
        db.session.add_all(new_drink)
        db.session.commit()
        flash(f"{new_drink} Added")
        return redirect('/drink')
    else:
        return render_template("add_drink.html", form=form, drinkName=drinkName, tags=tags, category=category, glass=glass, instructions=instructions, ingredients=ingredients, measures = measures, imageThumb=imageThumb, user_id=user_id)
    
###############
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
            return render_template('register.html', form=form)
        session['user_id'] = new_user.id
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect('/')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session['user_id'] = user.id
            return redirect('/drinks')
        else:
            form.username.errors = ['Invalid username/password.']
            return redirect('/')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/login")
