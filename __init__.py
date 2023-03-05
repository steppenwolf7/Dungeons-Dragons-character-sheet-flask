import random
import os
from flask import Flask, jsonify

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskapp.sqlite'),
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


    @app.route('/attribute', methods=('GET', 'POST'))
    def attribute():
        throws = []
        def roll_1d6():
            return random.randint(1,6)
    
        def roll_4d6(num_dice):
            for i in range(num_dice):
                throws.append(roll_1d6())
            
            return throws
        roll_4d6(4)
        sorted_throws = sorted(throws, reverse=True) 
        top_tree = sorted_throws[:3]
        attribute = sum(top_tree)
        
        return jsonify(attribute)
    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    
    from . import dd_roller
    app.register_blueprint(dd_roller.bp)
    app.add_url_rule('/roll', endpoint='roll')
    
    return app