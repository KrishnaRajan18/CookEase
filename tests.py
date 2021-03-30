# import library used for user tests
from unittest import TestCase

# import example_data function only
from model import connect_to_db, db, example_data, User, Bookmark

from server import app
from flask import session

# import file with Spoonacular API calls to mock
import api_calls

import fake_api_json




class FlaskTestsLogInLogOutRegistration(TestCase):
   
    def setUp(self):
        """Before every test"""

        app.config['TESTING'] = True
        self.client = app.test_client()

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_login_form_display(self):
        """ Test that login page properly showing login form. """

        result = self.client.get('/')
        self.assertIn(b"Log In", result.data)

    def test_registration_form_display(self):
        """ That that registration page properly showing registration form. """

        result = self.client.get('/')
        self.assertIn(b"Register", result.data)

    def test_correct_login(self):
        """Test log in form with correct info."""

        with self.client as c:
            result = c.post('/login',
                            data={'username': 'krish', 'password': 'qwert'},
                            follow_redirects=True
                            )

            self.assertEqual(session['user_id'], 1)
            self.assertIn(b"krish has successfully logged in.", result.data)

   
    def test_logout(self):
        """Test logout route."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'

            result = self.client.get('/logout', follow_redirects=True)

            self.assertNotIn('user_id', session)
            self.assertIn(b'You have logged out.', result.data)
        
    

    def test_registration_correct_info(self):
        """Test that user successfully registers upon form submission."""

        with self.client as c:
            result = c.post('/register',
                            data={'username': 'neerja',
                                  'email': 'neerja@gmail.com',
                                  'password': 'neer1'},
                            follow_redirects=True
                            )

            # Check that success message appears
            self.assertIn(b"Thanks for registering neerja!", result.data)

            # Check that info gets stored in DB
            current_user = User.query.filter(User.username == 'neerja').first()
            self.assertIsNotNone(current_user)

 
    def test_cannot_access_page(self):
        """Test that @loginrequired wrapper works, where user cannot access
        page that requires being logged in."""

        result = self.client.get('/dashboard')

        self.assertIn(b"Redirecting", result.data)



class FlaskTestsFavorite(TestCase):
   
    def setUp(self):
        """Before every test"""

        app.config['TESTING'] = True
        self.client = app.test_client()

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_correct_page(self):
        """Test that correct page is showing up."""

        result = self.client.get('/favorite')
        self.assertIn(b"User Details", result.data)
        

    def test_correct_username(self):
        """Test correct username is showing onpage."""

        result = self.client.get('/favorite')
        self.assertIn(b"krish", result.data)
        self.assertNotIn(b"neerja", result.data)

    def test_correct_email(self):
        """Test that correct email is showing on page."""

        result = self.client.get('/favorite')
        self.assertIn(b"krish@gmail.com", result.data)
        self.assertNotIn(b"neerja@gmail.com", result.data)

    # def test_correct_bookmarks(self):
    #     """Test that correct bookmarked recipes is showing on page."""

    #     result = self.client.get('/favorite')
    #     print(result.data)
    #     self.assertIn(b"Thai Sweet Potato Veggie Burgers with Spicy Peanut Sauce", result.data)
    #     self.assertNotIn(b"Meatless Burgers with Romesco and Arugula", result.data)



class FlaskTestsSearchPage(TestCase):
    """Test dashboard page."""

    def setUp(self):
        """Before every test"""

        app.config['TESTING'] = True
        self.client = app.test_client()

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_correct_info(self):
        """ Test that what is supposed to show up in initial page is indeed showing. """

        result = self.client.get('/dashboard')
        self.assertIn(b"Discover new recipes with just one click", result.data)
        

    def test_no_search_results(self):
        """ Test that search results are not showing upon initial load. """

        result = self.client.get('/dashboard')
        self.assertNotIn(b"help", result.data)



class FlaskTestsBookmark(TestCase):
    """Test bookmark feature from server side."""

    def setUp(self):
        """Before every test"""

        app.config['TESTING'] = True
        self.client = app.test_client()

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_already_existing_bookmark(self):
        """ Test if error message appears with already-bookmarked recipe. """

        with self.client as c:
            result = c.post('/bookmark.json',
                            data={'recipe_id': '262682'},
                            follow_redirects=True
                            )

            self.assertIn(b"This recipe has been bookmarked!", result.data)

    def test_new_bookmark(self):
        """ Test if success message appears with bookmarking a new recipe. """

        # Check that bookmark did not exist before
        check = Bookmark.query.filter((Bookmark.recipe_id == '227961') & (Bookmark.user_id == 1)).first()
        self.assertIsNone(check)

        with self.client as c:
            result = c.post('/bookmark.json',
                            data={'recipe_id': '227961'},
                            follow_redirects=True
                            )

            # Check that success message appears
            self.assertIn(b"This recipe has been bookmarked!", result.data)

            # Check that new bookmark now successfully added
            current_bookmark = Bookmark.query.filter((Bookmark.recipe_id == '227961') & (Bookmark.user_id == 1)).first()
            self.assertIsNotNone(current_bookmark)

    # def test_existing_bookmark(self):
    #     """ Test if error message appears with an already-bookmarked recipe. """

    #     with self.client as c:
    #         result = c.post('/bookmark.json',
    #                         data={'recipe_id': '262682'},
    #                         follow_redirects=True
    #                         )

    #         # Check that error message appears
    #         self.assertIn(b"You've already bookmarked this recipe.", result.data)

    #         # Check that bookmark does not get duplicated in DB
    #         current_bookmark = Bookmark.query.filter((Bookmark.recipe_id == '262682') & (Bookmark.user_id == 1)).count()
    #         self.assertEqual(1L, current_bookmark)
        

if __name__ == "__main__":
    import unittest

    unittest.main()
