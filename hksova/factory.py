import os
from flask import Flask
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_mdeditor import MDEditor
from flask import render_template

from .page import main_blueprint
from .team import team_blueprint
from .forum import forum_blueprint
from .admin import admin_blueprint
from .year.model import get_year, get_years
from hksova import admin


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

    flask_app.register_blueprint(main_blueprint)
    flask_app.register_blueprint(team_blueprint)
    flask_app.register_blueprint(forum_blueprint)
    flask_app.register_blueprint(admin_blueprint)

    with flask_app.app_context():
        years = get_years()
        for yy in years:
            y = str(yy['idyear'])
            flask_app.register_blueprint(main_blueprint, name="main" + y, url_prefix="/" + y)
            flask_app.register_blueprint(team_blueprint, name="team" + y, url_prefix="/" + y)
            flask_app.register_blueprint(forum_blueprint, name="forum" + y, url_prefix="/" + y)
            flask_app.register_blueprint(admin_blueprint, name="admin" + y, url_prefix="/" + y)

        # blueprint for next year
        y = str(years[0]['idyear'] + 1)
        flask_app.register_blueprint(main_blueprint, name="main" + y, url_prefix="/" + y)
        flask_app.register_blueprint(team_blueprint, name="team" + y, url_prefix="/" + y)
        flask_app.register_blueprint(forum_blueprint, name="forum" + y, url_prefix="/" + y)
        flask_app.register_blueprint(admin_blueprint, name="admin" + y, url_prefix="/" + y)

    @flask_app.errorhandler(500)
    def internal_server_error(error):
        year = get_year('notemptystring')
        return render_template("errors/500.jinja", year=year), 500

    @flask_app.errorhandler(404)
    def not_found_error(error):
        year = get_year('notemptystring')
        return render_template("errors/404.jinja", year=year), 404

    return flask_app
