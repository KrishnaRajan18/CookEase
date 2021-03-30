
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
import os

db = SQLAlchemy()



class User(db.Model):
    """ User of website. """

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id={} username={} email={} password={}>".format(
            self.user_id, self.username, self.email, self.password)


class Recipe(db.Model):
    """ Recipe in website. """

    __tablename__ = 'recipes'

    # Recipe_id the actual Spoonacular recipe_id; not auto-incrementing
    recipe_id = db.Column(db.String(64), nullable=False, primary_key=True)
    recipe_name = db.Column(db.String(200), nullable=False)
    img_url = db.Column(db.String(1000), nullable=True)
    instructions = db.Column(db.String(10000), nullable=True)

  

    # Define relationship to users (ASSOCIATION)
    users = db.relationship("User",
                            secondary="bookmarks",
                            backref=db.backref("recipes"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return """<Recipe recipe_id={} recipe_name={} img_url={}
                  instructions={}>""".format(self.recipe_id, self.recipe_name,
                                             self.img_url, self.instructions)





class Bookmark(db.Model):
    """ Ingredients of particular recipe / Recipes of particular ingredient. """

    __tablename__ = "bookmarks"

    bookmark_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    recipe_id = db.Column(db.String(64), db.ForeignKey('recipes.recipe_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return """<Bookmark bookmark_id={} user_id={} recipe_id={}>""".format(
            self.bookmark_id, self.user_id, self.recipe_id)



def example_data():
    # Add sample users
    user1 = User(username='krish', email='krish@gmail.com', password='qwert')
    user2 = User(username='rajan', email='rajan@gmail.com', password='qwert1')
    user3 = User(username='gauth', email='gauth@gmail.com', password='qwert2')

    db.session.add_all([user1, user2, user3])
    db.session.commit()

    # Add sample recipes
    recipe1 = Recipe(recipe_id='262682',
                     recipe_name="Thai Sweet Potato Veggie Burgers with Spicy Peanut Sauce",
                     img_url="https://spoonacular.com/recipeImages/262682-556x370.jpg",
                     instructions="Preheat the oven to 350F")
    recipe2 = Recipe(recipe_id='227961',
                     recipe_name="Cajun Spiced Black Bean and Sweet Potato Burgers",
                     img_url="Cajun-Spiced-Blao-Burgers-227961.jpg",
                     instructions='bake it')
    recipe3 = Recipe(recipe_id='602708',
                     recipe_name="Meatless Burgers with Romesco and Arugula",
                     img_url="Meatls-with-Romesco-and-Arugula-602708.jpg",
                     instructions='mix it')

    db.session.add_all([recipe1, recipe2, recipe3])
    db.session.commit()


    # Add sample bookmarks
    bookmark1 = Bookmark(user_id=1, recipe_id='262682')
    bookmark2 = Bookmark(user_id=2, recipe_id='227961')
    bookmark3 = Bookmark(user_id=3, recipe_id='602708')




def connect_to_db(app,db_uri=os.environ.get('DATABASE_URL','postgresql:///recipe')):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','postgresql:///test')
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # Ability to play with table definitions in interactive mode

    from server import app
    connect_to_db(app)
    db.create_all()
    print("Connected to DB.")
