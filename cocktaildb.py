import requests

key = '9973533'

response = requests.get("http://www.thecocktaildb.com/api/json/v2/{key}/search.php?s={strDrink}",
                        params={'key': key, 'strDrink': 'Lemon Elderflower Spritzer'})