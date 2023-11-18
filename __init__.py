import json
import os

from flask import Flask, request, jsonify
import pandas as pd
import db
# import utils
from flask_cors import CORS
import urllib.parse
import collections
import numpy as np
from recomendations_recipies import getRecepyIDs, exampleDislikes
from nltk.corpus import stopwords



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'backend.sqlite'),
    )
    CORS(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    # TODO: call init recipes

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/addUser')
    def add_user():
        username = "MaxMustermann"
        preferences = ["vegan"]
        allergic_to = ["nuts"]

        database = db.get_db()
        error = None
        if database.execute(
                'SELECT preferences FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            database.execute(
                'INSERT INTO user (username, preferences, allergies) VALUES (?, ?, ?)',
                (username, utils.dump_to_text(preferences), utils.dump_to_text(allergic_to))
            )
            database.commit()
            return 'User {} added!'.format(username)

        return error

    @app.route('/getPreferences', methods=['GET'])
    def getPreferences():
        username = "MaxMustermann"
        preferences = None

        # connect to the database and get the preferences of the user
        database = db.get_db()

        preferences = database.execute(
            'SELECT preferences FROM user WHERE username = ?', (username,)
        ).fetchone()

        if preferences:
            return utils.dump_to_text(preferences[0])
        return 'No such user added!'

    @app.route('/getAllergies', methods=['GET'])
    def getAllergies():
        username = "MaxMustermann"
        allergies = None

        # connect to the database and get the preferences of the user
        database = db.get_db()

        allergies = database.execute(
            'SELECT allergies FROM user WHERE username = ?', (username,)
        ).fetchone()

        if allergies:
            return utils.dump_to_text(allergies[0])
        return 'No such user added!'

    @app.route('/getRecommendations', methods=['GET'])
    def getRecommendation():
        stored_recepies = pd.read_csv("data/customer_recipes.csv")
        stored_recepies = stored_recepies["recipe_match"]
        return "|".join(list(map(lambda x: str((int(x[0]), int(x[1]))), getRecepyIDs(stored_ids=stored_recepies, dislikes_ingredients=exampleDislikes()))))
        # return "|".join(list(map(lambda x: str(x), list(
        #     zip(list(np.random.randint(1000, size=40)), list(np.random.randint(1000, size=40)))))))

    @app.route('/getRecipe', methods=['GET'])
    def getRecipe():
        df = pd.read_csv('data/prepared_recipes.csv')
        recipe_id = request.args.get('recipe_id')
        recipe = df.iloc[int(recipe_id)]
        return recipe.to_json()

    @app.route('/writeMealPlan', methods=['GET'])
    def writeMealPlan():
        meal_id = request.args.get("meal")
        user_id = request.args.get("user_id")
        print("writing meal plan")
        df = pd.read_csv('data/meal_plan.csv')
        weekdays = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
        try:
            last_day = df["day"].iloc(-1)
            index = weekdays.index(last_day)+1
            day = weekdays[index]
        except:
            day = "MON"
        storage_dict = {
            "user_id":user_id,
            "meal":meal_id,
            "day":day}
        df = pd.concat([df, pd.DataFrame(storage_dict, index=[0])], ignore_index=True)
        df.to_csv('data/customer_recipes.csv', index=False)

    @app.route('/getMealPlan', methods=['GET'])
    def getMealPlan():
        print("loading meal plan")
        df = pd.read_csv('data/meal_plan.csv')
        df_recipes = pd.read_csv('data/prepared_recipes.csv')
        user_id = request.args.get('user_id')
        print(df)
        df = df[df['user_id'].astype(str) == user_id]
        recipes = df['meal']
        recipes_name = df['meal'].map(lambda x: df_recipes.iloc[x]['name'])
        day = df['day']
        return "|".join(list(map(lambda x: str(x), list(zip(list(day), list(recipes), list(recipes_name))))))

    @app.route('/upload', methods=['GET'])
    def addAndMatchRecipe():
        url = urllib.parse.unquote(request.args.get('url'))
        user_id = urllib.parse.unquote(request.args.get('user_id'))
        print(user_id)
        print(url)
        # url = "https://www.instagram.com/p/BTWJYWrj5h_/?igshid=MzRlODBiNWFlZA=="
        tokens = url.split("/")
        post_id = tokens[4]
        print(post_id)
        import http.client

        conn = http.client.HTTPSConnection("easy-instagram-service.p.rapidapi.com")

        headers = {
            'X-RapidAPI-Key': "6cd495ba24msha250124f90cae4bp134cfdjsn42ebe9af169c",
            'X-RapidAPI-Host': "easy-instagram-service.p.rapidapi.com"
        }

        conn.request("GET", "/get-post?shortcode=" + post_id, headers=headers)

        res = conn.getresponse()
        data = res.read()
        j = json.loads(data)
        result_string = j['caption']
        print(j)
        # result_string = "Cornish plaice, herb crust, tomato and basil giant bean stew on as fish of the day"
        result_string = result_string.replace(",", "").replace("@", "").replace(".", "")
        result_tokens = set(result_string.split(" ")[:20])
        s = stopwords.words('english')
        result_tokens.discard(set(s))
        df = pd.read_csv("data/prepared_recipes.csv")
        df['names'] = df['name'].astype(str).apply(lambda x: x.split(" "))
        df['no_tokens'] = df['names'].transform(lambda x: len(x))
        df['matches'] = df['names'].transform(lambda x: len(result_tokens.intersection(set(x))))
        df['ratio'] = df['matches'] / df['no_tokens']
        m = df['ratio'].max()
        recipe = df[df['ratio'] == m]
        recipe = str(list(recipe.index)[0])
        storage_dict = {
            "user_id": user_id,
            "caption": result_string,
            "image_url": j['display_url'],
            "recipe_match": recipe
        }
        df2 = pd.read_csv('data/customer_recipes.csv')
        df2 = pd.concat([df2, pd.DataFrame(storage_dict, index=[0])], ignore_index=True)
        df2.to_csv('data/customer_recipes.csv', index=False)
        return (recipe)

    return app