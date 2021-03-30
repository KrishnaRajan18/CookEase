## CookEase

CookEase helps the user to search for recipies based on the ingredient. This gives the user the exact idea of what all ingredients and steps are required to make a recipe at home. It also provides a feature to bookmark a recipe for future.

## Table of Contents

- [Technologies](#technologies)
- [Features](#features)
- [Installation](#installation)
- [Future Features](#future-features)

## Technologies

- Backend: Python, Flask, PostgreSQL, SQLAlchemy
- Frontend: JavaScript, jQuery, AJAX, JSON, Jinja2, HTML5, CSS, Bootstrap
- API: Spoonacular API

## Features

Users can log in or register in the homepage, where the data is stored after password hashing to the PostgreSQL database. Registered users have access to the search page and once own bookmark page.

Users can also search for recipes, triggering Spoonacular API calls to access recipe data upon clicking the search button. A loading button is installed to provide user feedback.

Users can bookmark recipes via AJAX POST requests, which can be accessed in their bookmark page. The bookmark page includes user details as well as a Bootstrap carousel of the bookmarked recipes' images. Jinja2 was particularly used here to standardize the layout schema of all bookmark pages.

## Installation

To run CookEase:

Install PostgreSQL (Mac OSX)

Clone or fork this repo:

```
https://github.com/KrishnaRajan18/CookEase.git
```

To have this app running on your local computer:
Create and activate a virtual environment inside your project directory:

```
virtualenv venv
source venv/bin/activate
```

Install the dependencies:

```
pip install -r requirements.txt
```

Sign up to use the [Spoonacular API](https://spoonacular.com/food-api).

Save your API key in a file called dotenv using this format:

```
API_KEY="YOURKEYHERE"
```

Create database 'recipe'.

```
createdb recipe
```

Create your database tables

```
python model.py
```

Run the app:

```
python server.py
```

You can now navigate to 'localhost:8000/' to start exploring CookEase. Happy Cooking!

## Future-Features

- Users can create a list of grocery items from recipe choosen.
- Users can access the recipes included in each grocery list.
- Expanding on the recipe search filter (e.g. dietary restrictions, calories, etc.)
