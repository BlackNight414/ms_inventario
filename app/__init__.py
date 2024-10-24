from flask import Flask
# from flask_marshmallow import Marshmallow
import os
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import config

db = SQLAlchemy()
migrate = Migrate()
# ma = Marshmallow()

def create_app():
    app_context = os.getenv('FLASK_CONTEXT')
    app = Flask(__name__)
    f = config.factory(app_context if app_context else 'development')
    app.config.from_object(f)

    db.init_app(app)
    migrate.init_app(app, db)
    # ma.init_app(app)
    
    from app.resources import inventario
    app.register_blueprint(inventario, url_prefix='/inventario')
    
    @app.shell_context_processor    
    def ctx():
        return {"app": app}
    
    return app