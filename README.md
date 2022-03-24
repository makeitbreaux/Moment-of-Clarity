# Moment of Clarity - Alcohol Free Drinks Guide
A mocktail website that offers alcohol-free alternatives for all of your old alcoholic favorites!

![MoCAnimation](https://user-images.githubusercontent.com/72421941/149238861-2728f484-a2a1-4542-96e8-61718db2e389.gif)

## Description

This is my first capstone project for Springboard's Software Engineering Career Track. The goal of my website is to offer people in sobriety, or people considering sobriety, a guide to alcohol-free mocktails. The sober/sober-curious will be able to type in their old favorite alcoholic drink and be presented with the alcohol-free version. 

## Features

Not logged in, users have access to:

* Search for drinks by name
* Browse a short list of randomnly selected alcohol-free mocktails

Logged in, users have access to the same features, as well as:

* Saving their favorite alcohol free mocktails to their favorites list
* Adding their own alcohol free mocktails to their favorites list
* Removing their favorited drinks

## User Flow

* A user can log in or create a new account; upon successful registration, user is redirected to app index page
* On the index page, a short list of drinks is listed in a carousel and a search box is presented to search specific drinks
* Upon searching a drink or clicking on a random presented drink, the logged in user has the ability to favorite the drink, from here the user can search another drink, go to the index page, or check their favorited drinks
* From the favorited drinks end point, the user can delete the drinks of their choosing
* At any point, using the navigation bar, the user can check their favorited drinks, add a new drink to their favorite, edit or delete their profile, or log out

### API
The data I used was from the [TheCocktailDB](https://www.thecocktaildb.com/api.php?ref=apilist.fun).

## Technologies Used

The main technologies I used to build Moment of Clarity were Python, and I used [Flask](https://github.com/pallets/flask) as a framework, and for the ORM I used[SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy). For the database, I used [PostgreSql](https://github.com/postgres/postgres).

Several Flask extensions were used in creating MoC, including [Flask-SQLAlchemy](https://github.com/pallets/flask-sqlalchemy), [Flask-WTForms](https://github.com/lepture/flask-wtf), and [Flask-Bcrypt](https://github.com/maxcountryman/flask-bcrypt).

## Looking Forward
While the capstone project hit all of the requirements, there are a few more features I'd like to add to enhance the User Experience:
* Google Sign-In Option
* Shop: Users will be able to purchase ingredients for their mocktails online
* Cross-Device Visitor Identification: Users will be able to access their favorite MoC-Tails from all of their devices

