from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from ..year.model import *
from .form import *
from .model import *
from .utils import org_login_required

admin = Blueprint("admin", __name__)

@admin.route("/admin/pages/", methods=["GET"])
@org_login_required
def view_admin_pages():
    year=get_year(request.blueprint)
    pages=get_admin_pages(year)
    return render_template("admin/pages.jinja", title="Správa stránek", year=year, pages=pages)

@admin.route("/admin/page/<int:idpage>", methods=["GET"])
@org_login_required
def view_admin_page(idpage):
    year=get_year(request.blueprint)
    page_form = PageForm()
    page=get_admin_page(idpage)
    page_form.title.data=page['title']
    page_form.url.data=page['url']
    page_form.content.data=page['texy']
    page_form.isvisible.data=page['isvisible']
    page_form.access_rights.process_data(encode_access_rights(page['ispublic'], page['isprivate']))
    return render_template("admin/page.jinja", title="Editace stránky", year=year, form=page_form, idpage=idpage)

@admin.route("/admin/page/<int:idpage>", methods=["POST"])
def edit_page(idpage):
    year=get_year(request.blueprint)
    page_form = PageForm(request.form)
    if page_form.validate():
        markdown = mistune.create_markdown(escape=False, plugins=['table'])
        html=markdown(page_form.content.data)
        is_public, is_private=decode_access_rights(page_form.access_rights.data)
        
        status, message=update_page(idpage, page_form.title.data, page_form.url.data, page_form.content.data, html, is_public, is_private, page_form.isvisible.data)
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
                    return render_template("admin/page.jinja", title="Editace stránky", year=year, form=page_form, idpage=idpage) 

    return redirect (url_for("admin"+year['year']+".view_admin_pages"))

@admin.route("/admin/menu/", methods=["GET"])
@org_login_required
def view_admin_menu():
    year=get_year(request.blueprint)
    menu=get_menu(year)
    return render_template("admin/menu.jinja", title="Správa menu", year=year, menu=menu)

@admin.route("/admin/menu/<idmenu>", methods=["GET"])
@org_login_required
def view_menu_item(idmenu):
    year=get_year(request.blueprint)
    menuitem=get_menu_item(year, idmenu)
    pagetype, link, page, issystem = encode_menu_item(menuitem)

    menuitem_form = MenuItemForm()

    menuitem_form.order.data=menuitem['order']
    menuitem_form.menu.data=menuitem['menu']
    menuitem_form.link.data=link
    menuitem_form.isnewpart.data=menuitem['isnewpart']
    menuitem_form.current_year.data=menuitem['iscurrentyear']
    menuitem_form.isvisible.data=menuitem['isvisible']
    
    menuitem_form.pages.choices = [ (p['idpage'], p['title']) for p in get_admin_pages(year) ]
    menuitem_form.pages.choices.insert(0, (0, ''))

    menuitem_form.pagetype.process_data(pagetype)
    menuitem_form.pages.process_data(page)
    menuitem_form.access_rights.process_data(encode_access_rights(menuitem['ispublic'], menuitem['isprivate']))
    
    return render_template("admin/menu_item.jinja", title="Položka menu", year=year, form=menuitem_form, idmenu=idmenu)

@admin.route("/admin/menu/<int:idmenu>", methods=["POST"])
def edit_menu_item(idmenu):
    year=get_year(request.blueprint)
    
    menuitem_form = MenuItemForm(request.form)
    menuitem_form.pages.choices = [ (p['idpage'], p['title']) for p in get_admin_pages(year) ]
    menuitem_form.pages.choices.insert(0, (0, ''))

    if menuitem_form.validate():
        is_public, is_private=decode_access_rights(menuitem_form.access_rights.data)
        idpage, link, is_system = decode_menu_item(menuitem_form.pagetype.data, menuitem_form.pages.data, menuitem_form.link.data)
        
        status, message=update_menu_item(idmenu, year, idpage, menuitem_form.menu.data, link, 
                                         menuitem_form.order.data, menuitem_form.isnewpart.data, 
                                         is_public, is_private, menuitem_form.isvisible.data, is_system, menuitem_form.current_year.data)
        if not status:
           flash (message, "error")
        else:
            flash ('Položka menu upravena', "info")
    else:
        for _, errors in menuitem_form.errors.items():
            for error in errors:
                if isinstance(error, dict):
                    if (len(error)>0):
                        for k in error.keys():
                            flash (f'{error[k][0]}', "error")
                else:
                    flash (f'{error}', "error")
                    return render_template("admin/menu_item.jinja", title="Položka menu", year=year, form=menuitem_form, idmenu=idmenu)

    return redirect (url_for("admin"+year['year']+".view_admin_menu"))
    

@admin.route("/admin/menu/delete/<idmenu>", methods=["GET"])
@org_login_required
def view_menu_item_delete(idmenu):
    year=get_year(request.blueprint)
    menuitem=get_menu_item(year, idmenu)
    menuitem_delete_form = MenuItemDeleteForm()
    return render_template("admin/menu_item_delete.jinja", title="Smazání položky menu", year=year, form=menuitem_delete_form, menuitem=menuitem)

@admin.route("/admin/menu/delete/<idmenu>", methods=["POST"])
@org_login_required
def menu_item_delete(idmenu):
    year=get_year(request.blueprint)
    print ("abc")

    status, message = delete_menu_item(idmenu)
    if not status:
        flash (message, "error")
    else:
        flash ('Položka menu smazána', "info")
    return redirect (url_for("admin"+year['year']+".view_admin_menu"))
    
@admin.route("/admin/menu/add", methods=["GET"])
@org_login_required
def view_menu_item_add():
    year=get_year(request.blueprint)
    menuitem_form = MenuItemForm()
    
    menuitem_form.pages.choices = [ (p['idpage'], p['title']) for p in get_admin_pages(year) ]
    menuitem_form.pages.choices.insert(0, (0, ''))
    
    return render_template("admin/menu_item_create.jinja", title="Nová položka menu", year=year, form=menuitem_form)

@admin.route("/admin/menu/add", methods=["POST"])
def create_menu_item():
    year=get_year(request.blueprint)
    
    menuitem_form = MenuItemForm(request.form)
    menuitem_form.pages.choices = [ (p['idpage'], p['title']) for p in get_admin_pages(year) ]
    menuitem_form.pages.choices.insert(0, (0, ''))

    if menuitem_form.validate():
        is_public, is_private=decode_access_rights(menuitem_form.access_rights.data)
        idpage, link, is_system = decode_menu_item(menuitem_form.pagetype.data, menuitem_form.pages.data, menuitem_form.link.data)
        
        status, message=insert_menu_item(year, idpage, menuitem_form.menu.data, link, 
                                         menuitem_form.order.data, menuitem_form.isnewpart.data, 
                                         is_public, is_private, menuitem_form.isvisible.data, is_system, menuitem_form.current_year.data)
        if not status:
           flash (message, "error")
        else:
            flash ('Položka menu přidána', "info")
    else:
        for _, errors in menuitem_form.errors.items():
            for error in errors:
                if isinstance(error, dict):
                    if (len(error)>0):
                        for k in error.keys():
                            flash (f'{error[k][0]}', "error")
                else:
                    flash (f'{error}', "error")
                    return render_template("admin/menu_item_create.jinja", title="Nová položka menu", year=year, form=menuitem_form)

    return redirect (url_for("admin"+year['year']+".view_admin_menu"))
    