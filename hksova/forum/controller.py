from flask import Blueprint
from flask import render_template
from flask import current_app
from flask_paginate import Pagination, get_page_parameter
from flask import request

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

    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, total=post_count, per_page=10, search=search, record_name='sections')
    section=get_forum(section_id, pagination.skip, 10)

    return render_template("forum/forum_section.jinja", title="Fórum", year=year, section=section, pagination=pagination)
