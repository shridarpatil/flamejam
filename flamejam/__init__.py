import os, sys
from flask import Flask
from datetime import *
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.markdown import Markdown
from flask.ext.principal import Principal, Permission, RoleNeed
from flask.ext.login import LoginManager, current_user
from flask.ext.cache import Cache

app = Flask(__name__)

app.config.from_pyfile('../doc/flamejam.cfg.default')
if os.environ.get('CONFIG_TYPE') == "production":
    app.config.from_pyfile('/etc/flamejam/flamejam.cfg', silent=True)
else:
    app.config.from_pyfile('../flamejam.cfg', silent=True)

mail = Mail(app)
db = SQLAlchemy(app)
markdown_object = Markdown(app, safe_mode="escape")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

principals = Principal(app)
admin_permission = Permission(RoleNeed('admin'))

cache = Cache(app)

from flamejam.utils import *
import flamejam.filters
import flamejam.views
import flamejam.models

@app.context_processor
def inject():
    return dict(current_user = current_user,
        current_datetime = datetime.utcnow(),
        current_jam = get_current_jam(),
        RATING_CATEGORIES = flamejam.models.rating.RATING_CATEGORIES)
