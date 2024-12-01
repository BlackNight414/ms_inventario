from flask import Flask
from flask_marshmallow import Marshmallow
import os
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import config
from flask_caching import Cache

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
cache = Cache()

def create_app():
    app_context = os.getenv('FLASK_CONTEXT')
    app = Flask(__name__)
    f = config.factory(app_context if app_context else 'development')
    app.config.from_object(f)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    
    cache.init_app(app, config={
        'CACHE_TYPE': 'RedisCache',
        'CACHE_DEFAULT_TIMEOUT': 300,
        'CACHE_REDIS_HOST': os.getenv('REDIS_HOST'),
        'CACHE_REDIS_PORT': os.getenv('REDIS_PORT'),
        'CACHE_REDIS_DB': os.getenv('REDIS_DB'),
        'CACHE_REDIS_PASSWORD': os.getenv('REDIS_PASSWORD'),
        'CACHE_KEY_PREFIX': 'inventario_'
    })

    from app.resources import inventario
    app.register_blueprint(inventario, url_prefix='/inventario')
    
    @app.shell_context_processor    
    def ctx():
        return {"app": app}
    
    import logging
    logging.basicConfig(
        level=logging.DEBUG, 
        format="{asctime} - {levelname} - {message}", # formato de mensaje log
        style="{",
        datefmt="%Y-%m-%d %H:%M", # formato de tiempo
        ) 

    return app