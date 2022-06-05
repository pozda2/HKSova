from flask import Blueprint
from flask import render_template
from flask import current_app
from flask_paginate import Pagination, get_page_parameter
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import flash
import socket

from ..year.model import *
from .form import *
from .model import *

forum = Blueprint("forum", __name__)

@forum.route("/forum")
def view_forum_section():
    year=get_year(request.blueprint)
    sections=get_forum_sections(year)
    return render_template("forum/forums.jinja", title="Fórum", year=year, sections=sections)

@forum.route("/forum/<int:section_id>")
def view_forum(section_id):
    year=get_year(request.blueprint)
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

    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, total=post_count, per_page=10, search=search, record_name='sections')
    section=get_forum(section_id, pagination.skip, 10)

    return render_template("forum/forum_section.jinja", title="Fórum", year=year, section=section, pagination=pagination, form=post_form, section_id=section_id)

@forum.route("/forum/<int:section_id>", methods=["POST"])
def create_post(section_id):
    year=get_year(request.blueprint)
    post_form = PostForm(request.form)

    if not year['is_current_year']:
        flash ("Komentovat lze pouze aktuální ročník", "error")
        return redirect (url_for("forum"+year['year']+".view_forum", section_id=section_id))

    if post_form.validate():
        status, message=save_post(section_id, post_form.user.data, post_form.post.data, request.remote_addr, socket.getnameinfo((request.remote_addr, 0), 0)[0], request.headers.get('User-Agent'))
        session['forum_name']=post_form.user.data
        if not status:
            flash (message, "error")
    else:
        for _, errors in post_form.errors.items():
            for error in errors:
                if isinstance(error, dict):
                    if (len(error)>0):
                        for k in error.keys():
                            flash (f'{error[k][0]}', "error")
                else:
                    flash (f'{error}', "error")

    return redirect (url_for("forum"+year['year']+".view_forum", section_id=section_id))