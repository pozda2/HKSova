from flask import Blueprint
from flask import render_template
from flask import make_response
from flask import current_app
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
