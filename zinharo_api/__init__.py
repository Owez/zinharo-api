from flask import Flask, send_file
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .utils import Config

# ---- CONFIG ----#


config = Config()
app = Flask(__name__)

app.config["SECRET_KEY"] = config.SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///zinharo.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)  # flask-sqlalchemy (db)
bcrypt = Bcrypt(app)  # BCrypt (pw hashing)
jwt = JWTManager(app)  # JSON-web-tokens (account auth)
ma = Marshmallow(app)  # Marshmallow (api parsing)
limiter = Limiter(
    app, key_func=get_remote_address, default_limits=["200 per day", "50 per hour"]
)  # API ratelimit


@app.errorhandler(404)
def error_404(_exception):
    """404 error handling"""

    return {"status": "endpoint not found"}, 404


@app.route(f"{config.API_PREFIX}/min_version/")
def api_minversion():
    """A simple auxillary route to provide the minimum API client version"""

    return {"status": "success", "body": {"min_version": config.MIN_API_VERSION}}, 200


@limiter.limit("2 per minute, 10 per day")
@app.route("/client/linux")
def download_linux():
    """Downloads linux client for user"""

    path = "zinharo-client-linux.zip"

    return send_file(path, as_attachment=True)


@limiter.limit("2 per minute, 10 per day")
@app.route("/client/windows")
def download_windows():
    """Downloads windows client for user"""

    path = "zinharo-client-windows.zip"

    return send_file(path, as_attachment=True)


# NOTE: keep imports here
from .routes.report import report_api_blueprint
from .routes.client import client_api_blueprint
from .routes.auth import auth_api_blueprint
from .routes.hash import hash_api_blueprint
from .routes.job import job_api_blueprint

app.register_blueprint(report_api_blueprint, url_prefix=config.API_PREFIX)
app.register_blueprint(client_api_blueprint, url_prefix=config.API_PREFIX)
app.register_blueprint(auth_api_blueprint, url_prefix=config.API_PREFIX)
app.register_blueprint(hash_api_blueprint, url_prefix=config.API_PREFIX)
app.register_blueprint(job_api_blueprint, url_prefix=config.API_PREFIX)
