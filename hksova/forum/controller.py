'''
Forum - controller
'''
import socket
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_paginate import Pagination, get_page_parameter

from .utils import current_year_required
from .form import PostForm
from .model import get_forum, get_forum_sections, get_forum_post_count, insert_post
from ..year.model import get_year, get_years
from ..menu.model import get_menu

forum_blueprint = Blueprint("forum", __name__)


@forum_blueprint.route("/forum/")
def view_forum_section():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    sections = get_forum_sections(year)
    return render_template("forum/forums.jinja", title="Fórum", year=year, sections=sections, menu=menu, years=years)


@forum_blueprint.route("/forum/<int:section_id>")
def view_forum(section_id):
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    post_count = get_forum_post_count(section_id)
    post_form = PostForm()
    post_form.source_url = "forum"

    search = False
    q = request.args.get('q')
    if q:
        search = True

    if session.get("forum_name"):
        post_form.user.data = session['forum_name']
    else:
        if session.get('team'):
            post_form.user.data = session['team']

    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, total=post_count, per_page=10, search=search, record_name='sections')
    section = get_forum(section_id, pagination.skip, 10)

    return render_template("forum/forum_section.jinja", title="Fórum", year=year, section=section, pagination=pagination, form=post_form, section_id=section_id, menu=menu, years=years)


@forum_blueprint.route("/forum/<int:section_id>", methods=["POST"])
@current_year_required
def create_post(section_id):
    year = get_year(request.blueprint)
    post_form = PostForm(request.form)

    '''
    # TODO: handle IPs behind proxy + probably proxy reconf needed
    print(request.remote_addr)
    print(request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
    print(request.environ)
    '''
    remote_ip = request.headers.get('X-Forwarded-For').split(', ')[0]

    if post_form.validate():
        status, message = insert_post(section_id, post_form.user.data, post_form.post.data, remote_ip, socket.getnameinfo((remote_ip, 0), 0)[0], request.headers.get('User-Agent'))

        session['forum_name'] = post_form.user.data
        if not status:
            flash(message, "error")
    else:
        for _, errors in post_form.errors.items():
            for error in errors:
                if isinstance(error, dict) and len(error) > 0:
                    for k in error.keys():
                        flash(f'{error[k][0]}', "error")
                else:
                    flash(f'{error}', "error")

    if post_form.source_url.data == "forum":
        return redirect(url_for("forum" + year['year'] + ".view_forum", section_id=section_id))

    return redirect(url_for("main" + year['year'] + ".view_page", pageurl=post_form.source_url.data))
