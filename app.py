from logging import raiseExceptions
from re import template
from flask import Flask, render_template, redirect, session, flash, jsonify, g, request
import requests
from flask_debugtoolbar import DebugToolbarExtension
from models import Drink, connect_db, db, User, Drink
from forms import UserAddForm, DrinkAddForm, DrinkEditForm, LoginForm, UserEditForm
from sqlalchemy.exc import IntegrityError
from alcoholic import alcoholicIngredients
# from secrets import API_SECRET_KEY

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///drinks"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

CURR_USER_KEY = "curr_user"
API_BASE_URL = "http://www.thecocktaildb.com/api/json/v2/9973533"
toolbar = DebugToolbarExtension(app)
database = "postgresql:///drinks"

connect_db(app)
db.create_all()
db.session.commit()


def serialize(self):
        """Returns a dict representation of drink which we can turn into JSON"""
        return {
            'id': self.id,
            'drinkName': self.drinkName,
            'category' : self.category,
            'glass' : self.glass,
            'instructions': self.instructions,
            'ingredients': self.ingredients,
            'measures': self.measures,
            'imageThumb': self.imageThumb
        }
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
        drinkName = drink["strDrink"]
        randomDrink = {'image': image, 'drinkName': drinkName}
        return randomDrink
    randomDrinks = list(map(transformDrinks, data["drinks"]))
    print(randomDrinks)
    return render_template('index.html', randomDrinks=randomDrinks)

@app.route('/drink', methods=["POST"])
def get_drink_form():
    drinkName = request.form['strDrink']
    return redirect(f"/drink/{drinkName}")

@app.route('/drink/<string:drinkName>', methods=["GET"])
def get_drink(drinkName):
    """Returns all information for specified drink, filters out alcoholic ingredients, displays information on a page."""
    key = '9973533'
    res = requests.get(f"{API_BASE_URL}/search.php?s={drinkName}",
                       params={'key': key, 'strDrink': drinkName})
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

    def determine_alcoholic(ingredient):
        return any(alcoholicIngredient['ingredient'] == ingredient for alcoholicIngredient in alcoholicIngredients)

    for i in range(1, numIngredients):
        ingredient = data["drinks"][0]["strIngredient" + str(i)]
        measure = data["drinks"][0]["strMeasure" + str(i)]
        if (ingredient is not None):
            isAlcoholic = determine_alcoholic(ingredient)
            if (not isAlcoholic):
                ingredients.append(f"{measure or ''} {ingredient}")
        drink = { 'id': id, 'name': drinkName, 'tags':tags, 'category': category, 'image': image, 'glass': glass, 'instructions': instructions, 'ingredients':ingredients} 
           
    return render_template('show_drinks.html', drink=drink, ingredients=ingredients)

# THIS MAY BE USED TO DISPLAY DRINKS IN DATABASE
# drinks = Drink.query.order_by(Post.created_at.desc()).limit(5).all()
    
# CHANGE THIS TO HANDLE SHOW_DRINK BUTTON
@app.route('/recipes', methods=["GET"])
def show_saved_drinks():
    """Shows drinks saved in DB."""
    # TODO: create page to show all of the user saved drinks
    # TODO: redirect to page with all of user saved drinks  

 
    drinks = Drink.query.all()

 
    return render_template("recipes.html", drinks=drinks)

@app.route('/add_drink', methods=["GET", "POST"])
def add_drink():
    """Using form found in navbar, user enters info into DrinkAddForm and submits a drink to DB."""
    
    # TODO: check to see if drink exists by searching by drink `name`
    # TODO: if drink does not exist, then add it to drink table
    # TODO: if drink exists, then get drink id
    # TODO: with drink id, tie it to user id

    # TODO: handle error
    
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
    # TRYING TO CHECK DB FOR DUPLICATE DRINKS
    def check_db():
        drinks = Drink.query.all()
        for drinkName in drinks:
            check_db(drinks)
            if (drinkName in drinks):
                print("Drink already exists!")
        
    
    if request.method == 'POST':
        drinkName = Drink(drinkName=form.drinkName.data)
        tags = Drink(tags=form.tags.data)
        category = Drink(category=form.category.data)
        glass = Drink(glass=form.glass.data)
        instructions = Drink(instructions=form.instructions.data)
        ingredients = Drink(ingredients=form.ingredients.data)
        measures = Drink(measures=form.measures.data)
        imageThumb = Drink(imageThumb=form.imageThumb.data)
        
        db.session.add(new_drink)
        db.session.commit()
        flash(f"{new_drink.drinkName} Added to Recipes")
        return redirect("/saved_drinks")
    else:
        return render_template("add_drink.html", form=form, drinkName=drinkName, tags=tags, category=category, glass=glass, instructions=instructions, ingredients=ingredients, measures = measures, imageThumb=imageThumb)


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
            return render_template('register.html', form=form)
        session['user_id'] = new_user.id
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect('/')

    return render_template('users/register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """Logs a user in."""
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
    return render_template('users/login.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/login")

############################################################
# USER SHOW, EDIT, DELETE
@app.route('/users')
def list_users():
    """Page with listing of users.

    Can take a 'q' param in querystring to search by that username.
    """

    search = request.args.get('q')

    if not search:
        users = User.query.all()
    else:
        users = User.query.filter(User.username.like(f"%{search}%")).all()

    return render_template('users/index.html', users=users)

@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show user profile."""

    user = User.query.get_or_404(user_id)

    return render_template('users/show.html', user=user)

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
            user.password = form.password.data
            user.email = form.email.data
          
            db.session.commit()
            return redirect(f"/users/{user.id}")

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