


from functools import wraps
from flask_migrate import Migrate

from jinja2 import StrictUndefined

# Password hashing library
from passlib.apps import custom_app_context as pwd_context

# Import Flask web framework
from flask import Flask, render_template, request, flash, redirect, session, g
from flask import url_for, jsonify
from flask_debugtoolbar import DebugToolbarExtension

# Import model.py table definitions
from model import connect_to_db, db, User
# Import helper functions that handles SQLAlchemy queries
import helper_functions

import api_calls
import os

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "helloiamsecret"

app.jinja_env.undefined = StrictUndefined



@app.before_request
def pre_process_all_requests():
    """Setup the request context. Current user info can now be
    accessed globally."""

    user_id = session.get('user_id')  # Get user id from session

    # Grab user's info from DB using the id. Save to g.current_user
    if user_id:
        g.current_user = User.query.get(user_id)
        g.logged_in = True
    else:
        g.logged_in = False
        g.current_user = None

def login_required(f):
    """ Redirects user to login page if trying to access a page that
    requires a logged in user."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.current_user is None:
            # Get url that corresponds back to the login form
            return redirect(url_for('display_homepage', next=request.url))
        return f(*args, **kwargs)
    return decorated_function





@app.route("/")
def display_homepage():
    """ Display homepage with login and registration form. """

    return render_template("homepage.html")


@app.route("/login", methods=['POST'])
def validate_login_info():
    """Form validation regarding log in form. Redirects user to dashboard page
    upon successful login."""

    # Get data back from login form
    username = request.form["username"]
    password = request.form["password"]

    # Hash pw
    hash = pwd_context.hash(password)
    verified = pwd_context.verify(password, hash)

    # Check if user in database
    existing_user = helper_functions.check_if_user_exists(username)

    # Form validation error messages
    if not existing_user:
        flash("{} does not exist!".format(username))
        return redirect("/")
    if existing_user.password != password:
        if not verified:
            flash("Incorrect password. Try again.")
            return redirect("/")

    # If successful, add user to session and redirect to dashboard.
    session["user_id"] = existing_user.user_id
    flash("{} has successfully logged in.".format(existing_user.username))
    return redirect("/dashboard")


@app.route("/logout")
def logout_user():
    """Log out user."""

    # Remove user from session when user clicks "logout" link
    del session["user_id"]
    flash("You have logged out.")
    return redirect("/")


@app.route("/register", methods=['POST'])
def process_registration_form():
    """Add user info to database. Upon successful registration, logs user in
    and redirects to dashboard page."""

    # Get form data from registration form
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]

    # Check if username already taken
    username_exists = helper_functions.check_if_user_exists(username)

    if username_exists:
        flash("{} already taken. Try again!".format(username))
        return redirect("/")

    # Add user to DB & session
    new_user = helper_functions.add_user(username, email, password)
    flash("Thanks for registering {}!".format(username))
    session["user_id"] = new_user.user_id

    # Redirect to dashboard with newly logged-in user.
    return redirect("/dashboard")




@app.route("/dashboard")
@login_required

def display_searchbox_and_list():
    """Displays initial dashboard with following features: recipe search form"""

    

    return render_template("search.html")




@app.route("/search.json")
@login_required

def process_recipe_search():
    """Processes recipe search, using Spoonacular API to access data."""

    
    recipe_search = request.args.get("recipe_search")


    results_json = api_calls.recipe_search(recipe_search)

    
    for recipe in results_json['results']:
        recipe_id = str(recipe['id'])

        summary_response = api_calls.summary_info(recipe_id)

        # Store info returned as json and isolate its "summary" info
        summary_json = summary_response
        summary_text = summary_json['summary']

        # Append info to other json's recipes
        recipe['summary'] = summary_text

    # Return json to search-result.js ajax success function
    return jsonify(results_json)



@app.route("/recipe-info/<recipe_id>")
@login_required

def display_recipe_info(recipe_id):
    """ Display detailed recipe info upon clicking on link. """

    # Call recipe info API
    recipe_info_json = api_calls.recipe_info(recipe_id)

    # Unpack json
    title = recipe_info_json['title']
    img = recipe_info_json['image']
    ingredients = recipe_info_json['extendedIngredients']  
    cooking_instructions = recipe_info_json['instructions']

    return render_template("recipe_info.html", title=title,
                           img=img, ingredients=ingredients,
                           cooking_instructions=cooking_instructions)




@app.route("/bookmark.json", methods=["POST"])
@login_required

def process_recipe_bookmark_button():
    """Adds bookmark to DB, returning either a success or error message"""

    
    recipe_id = request.form["recipe_id"]

    # Check if recipe in DB. If not, add new recipe to DB.
    current_recipe = helper_functions.check_if_recipe_exists(recipe_id)

    if not current_recipe:
        current_recipe = helper_functions.add_recipe(recipe_id)

    # Check if user already bookmarked recipe. If not, add to DB.
    bookmark_exists = (helper_functions
                       .check_if_bookmark_exists(current_recipe.recipe_id,
                                                 g.current_user.user_id))

    if not bookmark_exists:
        helper_functions.add_bookmark(g.current_user.user_id,
                                      current_recipe.recipe_id)
        # Return success message to bookmark-recipe.js 
        success_message = "This recipe has been bookmarked!"
        return success_message

    # Return error message to bookmark-recipe.js 
    error_message = "You have already bookmarked this recipe."
    return error_message




@app.route("/favorite")
@login_required

def display_profile():
    """Display user profile of username, email, and bookmarked recipes."""

    return render_template("user_profile.html",
                           username=g.current_user.username,
                           email=g.current_user.email,
                           bookmarked_recipes=g.current_user.recipes)


                           
@app.route("/bookmark-display.json")
@login_required

def process_bookmark_images():
    """Get all bookmark images from DB."""
    

    # Extract list of recipes from DB
    bookmarked_recipes = g.current_user.recipes

    # Create dictionary of recipe image links
    bookmark_images = {'images': []}

    for recipe in bookmarked_recipes:
        bookmark_images['images'].append(recipe.img_url)

    print(bookmark_images)

    return jsonify(bookmark_images)

if __name__ == "__main__":
   
    app.debug = True

    connect_to_db(app)

    app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

    port = int(os.environ.get('PORT', 8000))

    app.run(host="localhost", port=port, debug=True)
