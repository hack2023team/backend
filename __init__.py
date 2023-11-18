import os

from flask import Flask, request, jsonify

from . import db
from . import utils

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'backend.sqlite'),
    )

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
    
    return app