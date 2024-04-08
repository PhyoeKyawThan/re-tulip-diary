from flask import Flask, config
from flask_sqlalchemy import SQLAlchemy
# define db for all file as global var
db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)
    
    # import blueprints
    from .views import views
    from .auth import auth
    from .actions import actions

    # register the blueprints
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(actions, url_prefix="/action")

    with app.app_context():
        db.create_all()
    
    # returning app
    return app
