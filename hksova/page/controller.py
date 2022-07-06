from flask import Blueprint
from flask import render_template
from flask import make_response
from flask import request
from flask import session

from ..year.model import *
from ..menu.model import *
from .model import *

main = Blueprint("main", __name__)

def check_authorization(ispublic, isprivate, isvisible):
    # org
    if session.get("org"): 
        if session["org"]: 
            return True

    # not org not visible
    if not isvisible: return False

    # public
    if ispublic: 
        return True
    else:
        if session.get("logged"):
            if not session["logged"]: False

            if isprivate==3 and session["ispaid"]: True
            if isprivate==2 and not session["isbackup"]: return True
            if isprivate==1: return True
            return False
        return False

@main.route("/")
def view_index():
    year=get_year(request.blueprint)
    years=get_years()
    menu=get_menu(year)
    page=get_page(year, 'index')
    r = make_response(render_template("page/page.jinja", title=page['title'], page=page, year=year, menu=menu, years=years))
    #r.headers.set('Content-Security-Policy', "default-src 'self'")
    r.headers.set('X-Content-Type-Options', 'nosniff')
    r.headers.set('X-Frame-Options', 'SAMEORIGIN')
    return r

@main.route("/<pageurl>")
def view_page(pageurl):
    year=get_year(request.blueprint)
    years=get_years()
    menu=get_menu(year)
    page=get_page(year, pageurl)

    if page:
        if check_authorization(page['ispublic'], page['isprivate'], page['isvisible']):
            r = make_response(render_template("page/page.jinja", title=page['title'], page=page, year=year, years=years, menu=menu))
            #r.headers.set('Content-Security-Policy', "default-src 'self'")
            r.headers.set('X-Content-Type-Options', 'nosniff')
            r.headers.set('X-Frame-Options', 'SAMEORIGIN')
            return r
        else:
            return render_template("errors/404.jinja",  year=year, menu=menu, years=years), 404
    else:
        return render_template("errors/404.jinja",  year=year, menu=menu, years=years), 404


