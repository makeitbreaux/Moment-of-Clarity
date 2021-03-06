from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
    
 

    
class User(db.Model):
    """User Model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    
    username = db.Column(db.String, 
                         unique=True)
    
    first_name = db.Column(db.String)
    
    last_name = db.Column(db.String)
    
    password = db.Column(db.String)
    
    email = db.Column(db.String)
    
    drinks = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        primary_key=True
    ), db.relationship('Drink', backref="drinks")
    
    @classmethod
    def register(cls, username, password, first_name, last_name, email):
        """Register user w/hashed password & return user."""

        hashed_pwd = bcrypt.generate_password_hash(password).decode("UTF-8")

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            first_name = first_name,
            last_name = last_name
        )

        db.session.add(user)
        return user
        # return instance of user w/username and hashed pwd
        # return cls(username=username, password=hashed_utf8, first_name=first_name, last_name=last_name, email=email)

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


# NEED TO KEEP ID AS ID AND NOT DRINK_ID
class Drink(db.Model):
    """Drinks Model"""
    __tablename__ = 'drinks'

    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id')) 
    
    drink_name = db.Column(db.String)
    
    tags = db.Column(db.String)
    
    category = db.Column(db.String)
    
    glass = db.Column(db.String)
    
    instructions = db.Column(db.String)
    
    ingredients = db.Column(db.String)
    
    measures = db.Column(db.String)
    
    image_thumb = db.Column(db.String)
    
    user = db.relationship('User', backref="drinks")
    
    def serialize(self):
        """Returns a dict representation of drink which we can turn into JSON"""
        return {
            'id': self.id,
            'drinkName': self.drink_name,
            'category' : self.category,
            'glass' : self.glass,
            'instructions': self.instructions,
            'ingredients': self.ingredients,
            'measures': self.measures,
            'imageThumb': self.image_thumb
        }

    def __repr__(self):
        return f"<Drink {self.id}, drinkName={self.drink_name}, category={self.category}, glass={self.glass}, instructions={self.instructions}, ingredients={self.ingredients}, measures={self.measures}, imageThumb={self.image_thumb}>"


