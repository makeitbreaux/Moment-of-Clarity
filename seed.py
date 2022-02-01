# NEED TO CREATE SEED DATA

from models import Drink, User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

Drink.query.delete()

# Add sample users
maynard_james= User(username="tool1", first_name="Maynard", last_name="Keenan", password="123456", email="mkeenan@gmail.com")

dave_grohl= User(username="foofighter1", first_name="David", last_name="Grohl", password="7891011", email="dgrohl@gmail.com")

shirley_manson= User(username="garbage1", first_name="Shirley", last_name="Manson", password="767689", email="smanson@gmail.com")

db.session.add_all([maynard_james, dave_grohl, shirley_manson])
db.session.commit()

# Add sample drinks 
orange_juice = Drink(drink_name="Orange Juice", tags="summer", category="classic", glass="collins", instructions="juice oranges, add to glass", ingredients="Fresh Oranges", measures="2 oranges")

iced_coffee = Drink(drink_name="Orange Juice", tags="iced", category="classic", glass="collins", instructions="brew coffee, add to glass, add sugar, add cream, add ice", ingredients="Coffee, Sugar, Cream, Ice", measures="1 cup, 2 tbsp, 1 tbsp, 1 cup")

sparkling_water = Drink(drink_name="Coconut Sparkling Water", tags="summer", category="classic", glass="collins", instructions="Pour sparkling water over ice, add coconut essence", ingredients="Sparkling Water, Coconut Essence", measure="1 cup, 2 tbsp")

db.session.add_all([orange_juice, iced_coffee, sparkling_water])
db.session.commit()
