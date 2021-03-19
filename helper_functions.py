

# Import model.py table definitions
from model import connect_to_db, db, User,Recipe,Bookmark


# Password hashing library
from passlib.apps import custom_app_context as pwd_context

# Import file with all the Spoonacular API calls
import api_calls


def check_if_user_exists(username):
    """Checks if user exists in DB. If so, returns instantiated User
    object. Returns none if user not found."""

    return User.query.filter(User.username == username).first()



def check_if_bookmark_exists(recipe_id, user_id):
    """Check if bookmark exists in DB. If so, returns instantiated Bookmark
    object. Returns none if bookmark not found."""

    return Bookmark.query.filter((Bookmark.recipe_id == recipe_id) &
                                 (Bookmark.user_id == user_id)).first()

  
def check_if_recipe_exists(recipe_id):
    """Check if recipe exists in DB. If so, returns instantiated Recipe object.
    Returns none if recipe not found."""

    return Recipe.query.filter(Recipe.recipe_id == recipe_id).first()


def check_if_ingredient_exists(ingredient_id):
    """Check if ingredient exists in DB. If so, returns instantiated Ingredient
    object. Returns none if ingredient not found."""

    return Ingredient.query.filter(Ingredient.ing_id == ingredient_id).first()





def add_user(username, email, password):
    """Adds user to Users table in DB. Returns instantiated user object."""

    # Hash pw
    hash = pwd_context.hash(password)

    new_user = User(username=username, email=email, password=hash)
    db.session.add(new_user)
    db.session.commit()

    return new_user




def add_recipe(recipe_id):
    """ Adds recipe to Recipes table, which also populates the following
    tables: Ingredient, Aisle, Cuisine, RecipeIngredient. Returns new Recipe
    object back to server."""

    # Get info from API and store as json
    info_response = api_calls.recipe_info(recipe_id)

    # Add new recipe to DB
    new_recipe = Recipe(recipe_id=recipe_id,
                        recipe_name=info_response['title'],
                        img_url=info_response['image'],
                        instructions=info_response['instructions'])

    db.session.add(new_recipe)
    db.session.commit()

    # Isolate ingredients and cuisine info from dict to be added to DB.
    ingredients_info = info_response['extendedIngredients']
    # add_ingredients(recipe_id, ingredients_info)

    

    return new_recipe






def add_bookmark(user_id, recipe_id):
    """Adds recipe to Bookmarks table. Returns instantiated Bookmark object."""

    new_bookmark = Bookmark(user_id=user_id, recipe_id=recipe_id)

    db.session.add(new_bookmark)
    db.session.commit()

    return new_bookmark


