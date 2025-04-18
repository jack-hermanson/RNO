import logging
import os
import subprocess
import sys
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, request
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from application.config import Config
from application.modules.accounts.ClearanceEnum import ClearanceEnum
from application.utils.CrudEnum import CrudEnum
from application.utils.get_ip import get_ip
from logger import StreamLogFormatter, FileLogFormatter, StaticURLFilter

bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate(compare_type=True)
logging.basicConfig(level=logging.DEBUG)

login_manager = LoginManager()
login_manager.login_view = "accounts.login"
login_manager.login_message_category = "warning"


def create_app(config_class=Config):
    # set up file paths for static resources
    app = Flask(__name__, static_url_path="/static", static_folder="web/static", template_folder="web/templates")

    # set up environment variables
    app.config.from_object(config_class)

    # bcrypt
    bcrypt.init_app(app)

    # models
    import application.modules.accounts.models
    import application.modules.admin.roles.models

    # database
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)

    # routes and blueprints
    from application.modules.main.routes import main
    from application.modules.accounts.routes import accounts
    from application.modules.admin.routes import admin
    from application.modules.admin.roles.routes import roles
    from .modules.errors.handlers import errors

    for blueprint in [main, accounts, admin, roles, errors]:
        app.register_blueprint(blueprint)

    # login manager
    login_manager.init_app(app)

    # filters
    @app.template_filter()
    def number_suffix(value):
        if 10 <= value % 100 <= 20:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(value % 10, "th")
        return f"{value}{suffix}"

    @app.context_processor
    def inject_environment():
        return dict(
            environment=os.environ.get("ENVIRONMENT"),
            rno_name=os.environ.get("RNO_NAME"),
            ClearanceEnum=ClearanceEnum,
            CrudEnum=CrudEnum,
            commit=subprocess.check_output(["git", "describe", "--always"]).strip().decode("utf-8"),
        )

    @app.before_request
    def before_request():
        if not request.path.startswith("/static"):
            logger.debug(
                f"[{current_user.username if current_user.is_authenticated else 'anon'} - {get_ip(request)}] "
                f"{request.method}: {request.path} "
            )

    # return the app
    print("RUNNING APPLICATION")
    logger.debug("LOGGING IS RUNNING")
    flask_debug = bool(int(os.environ.get("FLASK_DEBUG")))
    logger.info(f"FLASK_DEBUG: '{flask_debug}'")
    return app


# Set up logging
environment = os.environ.get("ENVIRONMENT")
logging.basicConfig()
logger = logging.getLogger("RNO")
logger.propagate = False
sh = logging.StreamHandler(sys.stdout)
sh.setFormatter(StreamLogFormatter())

log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

fh = TimedRotatingFileHandler(os.path.join(log_dir, "logs.txt"), when="midnight", interval=1, backupCount=7)
fh.setFormatter(FileLogFormatter())
fh.suffix += ".txt"
fh.namer = lambda name: name.replace(".txt", "") + ".txt"

logger.addHandler(fh)
logger.addHandler(sh)
log_level = getattr(logging, os.environ.get("LOG_LEVEL", "INFO"))
print(f"Setting application log level to {logging.getLevelName(log_level)} in {os.environ.get('ENVIRONMENT')}")
logger.setLevel(log_level)

# SQL Alchemy
logging.getLogger("sqlalchemy.engine").setLevel(
    logging.INFO if bool(int(os.environ.get("SQLALCHEMY_ECHO", 0))) else logging.WARNING
)
logging.getLogger("sqlalchemy.engine").addHandler(fh)
logging.getLogger("sqlalchemy.engine").addHandler(fh)
logging.getLogger("sqlalchemy.engine").propagate = False

# Werkzeug
werkzeug_log_level = logging.WARNING  # if environment == "production" else logging.INFO
print(f"Setting werkzeug log level to {logging.getLevelName(werkzeug_log_level)} in {environment}")
logging.getLogger("werkzeug").setLevel(werkzeug_log_level)
logging.getLogger("werkzeug").addFilter(StaticURLFilter())
logging.getLogger("werkzeug").addHandler(fh)
logging.getLogger("werkzeug").addHandler(sh)
logging.getLogger("werkzeug").propagate = False
