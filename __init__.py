import json
import os

from flask import Flask, request, jsonify
import pandas as pd
import db
# import utils
from flask_cors import CORS
import urllib.parse
import collections

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

    @app.route('/getRecipe', methods=['GET'])
    def getRecipe():
        # TODO move data to Database
        df = pd.read_csv('data/prepared_recipes.csv')
        recipe_id = request.args.get('recipe_id')
        recipe = df.iloc[int(recipe_id)]
        return recipe.to_json()

    @app.route('/upload', methods=['GET'])
    def addAndMatchRecipe():
        url = urllib.parse.unquote(request.args.get('url'))
        #url = "https://www.instagram.com/p/BTWJYWrj5h_/?igshid=MzRlODBiNWFlZA=="
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
        print(result_string)
        #result_string = "Cornish plaice, herb crust, tomato and basil giant bean stew on as fish of the day"
        result_string = result_string.replace(",", "").replace("@", "").replace(".", "")
        result_tokens = set(result_string.split(" ")[:20])
        df = pd.read_csv("data/prepared_recipes.csv")
        df['names'] = df['name'].astype(str).apply(lambda x: x.split(" "))
        df['no_tokens'] = df['names'].transform(lambda x: len(x))
        df['matches'] = df['names'].transform(lambda x: len(result_tokens.intersection(set(x))))
        df['ratio'] = df['matches'] / df['no_tokens']
        m = df['ratio'].max()
        recipe = df[df['ratio'] == m]
        return(str(list(recipe.index)[0]))


    @app.route('/crawl')
    def crawlGoogleImages():
        utils.scrapFirstImageFromGoogle("cat")
        return 'Crawling!'

    return app