from flask import Blueprint
from flask import render_template
from flask import make_response
from flask import current_app
from flask import request

from ..year.model import *

main = Blueprint("main", __name__)

@main.route("/")
def view_index():
    year=get_year(request.blueprint)
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''SELECT * FROM page where idYear=%s and url=%s''', [year['year'], "index"])
    data = cursor.fetchall()

    r = make_response(render_template("page/page.jinja", text=data[0]['html'], title="Informace", year=year))
    #r.headers.set('Content-Security-Policy', "default-src 'self'")
    r.headers.set('X-Content-Type-Options', 'nosniff')
    r.headers.set('X-Frame-Options', 'SAMEORIGIN')
    return r
