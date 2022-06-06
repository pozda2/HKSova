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
from .utils import org_login_required

admin = Blueprint("admin", __name__)

@admin.route("/admin/pages/", methods=["GET"])
@org_login_required
def view_pages():
    year=get_year(request.blueprint)
    pages=get_pages(year)
    print (pages)
    print (year)
    #return redirect (url_for("main.view_index"))
    return render_template("admin/pages.jinja", title="Správa stránek", year=year, pages=pages)