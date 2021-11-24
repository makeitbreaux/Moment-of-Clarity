from logging import raiseExceptions
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
# db.drop_all()
db.create_all()
db.session.commit()

toolbar = DebugToolbarExtension(app)

### API STUFF
# BASE URL FOR SEARCH  http://www.thecocktaildb.com/api/json/v2/9973533/search.php?s=

    # data = res.json()
    # drink = data["results"][0]
    
    # return drink
# def get_random_drink():
#     strDrinkThumb = request.get_data("strDrinkThumb")
#     res = requests.get(f"{API_BASE_URL}/randomselection.php",
#                        params={
#                            'strDrinkThumb': strDrinkThumb,
#                         })
#     data = res.json()
#     image = data["drinks"][0]["strDrinkThumb"]
#     drinkName = data["drinks"][0]["strDrink"]

#     randomDrink = {'image': image, 'drinkName': drinkName}
    
#     return randomDrink

@app.route('/')
def index_page():
    strDrinkThumb = request.get_data("strDrinkThumb")
    res = requests.get(f"{API_BASE_URL}/randomselection.php",
                       params={
                           'strDrinkThumb': strDrinkThumb,
                        })
    data = res.json()
    image = data["drinks"][0]["strDrinkThumb"]
    drinkName = data["drinks"][0]["strDrink"]

    randomDrink = {'image': image, 'drinkName': drinkName}
    return render_template('index.html', randomDrink=randomDrink)

@app.route('/random_drink', methods=['GET', 'POST'])
def display_random_drink():
    strDrinkThumb = request.get_data("strDrinkThumb")
    res = requests.get(f"{API_BASE_URL}/randomselection.php",
                       params={
                           'strDrinkThumb': strDrinkThumb,
                        })
    data = res.json()
    id = data["drinks"][0]["idDrink"]
    drinkName = data["drinks"][0]["strDrink"]
    tags = data["drinks"][0]["strTags"]
    category = data["drinks"][0]["strCategory"]
    image = data["drinks"][0]["strDrinkThumb"]
    glass = data["drinks"][0]["strGlass"]
    instructions = data["drinks"][0]["strInstructions"]

    ingredients = []
    numIngredients = 15
    for i in range(1, numIngredients):
        ingredient = data["drinks"][0]["strIngredient" + str(i)]
        measure = data["drinks"][0]["strMeasure" + str(i)]
        if (ingredient is not None):
            ingredients.append(measure + " " + ingredient)

    randomDrink = { 'id': id, 'name': drinkName, 'tags':tags, 'category': category, 'image': image, 'glass': glass, 'instructions': instructions, 'ingredients':ingredients}
    return render_template('show_drinks.html', drink=randomDrink, ingredients=ingredients)


# QUERIES API AND RETURNS SPECIFIED INFO
@app.route('/drink', methods=["GET", "POST"])
def get_drink():
    """Return name, tags, and category for specified drink"""
    key = '9973533'
    strDrink = request.form["strDrink"]
    res = requests.get(f"{API_BASE_URL}/search.php?s={strDrink}",
                       params={'key': key, 'strDrink': strDrink})
    data = res.json()
    
    id = data["drinks"][0]["idDrink"]
    drinkName = data["drinks"][0]["strDrink"]
    tags = data["drinks"][0]["strTags"]
    category = data["drinks"][0]["strCategory"]
    image = data["drinks"][0]["strDrinkThumb"]
    glass = data["drinks"][0]["strGlass"]
    instructions = data["drinks"][0]["strInstructions"]

    ingredients = []
    numIngredients = 15
    for i in range(1, numIngredients):
        ingredient = data["drinks"][0]["strIngredient" + str(i)]
        measure = data["drinks"][0]["strMeasure" + str(i)]
        if (ingredient is not None):
            ingredients.append(measure + " " + ingredient)
    
    drink = { 'id': id, 'name': drinkName, 'tags':tags, 'category': category, 'image': image, 'glass': glass, 'instructions': instructions, 'ingredients':ingredients} 
    
    return render_template('show_drinks.html', drink=drink, ingredients=ingredients)


# ****** THESE WERE CREATED WITH ADDING YOUR OWN DRINKS IN MIND, RETURN TO THIS LATER ******


# #THIS CREATE_DRINK ONLY RETURNS JSON
@app.route('/add_drink', methods=["POST"])
def create_drink():
    """Creates a new drink from form data and returns JSON of that created drink"""
    
    name = request.json["name"]
    image = request.json["image"]

    # TODO: add any other drink info you wish to store in DB. use above example as reference
    # TODO: check to see if drink exists by searching by drink `name`
    # TODO: if drink does not exist, then add it to drink table
    # TODO: if drink exists, then get drink id
    # TODO: with drink id, tie it to user id
    # new_drink = Drink(name=name, ingredients=ingredients, image_url=image)
    
    # db.session.add(new_drink)
    # db.session.commit()

    # TODO: create page to show all of the user saved drinks
    # TODO: redirect to page with all of user saved drinks 
    # TODO: handle error
    response_json = jsonify(success=True)
    return (response_json, 201)

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
    form = DrinkAddForm(request.form)
    drinkName = request.form.get("drinkName")
    tags = request.form.get("tags")
    category = request.form.get("category")
    glass = request.form.get("glass")
    instructions = request.form.get("instructions")
    ingredients = request.form.get("ingredients")
    measures = request.form.get("measures")
    imageThumb = request.form.get("imageThumb")

    new_drink = Drink(drinkName=drinkName, tags=tags, category=category, glass=glass, instructions=instructions, ingredients=ingredients, measures=measures, imageThumb=imageThumb)
    
    if request.method == 'POST':
        drinkName = Drink(drinkName=form.drinkName.data)
        tags = Drink(tags=form.tags.data)
        category = Drink(category=form.category.data)
        glass = Drink(glass=form.glass.data)
        instructions = Drink(instructions=form.instructions.data)
        ingredients = Drink(ingredients=form.ingredients.data)
        measures = Drink(measures=form.measures.data)
        imageThumb = Drink(imageThumb=form.imageThumb.data)
        # drinkName = request.form.data
        # tags = request.form.data
        # category = request.form.data
        # glass = request.form.data
        # instructions = request.form.data
        # ingredients = request.form.data
        # measures = request.form.data
        # imageThumb = request.form.data
        
        
        db.session.add(new_drink)
        db.session.commit()
        flash(f"{new_drink} Added")
        return redirect('/')
    else:
        return render_template("add_drink.html", form=form, drinkName=drinkName, tags=tags, category=category, glass=glass, instructions=instructions, ingredients=ingredients, measures = measures, imageThumb=imageThumb)
    
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
