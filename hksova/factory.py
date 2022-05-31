import os
from flask import Flask
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_mdeditor import MDEditor
from flask import render_template

from .Page import main
from .Team import team
#from .Settings import settings

def create_flask_app():
	flask_app = Flask(__name__)

	if "HKSOVA_CONFIG_DIR" in os.environ:
		if os.environ['HKSOVA_CONFIG_DIR']:
			config_dir=os.environ['HKSOVA_CONFIG_DIR']
		else:
			config_dir=".."

	config_file=os.path.join(config_dir, "default.py")
	flask_app.config.from_pyfile(config_file)

	if "HKSOVA_CONFIG" in os.environ:
		if os.environ['HKSOVA_CONFIG']:
			flask_app.config.from_envvar("HKSOVA_CONFIG")

	mysql = MySQL()
	mysql.init_app(flask_app)
	print (flask_app.config['MYSQL_HOST'])
	flask_app.mysql=mysql
	mdeditor = MDEditor(flask_app)

	csrf = CSRFProtect(flask_app)

	flask_app.register_blueprint (main)
	#flask_app.register_blueprint (main, name="2021", url_prefix="/2021")

	flask_app.register_blueprint (team)
	#flask_app.register_blueprint (team, name="team_2021", url_prefix="/2021")
	flask_app.register_blueprint (team, name="team_2022", url_prefix="/2022")


	@flask_app.errorhandler(500)
	def internal_server_error(error):
		return render_template("errors/500.jinja"), 500

	@flask_app.errorhandler(404)
	def internal_server_error(error):
		return render_template("errors/404.jinja"), 500

	return flask_app