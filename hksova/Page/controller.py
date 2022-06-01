from flask import Blueprint
from flask import render_template
from flask import make_response
from flask import current_app
from flask import request

import mistune
from mistune.plugins import plugin_table

from ..Year.model import *

main = Blueprint("main", __name__)

@main.route("/")
def view_index():
	year=get_year(request.blueprint)

	cursor = current_app.mysql.connection.cursor()
	# mysql.connectin.commit()
	cursor.execute('''SELECT * FROM page where idYear=%s and url=%s''', [year, "index"])
	data = cursor.fetchall()
# 	texy=data[0]['texy']

# 	texy='''| a  | b  |
# | ------------ | ------------ |
# | c  |  d |
# |  e |  f |'''

# 	t = mistune.html(texy)

	#markdown = mistune.create_markdown(escape=False, plugins=['table'])
	#t=markdown(texy)

	r = make_response(render_template("Page/page.jinja", text=data[0]['html'], title="Informace", year=year))
	#r.headers.set('Content-Security-Policy', "default-src 'self'")
	r.headers.set('X-Content-Type-Options', 'nosniff')
	r.headers.set('X-Frame-Options', 'SAMEORIGIN')
	return r