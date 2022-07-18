'''
Page - controller
'''
from flask import Blueprint, render_template, make_response, request, session
from flask_paginate import Pagination, get_page_parameter

from .model import get_page

from ..year.model import get_year, get_years
from ..menu.model import get_menu
from ..forum.model import get_forum, get_forum_post_count
from ..forum.form import PostForm
from ..team.model import get_reports

main_blueprint = Blueprint("main", __name__)


def check_authorization(ispublic, isprivate, isvisible):
    # org
    if session.get("org"):
        if session["org"]:
            return True

    # not org not visible
    if not isvisible:
        return False

    # public
    if ispublic:
        return True

    # solve access in common case
    if session.get("logged"):
        if not session["logged"]:
            return False

        if isprivate == 3 and session["ispaid"]:
            return True
        if isprivate == 2 and not session["isbackup"]:
            return True
        if isprivate == 1:
            return True
        return False

    return False


@main_blueprint.route("/")
def view_index():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    page = get_page(year, 'index')
    r = make_response(render_template("page/page.jinja", title=page['title'], page=page, year=year, menu=menu, years=years))
    # r.headers.set('Content-Security-Policy', "default-src 'self'")
    r.headers.set('X-Content-Type-Options', 'nosniff')
    r.headers.set('X-Frame-Options', 'SAMEORIGIN')
    return r


@main_blueprint.route("/<pageurl>")
def view_page(pageurl):
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    page = get_page(year, pageurl)

    # forum on page
    if page is not None and page['idforumsection']:
        section_id = page['idforumsection']
        post_count = get_forum_post_count(section_id)
        post_form = PostForm()
        search = False
        q = request.args.get('q')
        if q:
            search = True

        if session.get("forum_name"):
            post_form.user.data = session['forum_name']
        else:
            if session.get('team'):
                post_form.user.data = session['team']

        forum_page = request.args.get(get_page_parameter(), type=int, default=1)
        pagination = Pagination(page=forum_page, total=post_count, per_page=10, search=search, record_name='sections')
        forum_section = get_forum(section_id, pagination.skip, 10)
        post_form.source_url = pageurl

        if check_authorization(page['ispublic'], page['isprivate'], page['isvisible']):
            r = make_response(render_template("page/page_forum.jinja", title=page['title'], page=page, year=year, years=years, menu=menu, section=forum_section, pagination=pagination, form=post_form, section_id=section_id))
            # r.headers.set('Content-Security-Policy', "default-src 'self'")
            r.headers.set('X-Content-Type-Options', 'nosniff')
            r.headers.set('X-Frame-Options', 'SAMEORIGIN')
            return r

        return render_template("errors/404.jinja", year=year, menu=menu, years=years, page=page), 404

    # reports on page
    if pageurl == "reportaze":
        reports = get_reports(year)
        if page:
            if check_authorization(page['ispublic'], page['isprivate'], page['isvisible']):
                r = make_response(render_template("page/page_reports.jinja", title=page['title'], page=page, year=year, years=years, menu=menu, reports=reports))
                # r.headers.set('Content-Security-Policy', "default-src 'self'")
                r.headers.set('X-Content-Type-Options', 'nosniff')
                r.headers.set('X-Frame-Options', 'SAMEORIGIN')
                return r

            return render_template("errors/404.jinja", year=year, menu=menu, years=years, page=page), 404

        return render_template("errors/404.jinja", year=year, menu=menu, years=years, page=page), 404

    # page wihout anything
    if page:
        if check_authorization(page['ispublic'], page['isprivate'], page['isvisible']):
            r = make_response(render_template("page/page.jinja", title=page['title'], page=page, year=year, years=years, menu=menu))
            # r.headers.set('Content-Security-Policy', "default-src 'self'")
            r.headers.set('X-Content-Type-Options', 'nosniff')
            r.headers.set('X-Frame-Options', 'SAMEORIGIN')
            return r

        return render_template("errors/404.jinja", year=year, menu=menu, years=years, page=page), 404

    return render_template("errors/404.jinja", year=year, menu=menu, years=years), 404
