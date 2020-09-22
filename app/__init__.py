
import logging
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_babel import Babel
from flask import request
from logging.handlers import RotatingFileHandler

import os
application = Flask(__name__)
application.config.from_object(Config)
db = SQLAlchemy(application)
migrate = Migrate(application, db)
login = LoginManager(application)
bootstrap = Bootstrap(application)
babel = Babel(application)
from app import routes, models

if not application.debug:
	if not os.path.exists('logs1'):
		os.mkdir('logs1')
	file_handler = RotatingFileHandler('logs1/lang.log', maxBytes=10240,
												backupCount=10)
	file_handler.setFormatter(logging.Formatter(
		'%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
	file_handler.setLevel(logging.INFO)
	application.logger.addHandler(file_handler)
	application.logger.setLevel(logging.INFO)
	application.logger.info('Lang startup')

@babel.localeselector
def get_locale():
	return request.accept_languages.best_match(application.config['LANGUAGES'])