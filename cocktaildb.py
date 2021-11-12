import requests

key = '9973533'

response = requests.get("http://www.thecocktaildb.com/api/json/v2/1/search.php?s=",
                        params={'key': key, 'strDrink': 'Lemon Elderflower Spritzer'})