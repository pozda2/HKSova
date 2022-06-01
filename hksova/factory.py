import os
from flask import Flask
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_mdeditor import MDEditor
from flask import render_template

from .page import main
from .team import team
# from .settings import settings

def create_flask_app():
    flask_app = Flask(__name__)

    config_dir = "configs"
    if 'HKSOVA_CONFIG_DIR' in os.environ:
        config_dir = os.environ['HKSOVA_CONFIG_DIR']

    config_file = os.path.join(config_dir, "default.py")
    flask_app.config.from_pyfile(config_file)

    if 'HKSOVA_CONFIG' in os.environ:
        flask_app.config.from_envvar("HKSOVA_CONFIG")

    # print(flask_app.config)

    mysql = MySQL()
    mysql.init_app(flask_app)
    print(flask_app.config['MYSQL_HOST'])
    flask_app.mysql = mysql
    mdeditor = MDEditor(flask_app)
    csrf = CSRFProtect(flask_app)

    # blueprinty budou v cyklu podle select * from year
    flask_app.register_blueprint (main)
    flask_app.register_blueprint (main, name="main2022", url_prefix="/2022")
    flask_app.register_blueprint (main, name="main2021", url_prefix="/2021")

    flask_app.register_blueprint (team)
    flask_app.register_blueprint (team, name="team2022", url_prefix="/2022")
    flask_app.register_blueprint (team, name="team2021", url_prefix="/2021")

    @flask_app.errorhandler(500)
    def internal_server_error(error):
        return render_template("errors/500.jinja"), 500

    @flask_app.errorhandler(404)
    def not_found_error(error):
        return render_template("errors/404.jinja"), 404

    return flask_app
