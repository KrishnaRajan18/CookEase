

# Library for API calls
import requests
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv('API_KEY')

headers = { 'x-rapidapi-key': API_KEY,
'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
    
           "Accept": "application/json"}


def recipe_search(recipe_search):
    """Extracts recipe search results from Spoonacular API."""

    # Set up parameters for API call, then call Spoonacular API
    payload = {'query': recipe_search}
    spoonacular_endpoint = 'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/search'
    response = requests.get(spoonacular_endpoint,
                            params=payload,
                            headers=headers)

    return response.json()
def summary_info(recipe_id):
    """Extracts recipe summary from Spoonacular API."""

    # call Spoonacular API, inserting recipe_id into endpoint
    summary_response = (requests.get('https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/'
                                     + recipe_id + '/summary',
                                     headers=headers))

    return summary_response.json()

def recipe_info(recipe_id):
    """Extracts detailed recipe info from Spoonacular API."""

    # Get info from API, inserting recipe_id into endpoint
    info_response = requests.get(
        'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/'
        + recipe_id + '/information', headers=headers)

    return info_response.json()


