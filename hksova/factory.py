import os
from flask import Flask
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_mdeditor import MDEditor
from flask import render_template

from .page import main
from .team import team
from .forum import forum
from .admin import admin
from .year.model import *

def create_flask_app():
    flask_app = Flask(__name__)

    config_dir = "configs"
    if 'HKSOVA_CONFIG_DIR' in os.environ:
        config_dir = os.environ['HKSOVA_CONFIG_DIR']

    config_file = os.path.join(config_dir, "default.py")
    flask_app.config.from_pyfile(config_file)

    if 'HKSOVA_CONFIG' in os.environ:
        flask_app.config.from_envvar("HKSOVA_CONFIG")

    mysql = MySQL()
    mysql.init_app(flask_app)
    flask_app.mysql = mysql
    mdeditor = MDEditor(flask_app)
    csrf = CSRFProtect(flask_app)

    flask_app.register_blueprint (main)
    flask_app.register_blueprint (team)
    flask_app.register_blueprint (forum)
    flask_app.register_blueprint (admin)

    with flask_app.app_context():
        years=get_years()
        for yy in years:
            y=str(yy['idyear'])
            flask_app.register_blueprint (main, name="main"+y, url_prefix="/"+y)
            flask_app.register_blueprint (team, name="team"+y, url_prefix="/"+y)
            flask_app.register_blueprint (forum, name="forum"+y, url_prefix="/"+y)
            flask_app.register_blueprint (admin, name="admin"+y, url_prefix="/"+y)

    @flask_app.errorhandler(500)
    def internal_server_error(error):
        return render_template("errors/500.jinja"), 500

    @flask_app.errorhandler(404)
    def not_found_error(error):
        return render_template("errors/404.jinja"), 404

    return flask_app
