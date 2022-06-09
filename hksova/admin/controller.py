from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from ..year.model import *
from ..menu.model import *
from .form import *
from .model import *
from .utils import org_login_required

import mistune
from mistune.plugins import plugin_table

admin = Blueprint("admin", __name__)

@admin.route("/admin/pages/", methods=["GET"])
@org_login_required
def view_admin_pages():
    year=get_year(request.blueprint)
    menu=get_menu(year)
    pages=get_admin_pages(year)
    return render_template("admin/pages.jinja", title="Správa stránek", year=year, pages=pages, menu=menu)

@admin.route("/admin/page/<int:idpage>", methods=["GET"])
@org_login_required
def view_admin_page(idpage):
    year=get_year(request.blueprint)
    menu=get_menu(year)
    page_form = PageForm()
    page=get_admin_page(idpage)
    page_form.title.data=page['title']
    page_form.url.data=page['url']
    page_form.content.data=page['texy']
    page_form.isvisible.data=page['isvisible']
    page_form.access_rights.process_data(encode_access_rights(page['ispublic'], page['isprivate']))
    page_form.forum_section.choices = [ (p['idforumsection'], p['section']) for p in get_admin_forum_sections(year) ]
    page_form.forum_section.choices.insert(0, (0, ''))
    page_form.forum_section.process_data(page['idforumsection'])
    return render_template("admin/page.jinja", title="Editace stránky", year=year, form=page_form, idpage=idpage, menu=menu)

@admin.route("/admin/page/<int:idpage>", methods=["POST"])
def edit_page(idpage):
    year=get_year(request.blueprint)
    menu=get_menu(year) 
    page_form = PageForm(request.form)
    page_form.forum_section.choices = [ (p['idforumsection'], p['section']) for p in get_admin_forum_sections(year) ]
    page_form.forum_section.choices.insert(0, (0, ''))

    if page_form.validate():
        markdown = mistune.create_markdown(escape=False, plugins=['table'])
        html=markdown(page_form.content.data)
        is_public, is_private=decode_access_rights(page_form.access_rights.data)
        
        status, message=update_page(idpage, page_form.title.data, page_form.url.data, page_form.content.data, html, is_public, is_private, page_form.isvisible.data, page_form.forum_section.data)
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
                    return render_template("admin/page.jinja", title="Editace stránky", year=year, form=page_form, idpage=idpage, menu=menu) 

    return redirect (url_for("admin"+year['year']+".view_admin_pages"))

@admin.route("/admin/page/add", methods=["GET"])
@org_login_required
def view_page_add():
    year=get_year(request.blueprint)
    menu=get_menu(year)
    page_form = PageForm()
    page_form.forum_section.choices = [ (p['idforumsection'], p['section']) for p in get_admin_forum_sections(year) ]
    page_form.forum_section.choices.insert(0, (0, ''))
    return render_template("admin/page_create.jinja", title="Vytvoření stránky", year=year, form=page_form, menu=menu)

@admin.route("/admin/page/add", methods=["POST"])
def create_page():
    year=get_year(request.blueprint)
    menu=get_menu(year) 
    page_form = PageForm(request.form)
    page_form.forum_section.choices = [ (p['idforumsection'], p['section']) for p in get_admin_forum_sections(year) ]
    page_form.forum_section.choices.insert(0, (0, ''))

    if page_form.validate():
        markdown = mistune.create_markdown(escape=False, plugins=['table'])
        html=markdown(page_form.content.data)
        is_public, is_private=decode_access_rights(page_form.access_rights.data)
        
        status, message=insert_page(year, page_form.title.data, page_form.url.data, page_form.content.data, html, is_public, is_private, page_form.isvisible.data, page_form.forum_section.data)
        if not status:
           flash (message, "error")
        else:
            flash ('Stránka vytvořena', "info")
    else:
        for _, errors in page_form.errors.items():
            for error in errors:
                if isinstance(error, dict):
                    if (len(error)>0):
                        for k in error.keys():
                            flash (f'{error[k][0]}', "error")
                else:
                    flash (f'{error}', "error")
                    return render_template("admin/page_create.jinja", title="Nová stránka", year=year, form=page_form, menu=menu) 

    return redirect (url_for("admin"+year['year']+".view_admin_pages"))

@admin.route("/admin/page/delete/<int:idpage>", methods=["GET"])
@org_login_required
def view_page_delete(idpage):
    year=get_year(request.blueprint)
    menu=get_menu(year)
    page=get_admin_page(idpage)
    page_delete_form = PageDeleteForm()
    return render_template("admin/page_delete.jinja", title="Smazání stránky", year=year, form=page_delete_form, page=page, idpage=idpage, menu=menu)

@admin.route("/admin/page/delete/<int:idpage>", methods=["POST"])
@org_login_required
def page_delete(idpage):
    year=get_year(request.blueprint)
    status, message = delete_page(idpage)
    if not status:
        flash (message, "error")
    else:
        flash ('Stránka byla smazána', "info")
    return redirect (url_for("admin"+year['year']+".view_admin_pages"))

@admin.route("/admin/menu/", methods=["GET"])
@org_login_required
def view_admin_menu():
    year=get_year(request.blueprint)
    menu=get_menu(year)
    admin_menu=get_admin_menu(year)
    return render_template("admin/menu.jinja", title="Správa menu", year=year, admin_menu=admin_menu, menu=menu)

@admin.route("/admin/menu/<idmenu>", methods=["GET"])
@org_login_required
def view_menu_item(idmenu):
    year=get_year(request.blueprint)
    menu=get_menu(year)
    menuitem=get_admin_menu_item(year, idmenu)
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
    
    return render_template("admin/menu_item.jinja", title="Položka menu", year=year, form=menuitem_form, idmenu=idmenu, menu=menu)

@admin.route("/admin/menu/<int:idmenu>", methods=["POST"])
def edit_menu_item(idmenu):
    year=get_year(request.blueprint)
    menu=get_menu(year)
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
                    return render_template("admin/menu_item.jinja", title="Položka menu", year=year, form=menuitem_form, idmenu=idmenu, menu=menu)

    return redirect (url_for("admin"+year['year']+".view_admin_menu"))
    

@admin.route("/admin/menu/delete/<int:idmenu>", methods=["GET"])
@org_login_required
def view_menu_item_delete(idmenu):
    year=get_year(request.blueprint)
    menu=get_menu(year)
    menuitem=get_admin_menu_item(year, idmenu)
    menuitem_delete_form = MenuItemDeleteForm()
    return render_template("admin/menu_item_delete.jinja", title="Smazání položky menu", year=year, form=menuitem_delete_form, menuitem=menuitem, menu=menu)

@admin.route("/admin/menu/delete/<int:idmenu>", methods=["POST"])
@org_login_required
def menu_item_delete(idmenu):
    year=get_year(request.blueprint)
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
    menu=get_menu(year)
    menuitem_form = MenuItemForm()
    
    menuitem_form.pages.choices = [ (p['idpage'], p['title']) for p in get_admin_pages(year) ]
    menuitem_form.pages.choices.insert(0, (0, ''))
    
    return render_template("admin/menu_item_create.jinja", title="Nová položka menu", year=year, form=menuitem_form, menu=menu)

@admin.route("/admin/menu/add", methods=["POST"])
def create_menu_item():
    year=get_year(request.blueprint)
    menu=get_menu(year)
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
                    return render_template("admin/menu_item_create.jinja", title="Nová položka menu", year=year, form=menuitem_form, menu=menu)

    return redirect (url_for("admin"+year['year']+".view_admin_menu"))

@admin.route("/admin/forum/", methods=["GET"])
@org_login_required
def view_admin_forum_sections():
    year=get_year(request.blueprint)
    menu=get_menu(year)
    forum_sections=get_admin_forum_sections(year)
    return render_template("admin/forum_sections.jinja", title="Správa sekcí fóra", year=year, forum_sections=forum_sections, menu=menu)

@admin.route("/admin/forum/<int:idsection>", methods=["GET"])
@org_login_required
def view_admin_forum_section(idsection):
    year=get_year(request.blueprint)
    menu=get_menu(year)
    forum_section_form = ForumSectionForm()
    section=get_admin_forum_section(idsection)
    forum_section_form.section.data=section['section']
    forum_section_form.isvisible.data=section['isvisible']
    forum_section_form.order.data=section['order']
    return render_template("admin/forum_section.jinja", title="Editace sekce fóra", year=year, form=forum_section_form, idsection=idsection, menu=menu)

@admin.route("/admin/forum/<int:idsection>", methods=["POST"])
def edit_forum_section(idsection):
    year=get_year(request.blueprint)
    menu=get_menu(year) 
    forum_section_form = ForumSectionForm(request.form)
    if forum_section_form.validate():
        status, message=update_forum_section(idsection, forum_section_form.section.data, forum_section_form.order.data, forum_section_form.isvisible.data)
        if not status:
           flash (message, "error")
        else:
            flash ('Sekce upravena', "info")
    else:
        for _, errors in forum_section_form.errors.items():
            for error in errors:
                if isinstance(error, dict):
                    if (len(error)>0):
                        for k in error.keys():
                            flash (f'{error[k][0]}', "error")
                else:
                    flash (f'{error}', "error")
                    return render_template("admin/forum_section.jinja", title="Editace stránky", year=year, form=forum_section_form, idsection=idsection, menu=menu) 
    return redirect (url_for("admin"+year['year']+".view_admin_forum_sections"))

@admin.route("/admin/forum/add", methods=["GET"])
@org_login_required
def view_forum_section_add():
    year=get_year(request.blueprint)
    menu=get_menu(year)
    forum_section_form = ForumSectionForm()
    return render_template("admin/forum_section_create.jinja", title="Nová sekce fóra", year=year, form=forum_section_form, menu=menu)

@admin.route("/admin/forum/add", methods=["POST"])
def create_forum_section():
    year=get_year(request.blueprint)
    menu=get_menu(year)
    forum_section_form = ForumSectionForm(request.form)

    if forum_section_form.validate():
        status, message=insert_forum_section(year, forum_section_form.section.data, forum_section_form.order.data, forum_section_form.isvisible.data)
        if not status:
           flash (message, "error")
        else:
            flash ('Sekce fóra byla přidána', "info")
    else:
        for _, errors in forum_section_form.errors.items():
            for error in errors:
                if isinstance(error, dict):
                    if (len(error)>0):
                        for k in error.keys():
                            flash (f'{error[k][0]}', "error")
                else:
                    flash (f'{error}', "error")
                    return render_template("admin/forum_section_create.jinja", title="Nová sekce fóra", year=year, form=forum_section_form, menu=menu)

    return redirect (url_for("admin"+year['year']+".view_admin_forum_sections"))

@admin.route("/admin/forum/delete/<int:idsection>", methods=["GET"])
@org_login_required
def view_forum_section_delete(idsection):
    year=get_year(request.blueprint)
    menu=get_menu(year)
    forum_section=get_admin_forum_section(idsection)
    forum_section_delete_form = ForumSectionDeleteForm()
    return render_template("admin/forum_section_delete.jinja", title="Smazání položky menu", year=year, form=forum_section_delete_form, forum_section=forum_section, menu=menu)

@admin.route("/admin/forum/delete/<int:idsection>", methods=["POST"])
@org_login_required
def forum_section_delete(idsection):
    year=get_year(request.blueprint)
    status, message = delete_forum_section(idsection)
    if not status:
        flash (message, "error")
    else:
        flash ('Sekce fóra smazána', "info")
    return redirect (url_for("admin"+year['year']+".view_admin_forum_sections"))

@admin.route("/admin/changepassword/", methods=["GET"])
@org_login_required
def view_admin_password_change():
    year=get_year(request.blueprint)
    menu=get_menu(year)
    password_change_form = PasswordChangeForm()
    return render_template("admin/password_change.jinja", form=password_change_form, title="Změna hesla", year=year, menu=menu)

@admin.route("/admin/changepassword/", methods=["POST"])
@org_login_required
def admin_change_password():
    year=get_year(request.blueprint)
    menu=get_menu(year)
    valid=True
    password_change_form = PasswordChangeForm(request.form)

    if (password_change_form.password1.data != password_change_form.password2.data):
        valid=False
        flash (f'Zadaná hesla nejsou stejná.', "error")

    if password_change_form.validate() and valid:
        status, message= change_admin_pass(password_change_form.password_old.data, password_change_form.password1.data)
        if (status):
            flash("Změna hesla orga proběhla přihlášení", "info")
            return redirect (url_for("main.view_index"))
        else:
            flash(message, "error")
            return render_template("admin/password_change.jinja", form=password_change_form, year=year, menu=menu)
    else:
        for error in password_change_form.errors:
            flash (f'{error} nezadán', "error")
        return redirect (url_for("admin.view_password_change"))