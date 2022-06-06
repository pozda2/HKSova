from flask import Blueprint
from flask import render_template
from flask import current_app
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

import mistune
from mistune.plugins import plugin_table

from ..year.model import *
from .form import *
from .model import *
from .utils import org_login_required

admin = Blueprint("admin", __name__)

@admin.route("/admin/pages/", methods=["GET"])
@org_login_required
def view_admin_pages():
    year=get_year(request.blueprint)
    pages=get_pages(year)
    return render_template("admin/pages.jinja", title="Správa stránek", year=year, pages=pages)

@admin.route("/admin/page/<int:idpage>")
@org_login_required
def view_admin_page(idpage):
    year=get_year(request.blueprint)
    page_form = PageForm()
    page=get_admin_page(idpage)
    page_form.title.data=page['title']
    page_form.url.data=page['url']
    page_form.content.data=page['texy']
    page_form.isvisible.data=page['isvisible']
    page_form.access_rights.data=encode_access_rights(page['ispublic'], page['isprivate'])
    return render_template("admin/page.jinja", title="Editace stránky", year=year, page=page, form=page_form, idpage=idpage)

@admin.route("/admin/page/<int:idpage>", methods=["POST"])
def edit_page(idpage):
    page_form = PageForm(request.form)
    if page_form.validate():
        markdown = mistune.create_markdown(escape=False, plugins=['table'])
        html=markdown(page_form.content.data)
        is_public, is_private=decode_access_rights(page_form.access_rights.data)
        
        status, message=save_page(idpage, page_form.title.data, page_form.url.data, page_form.content.data, html, is_public, is_private, page_form.isvisible.data)
        if not status:
           flash (message, "error")
        else:
            flash ('Stránka upravena', "info")
    else:
        for _, errors in page_form.errors.items():
            for error in errors:
                if isinstance(error, dict):
                    if (len(error)>0):
                        for k in error.keys():
                            flash (f'{error[k][0]}', "error")
                else:
                    flash (f'{error}', "error")

    return redirect (url_for("admin.view_admin_pages"))