from flask import Blueprint
from flask import render_template
from flask import make_response
from flask import request
from flask import session
from flask_paginate import Pagination, get_page_parameter

from .model import *
from ..year.model import *
from ..menu.model import *
from ..forum.model import *
from ..forum.form import *
from ..team.model import *

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

    # forum on page
    if page['idforumsection']:
        section_id=page['idforumsection']
        post_count=get_forum_post_count(section_id)
        post_form = PostForm()
        search = False
        q = request.args.get('q')
        if q:
            search = True

        if session.get("forum_name"):
            post_form.user.data=session['forum_name']
        else:
            if session.get('team'):
                post_form.user.data=session['team']

        forum_page = request.args.get(get_page_parameter(), type=int, default=1)
        pagination = Pagination(page=forum_page, total=post_count, per_page=10, search=search, record_name='sections')
        forum_section=get_forum(section_id, pagination.skip, 10)
        post_form.source_url=pageurl

        if check_authorization(page['ispublic'], page['isprivate'], page['isvisible']):
            r = make_response(render_template("page/page_forum.jinja", title=page['title'], page=page, year=year, years=years, menu=menu, section=forum_section, pagination=pagination, form=post_form, section_id=section_id))
            #r.headers.set('Content-Security-Policy', "default-src 'self'")
            r.headers.set('X-Content-Type-Options', 'nosniff')
            r.headers.set('X-Frame-Options', 'SAMEORIGIN')
            return r
        else:
            return render_template("errors/404.jinja",  year=year, menu=menu, years=years), 404

    # reports on page
    if (pageurl == "reportaze"):
        reports=get_reports(year)
        if page:
            if check_authorization(page['ispublic'], page['isprivate'], page['isvisible']):
                r = make_response(render_template("page/page_reports.jinja", title=page['title'], page=page, year=year, years=years, menu=menu, reports=reports))
                #r.headers.set('Content-Security-Policy', "default-src 'self'")
                r.headers.set('X-Content-Type-Options', 'nosniff')
                r.headers.set('X-Frame-Options', 'SAMEORIGIN')
                return r
            else:
                return render_template("errors/404.jinja",  year=year, menu=menu, years=years), 404
        else:
            return render_template("errors/404.jinja",  year=year, menu=menu, years=years), 404

    # page wihout anything
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


