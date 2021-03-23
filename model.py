
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






def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','postgresql:///recipe')
    # app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # Ability to play with table definitions in interactive mode

    from server import app
    connect_to_db(app)
    db.create_all()
    print("Connected to DB.")
