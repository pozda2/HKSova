import csv
import czech_sort
import io
import locale
import mistune
from datetime import datetime
from flask import Blueprint, Response, render_template, request, redirect, url_for, flash, session

from ..year.model import get_year, get_years
from ..menu.model import get_menu
from ..settings.model import get_min_players, get_max_players, get_trakar_token
from .form import PageForm, PageDeleteForm, MenuItemForm, MenuItemDeleteForm, ForumSectionForm, ForumSectionDeleteForm, PasswordChangeForm, EditTeamForm
from .form import SettingForm, SettingDeleteForm, GeneratingEmailsForm, MascotForm, MascotDeleteForm, NextYearForm, PlaceForm, PlaceDeleteForm
from .model import encode_access_rights, encode_menu_item, decode_access_rights, decode_menu_item
from .model import insert_forum_section, insert_mascot, insert_menu_item, insert_page, insert_setting, insert_place
from .model import update_admin_team, update_forum_section, update_mascot, update_menu_item, update_page, update_setting, update_place
from .model import delete_forum_section, delete_mascot, delete_menu_item, delete_page, delete_setting, delete_place
from .model import copy_year, change_admin_pass
from .model import sync_teams_trakar
from .model import get_admin_forum_section, get_admin_forum_sections, get_admin_menu, get_admin_menu_item, get_admin_page, get_admin_pages, get_admin_team, get_admin_teams
from .model import get_emails_list, get_mascot, get_mascots, get_setting, get_settings, get_team_players, get_place, get_places
from .model import is_minimum_players, is_unique_email, is_unique_name
from .utils import org_login_required


admin_blueprint = Blueprint("admin", __name__)


@admin_blueprint.route("/admin/pages/", methods=["GET"])
@org_login_required
def view_admin_pages():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    pages = get_admin_pages(year)
    return render_template("admin/pages.jinja", title="Správa stránek", year=year, pages=pages, menu=menu, years=years)


@admin_blueprint.route("/admin/page/<int:idpage>", methods=["GET"])
@org_login_required
def view_admin_page(idpage):
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    page_form = PageForm()
    page = get_admin_page(idpage)
    page_form.title.data = page['title']
    page_form.url.data = page['url']
    page_form.content.data = page['texy']
    page_form.isvisible.data = page['isvisible']
    page_form.access_rights.process_data(encode_access_rights(page['ispublic'], page['isprivate']))
    page_form.forum_section.choices = [(p['idforumsection'], p['section']) for p in get_admin_forum_sections(year)]
    page_form.forum_section.choices.insert(0, (0, ''))
    page_form.forum_section.process_data(page['idforumsection'])
    return render_template("admin/page.jinja", title="Editace stránky", year=year, form=page_form, idpage=idpage, menu=menu, years=years)


@admin_blueprint.route("/admin/page/<int:idpage>", methods=["POST"])
@org_login_required
def edit_page(idpage):
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    page_form = PageForm(request.form)
    page_form.forum_section.choices = [(p['idforumsection'], p['section']) for p in get_admin_forum_sections(year)]
    page_form.forum_section.choices.insert(0, (0, ''))

    if page_form.validate():
        markdown = mistune.create_markdown(escape=False, plugins=['table'])
        html = markdown(page_form.content.data)
        is_public, is_private = decode_access_rights(page_form.access_rights.data)

        status, message = update_page(idpage, page_form.title.data, page_form.url.data, page_form.content.data, html, is_public, is_private, page_form.isvisible.data, page_form.forum_section.data)
        if not status:
            flash(message, "error")
        else:
            flash('Stránka upravena', "info")
    else:
        for _, errors in page_form.errors.items():
            for error in errors:
                if isinstance(error, dict) and (len(error) > 0):
                    for k in error.keys():
                        flash(f'{error[k][0]}', "error")
                else:
                    flash(f'{error}', "error")
                    return render_template("admin/page.jinja", title="Editace stránky", year=year, form=page_form, idpage=idpage, menu=menu, years=years)

    if request.form['action'] == "save_and_page":
        return redirect(url_for("main" + year['year'] + ".view_page", pageurl=page_form.url.data))

    return redirect(url_for("admin" + year['year'] + ".view_admin_pages"))


@admin_blueprint.route("/admin/page/add", methods=["GET"])
@org_login_required
def view_page_add():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    page_form = PageForm()
    page_form.forum_section.choices = [(p['idforumsection'], p['section']) for p in get_admin_forum_sections(year)]
    page_form.forum_section.choices.insert(0, (0, ''))
    return render_template("admin/page_create.jinja", title="Vytvoření stránky", year=year, form=page_form, menu=menu, years=years)


@admin_blueprint.route("/admin/page/add", methods=["POST"])
@org_login_required
def create_page():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    page_form = PageForm(request.form)
    page_form.forum_section.choices = [(p['idforumsection'], p['section']) for p in get_admin_forum_sections(year)]
    page_form.forum_section.choices.insert(0, (0, ''))

    if page_form.validate():
        markdown = mistune.create_markdown(escape=False, plugins=['table'])
        html = markdown(page_form.content.data)
        is_public, is_private = decode_access_rights(page_form.access_rights.data)

        status, message = insert_page(year, page_form.title.data, page_form.url.data, page_form.content.data, html, is_public, is_private, page_form.isvisible.data, page_form.forum_section.data)
        if not status:
            flash(message, "error")
        else:
            flash('Stránka vytvořena', "info")
    else:
        for _, errors in page_form.errors.items():
            for error in errors:
                if isinstance(error, dict) and (len(error) > 0):
                    for k in error.keys():
                        flash(f'{error[k][0]}', "error")
                else:
                    flash(f'{error}', "error")
                    return render_template("admin/page_create.jinja", title="Nová stránka", year=year, form=page_form, menu=menu, years=years)

    return redirect(url_for("admin" + year['year'] + ".view_admin_pages"))


@admin_blueprint.route("/admin/page/delete/<int:idpage>", methods=["GET"])
@org_login_required
def view_page_delete(idpage):
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    page = get_admin_page(idpage)
    page_delete_form = PageDeleteForm()
    return render_template("admin/page_delete.jinja", title="Smazání stránky", year=year, form=page_delete_form, page=page, idpage=idpage, menu=menu, years=years)


@admin_blueprint.route("/admin/page/delete/<int:idpage>", methods=["POST"])
@org_login_required
def page_delete(idpage):
    year = get_year(request.blueprint)
    status, message = delete_page(idpage)
    if not status:
        flash(message, "error")
    else:
        flash('Stránka byla smazána', "info")
    return redirect(url_for("admin" + year['year'] + ".view_admin_pages"))


@admin_blueprint.route("/admin/menu/", methods=["GET"])
@org_login_required
def view_admin_menu():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    admin_menu = get_admin_menu(year)
    return render_template("admin/menu.jinja", title="Správa menu", year=year, admin_menu=admin_menu, menu=menu, years=years)


@admin_blueprint.route("/admin/menu/<idmenu>", methods=["GET"])
@org_login_required
def view_menu_item(idmenu):
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    menuitem = get_admin_menu_item(year, idmenu)
    pagetype, link, page, _ = encode_menu_item(menuitem)

    menuitem_form = MenuItemForm()

    menuitem_form.order.data = menuitem['order']
    menuitem_form.menu.data = menuitem['menu']
    menuitem_form.link.data = link
    menuitem_form.isnewpart.data = menuitem['isnewpart']
    menuitem_form.current_year.data = menuitem['iscurrentyear']
    menuitem_form.isvisible.data = menuitem['isvisible']

    menuitem_form.pages.choices = [(p['idpage'], p['title']) for p in get_admin_pages(year)]
    menuitem_form.pages.choices.insert(0, (0, ''))

    menuitem_form.pagetype.process_data(pagetype)
    menuitem_form.pages.process_data(page)
    menuitem_form.access_rights.process_data(encode_access_rights(menuitem['ispublic'], menuitem['isprivate']))

    return render_template("admin/menu_item.jinja", title="Položka menu", year=year, form=menuitem_form, idmenu=idmenu, menu=menu, years=years)


@admin_blueprint.route("/admin/menu/<int:idmenu>", methods=["POST"])
@org_login_required
def edit_menu_item(idmenu):
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    menuitem_form = MenuItemForm(request.form)
    menuitem_form.pages.choices = [(p['idpage'], p['title']) for p in get_admin_pages(year)]
    menuitem_form.pages.choices.insert(0, (0, ''))

    if menuitem_form.validate():
        is_public, is_private = decode_access_rights(menuitem_form.access_rights.data)
        idpage, link, is_system = decode_menu_item(menuitem_form.pagetype.data, menuitem_form.pages.data, menuitem_form.link.data)

        status, message = update_menu_item(idmenu, year, idpage, menuitem_form.menu.data, link,
                                           menuitem_form.order.data, menuitem_form.isnewpart.data,
                                           is_public, is_private, menuitem_form.isvisible.data, is_system, menuitem_form.current_year.data)
        if not status:
            flash(message, "error")
        else:
            flash('Položka menu upravena', "info")
    else:
        for _, errors in menuitem_form.errors.items():
            for error in errors:
                if isinstance(error, dict) and (len(error) > 0):
                    for k in error.keys():
                        flash(f'{error[k][0]}', "error")
                else:
                    flash(f'{error}', "error")
                    return render_template("admin/menu_item.jinja", title="Položka menu", year=year, form=menuitem_form, idmenu=idmenu, menu=menu, years=years)

    return redirect(url_for("admin" + year['year'] + ".view_admin_menu"))


@admin_blueprint.route("/admin/menu/delete/<int:idmenu>", methods=["GET"])
@org_login_required
def view_menu_item_delete(idmenu):
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    menuitem = get_admin_menu_item(year, idmenu)
    menuitem_delete_form = MenuItemDeleteForm()
    return render_template("admin/menu_item_delete.jinja", title="Smazání položky menu", year=year, form=menuitem_delete_form, menuitem=menuitem, menu=menu, years=years)


@admin_blueprint.route("/admin/menu/delete/<int:idmenu>", methods=["POST"])
@org_login_required
def menu_item_delete(idmenu):
    year = get_year(request.blueprint)
    status, message = delete_menu_item(idmenu)
    if not status:
        flash(message, "error")
    else:
        flash('Položka menu smazána', "info")
    return redirect(url_for("admin" + year['year'] + ".view_admin_menu"))


@admin_blueprint.route("/admin/menu/add", methods=["GET"])
@org_login_required
def view_menu_item_add():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    menuitem_form = MenuItemForm()

    menuitem_form.pages.choices = [(p['idpage'], p['title']) for p in get_admin_pages(year)]
    menuitem_form.pages.choices.insert(0, (0, ''))

    return render_template("admin/menu_item_create.jinja", title="Nová položka menu", year=year, form=menuitem_form, menu=menu, years=years)


@admin_blueprint.route("/admin/menu/add", methods=["POST"])
@org_login_required
def create_menu_item():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    menuitem_form = MenuItemForm(request.form)
    menuitem_form.pages.choices = [(p['idpage'], p['title']) for p in get_admin_pages(year)]
    menuitem_form.pages.choices.insert(0, (0, ''))

    if menuitem_form.validate():
        is_public, is_private = decode_access_rights(menuitem_form.access_rights.data)
        idpage, link, is_system = decode_menu_item(menuitem_form.pagetype.data, menuitem_form.pages.data, menuitem_form.link.data)

        status, message = insert_menu_item(year, idpage, menuitem_form.menu.data, link,
                                           menuitem_form.order.data, menuitem_form.isnewpart.data,
                                           is_public, is_private, menuitem_form.isvisible.data, is_system, menuitem_form.current_year.data)
        if not status:
            flash(message, "error")
        else:
            flash('Položka menu přidána', "info")
    else:
        for _, errors in menuitem_form.errors.items():
            for error in errors:
                if isinstance(error, dict) and (len(error) > 0):
                    for k in error.keys():
                        flash(f'{error[k][0]}', "error")
                else:
                    flash(f'{error}', "error")
                    return render_template("admin/menu_item_create.jinja", title="Nová položka menu", year=year, form=menuitem_form, menu=menu, years=years)

    return redirect(url_for("admin" + year['year'] + ".view_admin_menu"))


@admin_blueprint.route("/admin/forum/", methods=["GET"])
@org_login_required
def view_admin_forum_sections():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    forum_sections = get_admin_forum_sections(year)
    return render_template("admin/forum_sections.jinja", title="Správa sekcí fóra", year=year, forum_sections=forum_sections, menu=menu, years=years)


@admin_blueprint.route("/admin/forum/<int:idsection>", methods=["GET"])
@org_login_required
def view_admin_forum_section(idsection):
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    forum_section_form = ForumSectionForm()
    section = get_admin_forum_section(idsection)
    forum_section_form.section.data = section['section']
    forum_section_form.isvisible.data = section['isvisible']
    forum_section_form.order.data = section['order']
    return render_template("admin/forum_section.jinja", title="Editace sekce fóra", year=year, form=forum_section_form, idsection=idsection, menu=menu, years=years)


@admin_blueprint.route("/admin/forum/<int:idsection>", methods=["POST"])
@org_login_required
def edit_forum_section(idsection):
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    forum_section_form = ForumSectionForm(request.form)
    if forum_section_form.validate():
        status, message = update_forum_section(idsection, forum_section_form.section.data, forum_section_form.order.data, forum_section_form.isvisible.data)
        if not status:
            flash(message, "error")
        else:
            flash('Sekce upravena', "info")
    else:
        for _, errors in forum_section_form.errors.items():
            for error in errors:
                if isinstance(error, dict) and (len(error) > 0):
                    for k in error.keys():
                        flash(f'{error[k][0]}', "error")
                else:
                    flash(f'{error}', "error")
                    return render_template("admin/forum_section.jinja", title="Editace stránky", year=year, form=forum_section_form, idsection=idsection, menu=menu, years=years)
    return redirect(url_for("admin" + year['year'] + ".view_admin_forum_sections"))


@admin_blueprint.route("/admin/forum/add", methods=["GET"])
@org_login_required
def view_forum_section_add():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    forum_section_form = ForumSectionForm()
    return render_template("admin/forum_section_create.jinja", title="Nová sekce fóra", year=year, form=forum_section_form, menu=menu, years=years)


@admin_blueprint.route("/admin/forum/add", methods=["POST"])
@org_login_required
def create_forum_section():
    year = get_year(request.blueprint)
    menu = get_menu(year)
    forum_section_form = ForumSectionForm(request.form)

    if forum_section_form.validate():
        status, message = insert_forum_section(year, forum_section_form.section.data, forum_section_form.order.data, forum_section_form.isvisible.data)
        if not status:
            flash(message, "error")
        else:
            flash('Sekce fóra byla přidána', "info")
    else:
        for _, errors in forum_section_form.errors.items():
            for error in errors:
                if isinstance(error, dict) and (len(error) > 0):
                    for k in error.keys():
                        flash(f'{error[k][0]}', "error")
                else:
                    flash(f'{error}', "error")
                    return render_template("admin/forum_section_create.jinja", title="Nová sekce fóra", year=year, form=forum_section_form, menu=menu)

    return redirect(url_for("admin" + year['year'] + ".view_admin_forum_sections"))


@admin_blueprint.route("/admin/forum/delete/<int:idsection>", methods=["GET"])
@org_login_required
def view_forum_section_delete(idsection):
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    forum_section = get_admin_forum_section(idsection)
    forum_section_delete_form = ForumSectionDeleteForm()
    return render_template("admin/forum_section_delete.jinja", title="Smazání položky menu", year=year, form=forum_section_delete_form, forum_section=forum_section, menu=menu, years=years)


@admin_blueprint.route("/admin/forum/delete/<int:idsection>", methods=["POST"])
@org_login_required
def forum_section_delete(idsection):
    year = get_year(request.blueprint)
    status, message = delete_forum_section(idsection)
    if not status:
        flash(message, "error")
    else:
        flash('Sekce fóra smazána', "info")
    return redirect(url_for("admin" + year['year'] + ".view_admin_forum_sections"))


@admin_blueprint.route("/admin/changepassword/", methods=["GET"])
@org_login_required
def view_admin_password_change():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    password_change_form = PasswordChangeForm()
    return render_template("admin/password_change.jinja", form=password_change_form, title="Změna hesla", year=year, menu=menu, years=years)


@admin_blueprint.route("/admin/changepassword/", methods=["POST"])
@org_login_required
def admin_change_password():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    valid = True
    password_change_form = PasswordChangeForm(request.form)

    if password_change_form.password1.data != password_change_form.password2.data:
        valid = False
        flash('Zadaná hesla nejsou stejná.', "error")

    if password_change_form.validate() and valid:
        status, message = change_admin_pass(password_change_form.password_old.data, password_change_form.password1.data)
        if status:
            flash("Změna hesla orga proběhla přihlášení", "info")
            return redirect(url_for("main.view_index"))

        flash(message, "error")
        return render_template("admin/password_change.jinja", form=password_change_form, year=year, menu=menu, years=years)

    for error in password_change_form.errors:
        flash(f'{error} nezadán', "error")
    return redirect(url_for("admin.view_password_change"))


@admin_blueprint.route("/admin/links/", methods=["GET"])
@org_login_required
def view_admin_links():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    trakar_token = get_trakar_token(year)
    return render_template("admin/links.jinja", title="Užitečné odkazy", year=year, menu=menu, years=years, trakar_token=trakar_token)


@admin_blueprint.route("/admin/teams/sync", methods=["GET"])
@org_login_required
def sync_admin_teams():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    teams = get_admin_teams(year)
    sync_stat = sync_teams_trakar(year, teams)
    return render_template("admin/teams.jinja", title="Správa týmů", year=year, teams=teams, menu=menu, years=years, sync_stat=sync_stat)


@admin_blueprint.route("/admin/teams/", methods=["GET"])
@org_login_required
def view_admin_teams():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    teams = get_admin_teams(year)
    return render_template("admin/teams.jinja", title="Správa týmů", year=year, teams=teams, menu=menu, years=years)


@admin_blueprint.route("/admin/team/<int:idteam>", methods=["GET"])
@org_login_required
def view_admin_team(idteam):
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    team = get_admin_team(idteam)
    min_players = get_min_players(year)
    max_players = get_max_players(year)
    players = get_team_players(idteam)

    edit_team_form = EditTeamForm()
    for _ in range(max_players):
        edit_team_form.players.append_entry()

    edit_team_form.name.data = team['name']
    edit_team_form.login.data = team['login']
    edit_team_form.email.data = team['email']
    edit_team_form.mobil.data = team['mobil']
    edit_team_form.weburl.data = team['weburl']
    edit_team_form.reporturl.data = team['reporturl']
    edit_team_form.ispaid.data = team['ispaid']
    edit_team_form.isdeleted.data = team['isdeleted']
    edit_team_form.isbackup.data = team['isbackup']

    # patch for old years
    shift = 0
    for player in players:
        if player['order'] == 5:
            shift = 1

    for player in players:
        edit_team_form['players'][player['order'] - shift]['name'].data = player['name']
        edit_team_form['players'][player['order'] - shift]['publicname'].data = player['publicname']
        edit_team_form['players'][player['order'] - shift]['city'].data = player['city']
        edit_team_form['players'][player['order'] - shift]['age'].data = player['age']

    return render_template("admin/team.jinja", title="Údaje o týmu", year=year, form=edit_team_form, team=team, menu=menu, min_players=min_players, years=years)


@admin_blueprint.route("/admin/team/<int:idteam>", methods=["POST"])
@org_login_required
def edit_admin_team(idteam):
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    min_players = get_min_players(year)
    edit_team_form = EditTeamForm(request.form)
    team = get_admin_team(idteam)

    if edit_team_form.validate():
        valid = True
        if not is_unique_name(year, edit_team_form.name.data, edit_team_form.login.data):
            valid = False
            flash('Zadané jméno týmu již existuje.', "error")

        if not is_unique_email(year, edit_team_form.email.data, edit_team_form.login.data):
            valid = False
            flash('Zadaný email je již letos registrován.', "error")

        if not is_minimum_players(edit_team_form.players.data, min_players):
            valid = False
            flash('V týmu musí být minimálně {min_players} hráčů', "error")

        if valid:
            status, error = update_admin_team(idteam, year, edit_team_form.login.data, edit_team_form.name.data, edit_team_form.email.data, edit_team_form.mobil.data,
                                              edit_team_form.weburl.data, edit_team_form.reporturl.data, edit_team_form.ispaid.data, edit_team_form.isdeleted.data, edit_team_form.isbackup.data,
                                              edit_team_form.players.data)
            if not status:
                flash(f'{error}', "error")
                return render_template("admin/team.jinja", form=edit_team_form, year=year, menu=menu, team=team, years=years)

            flash("Údaje o týmu byly úspěšně změněny", "info")
            return redirect(url_for("admin" + year['year'] + ".view_admin_teams"))

        return render_template("admin/team.jinja", form=edit_team_form, year=year, menu=menu, team=team, years=years)
    else:
        for _, errors in edit_team_form.errors.items():
            for error in errors:
                if isinstance(error, dict) and (len(error) > 0):
                    for k in error.keys():
                        flash(f'{error[k][0]}', "error")
                else:
                    flash(f'{error}', "error")

        return render_template("admin/team.jinja", form=edit_team_form, year=year, menu=menu, team=team, years=years)


@admin_blueprint.route("/admin/settings/", methods=["GET"])
@org_login_required
def view_settings():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    settings = get_settings(year)
    return render_template("admin/settings.jinja", title="Správa nastavení", year=year, settings=settings, menu=menu, years=years)


@admin_blueprint.route("/admin/settings/add", methods=["GET"])
@org_login_required
def view_setting_add():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    settings_form = SettingForm()
    return render_template("admin/setting_create.jinja", title="Nové nastavení", year=year, form=settings_form, menu=menu, years=years)


@admin_blueprint.route("/admin/settings/add", methods=["POST"])
@org_login_required
def create_setting():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    settings_form = SettingForm(request.form)

    if settings_form.validate():
        status, message = insert_setting(year, settings_form.param.data, settings_form.value.data)
        if not status:
            flash(message, "error")
        else:
            flash('Nastavení bylo přidáno', "info")
    else:
        for _, errors in settings_form.errors.items():
            for error in errors:
                if isinstance(error, dict) and (len(error) > 0):
                    for k in error.keys():
                        flash(f'{error[k][0]}', "error")
                else:
                    flash(f'{error}', "error")
                    return render_template("admin/setting_create.jinja", title="Nové nastavení", year=year, form=settings_form, menu=menu, years=years)

    return redirect(url_for("admin" + year['year'] + ".view_settings"))


@admin_blueprint.route("/admin/settings/<int:idsetting>", methods=["GET"])
@org_login_required
def view_setting(idsetting):
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    setting = get_setting(idsetting)
    setting_form = SettingForm()
    setting_form.param.data = setting['param']
    setting_form.value.data = setting['value']
    return render_template("admin/setting.jinja", title="Editace nastavení", year=year, form=setting_form, idsetting=idsetting, menu=menu, years=years)


@admin_blueprint.route("/admin/settings/<int:idsetting>", methods=["POST"])
@org_login_required
def edit_setting(idsetting):
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    setting_form = SettingForm(request.form)
    if setting_form.validate():
        status, message = update_setting(idsetting, setting_form.param.data, setting_form.value.data)
        if not status:
            flash(message, "error")
        else:
            flash('Nastavení upraveno', "info")
    else:
        for _, errors in setting_form.errors.items():
            for error in errors:
                if isinstance(error, dict) and (len(error) > 0):
                    for k in error.keys():
                        flash(f'{error[k][0]}', "error")
                else:
                    flash(f'{error}', "error")
                    return render_template("admin/setting.jinja", title="Editace nastavení", year=year, form=setting_form, idsetting=idsetting, menu=menu, years=years)
    return redirect(url_for("admin" + year['year'] + ".view_settings"))


@admin_blueprint.route("/admin/settings/delete/<int:idsetting>", methods=["GET"])
@org_login_required
def view_setting_delete(idsetting):
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    setting = get_setting(idsetting)
    setting_delete_form = SettingDeleteForm()
    return render_template("admin/setting_delete.jinja", title="Smazání parametru", year=year, form=setting_delete_form, setting=setting, menu=menu, years=years)


@admin_blueprint.route("/admin/settings/delete/<int:idsetting>", methods=["POST"])
@org_login_required
def setting_delete(idsetting):
    year = get_year(request.blueprint)
    status, message = delete_setting(idsetting)
    if not status:
        flash(message, "error")
    else:
        flash('Parametr z nastavení smazán', "info")
    return redirect(url_for("admin" + year['year'] + ".view_settings"))


@admin_blueprint.route("/admin/emails/", methods=["GET"])
@org_login_required
def view_generating_emails():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    email_form = GeneratingEmailsForm()
    return render_template("admin/emails_filter.jinja", title="Generování seznamu emailů", year=year, form=email_form, menu=menu, years=years)


@admin_blueprint.route("/admin/emails/", methods=["POST"])
@org_login_required
def generating_emails():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    email_form = GeneratingEmailsForm()

    if email_form.validate():
        email_list, status, message = get_emails_list(year, email_form.filter.data)
        if not status:
            flash(message, "error")
        else:
            lists = []
            _list = ""
            for i, email in enumerate(email_list):
                if i % 40 == 0:
                    lists.append(_list)
                    _list = ""
                    _list += email['email']
                else:
                    _list += ", " + email['email']
            lists.append(_list)

            return render_template("admin/emails.jinja", title="Seznamu emailů", year=year, menu=menu, years=years, email_list=lists)
    else:
        for _, errors in email_form.errors.items():
            for error in errors:
                if isinstance(error, dict) and len(error) > 0:
                    for k in error.keys():
                        flash(f'{error[k][0]}', "error")
                else:
                    flash(f'{error}', "error")
                    return render_template("admin/emails_filter.jinja", title="Generování seznamu emailů", year=year, form=email_form, menu=menu, years=years)
    return render_template("admin/emails_filter.jinja", title="Generování seznamu emailů", year=year, form=email_form, menu=menu, years=years)


@admin_blueprint.route("/admin/export/csv", methods=["GET"])
@org_login_required
def export_csv():
    year = get_year(request.blueprint)
    teams = get_admin_teams(year)
    output = io.StringIO()
    csv.register_dialect('sova', delimiter=';', quoting=csv.QUOTE_MINIMAL)
    writer = csv.writer(output, dialect='sova')

    # header
    line = ['Jméno', 'Maskot', 'Mobil', 'Email', 'Zaplaceno', 'Stav', 'Hráči']
    writer.writerow(line)

    # content
    locale.setlocale(locale.LC_ALL, 'cs_CZ.UTF-8')
    for team in sorted(teams, key=lambda x: locale.strxfrm(x['name'].lower())):
        if team['isdeleted'] == 1:
            continue
        line = [team['name'], team['mascot'], team['mobil'], team['email'], team['zaplaceno'], team['stav'], team['players_private']]
        writer.writerow(line)

    dstr = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    output.seek(0)
    return Response(output, mimetype="text/csv", headers={"Content-Disposition": f"attachment;filename=sova-teams-export_{dstr}.csv"})
    # return Response(output, mimetype="text/plain", headers={})


@admin_blueprint.route("/admin/export/envelope", methods=["GET"])
@org_login_required
def export_envelope():
    year = get_year(request.blueprint)
    teams = get_admin_teams(year)
    output = io.StringIO()
    csv.register_dialect('sova', delimiter=';', quoting=csv.QUOTE_MINIMAL)
    writer = csv.writer(output, dialect='sova')

    # header
    line = ['Jméno', 'Maskot', 'Mobil', 'Email', 'Zaplaceno', 'Stav', 'Hráči']
    writer.writerow(line)

    # content
    locale.setlocale(locale.LC_ALL, 'cs_CZ.UTF-8')
    teams_output = []
    # for team in sorted(teams, key=lambda x: locale.strxfrm(x['name'].lower())):
    for team in sorted(teams, key=lambda x: czech_sort.key(x['name'].lower())):
        if team['isdeleted'] == 1:
            continue
        line = [team['name'], team['mascot'], team['mobil'], team['email'], team['zaplaceno'], team['stav'], team['players_private']]
        writer.writerow(line)
        teams_output.append(team)
        print(team['name'])

    # output.seek(0)
    # return Response(output, mimetype="text/csv", headers={"Content-Disposition": f"attachment;filename=sova-teams-export_{dstr}.csv"})
    # return Response(output, mimetype="text/plain", headers={})
    return render_template("admin/envelopes.jinja", title="Tisk startovních obálek", year=year, teams=teams_output)


@admin_blueprint.route("/admin/mascots/", methods=["GET"])
@org_login_required
def view_admin_mascots():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    mascots = get_mascots()
    return render_template("admin/mascots.jinja", title="Správa maskotů", year=year, menu=menu, years=years, mascots=mascots)


@admin_blueprint.route("/admin/mascot/add", methods=["GET"])
@org_login_required
def view_mascot_add():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    mascot_form = MascotForm()
    return render_template("admin/mascot_create.jinja", title="Nový maskot", year=year, form=mascot_form, menu=menu, years=years)


@admin_blueprint.route("/admin/mascot/add", methods=["POST"])
@org_login_required
def create_mascot():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    mascot_form = MascotForm(request.form)

    if mascot_form.validate():
        status, message = insert_mascot(mascot_form.mascot.data)
        if not status:
            flash(message, "error")
        else:
            flash('Maskot byl přidán', "info")
    else:
        for _, errors in mascot_form.errors.items():
            for error in errors:
                if isinstance(error, dict) and (len(error) > 0):
                    for k in error.keys():
                        flash(f'{error[k][0]}', "error")
                else:
                    flash(f'{error}', "error")
                    return render_template("admin/mascot_create.jinja", title="Nový maskot", year=year, form=mascot_form, menu=menu, years=years)

    return redirect(url_for("admin" + year['year'] + ".view_admin_mascots"))


@admin_blueprint.route("/admin/mascots/<mascot>", methods=["GET"])
@org_login_required
def view_mascot(mascot):
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    mascot = get_mascot(mascot)
    if not mascot:
        return render_template("errors/404.jinja", year=year, menu=menu, years=years), 404
    mascot_form = MascotForm()
    mascot_form.mascot.data = mascot['mascot']
    return render_template("admin/mascot.jinja", title="Editace maskota", year=year, form=mascot_form, oldmascot=mascot, menu=menu, years=years)


@admin_blueprint.route("/admin/mascots/<oldmascot>", methods=["POST"])
@org_login_required
def edit_mascot(oldmascot):
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    mascot_form = MascotForm(request.form)
    if mascot_form.validate():
        status, message = update_mascot(oldmascot, mascot_form.mascot.data)
        if not status:
            flash(message, "error")
        else:
            flash('Maskot upraven', "info")
    else:
        for _, errors in mascot_form.errors.items():
            for error in errors:
                if isinstance(error, dict) and (len(error) > 0):
                    for k in error.keys():
                        flash(f'{error[k][0]}', "error")
                else:
                    flash(f'{error}', "error")
                    return render_template("admin/mascot.jinja", title="Editace maskota", year=year, form=mascot_form, oldmascot=oldmascot, menu=menu, years=years)
    return redirect(url_for("admin" + year['year'] + ".view_admin_mascots"))


@admin_blueprint.route("/admin/mascots/delete/<mascot>", methods=["GET"])
@org_login_required
def view_mascot_delete(mascot):
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    mascot = get_mascot(mascot)
    if not mascot:
        return render_template("errors/404.jinja", year=year, menu=menu, years=years), 404

    mascot_delete_form = MascotDeleteForm()
    return render_template("admin/mascot_delete.jinja", title="Smazání maskota", year=year, form=mascot_delete_form, mascot=mascot, menu=menu, years=years)


@admin_blueprint.route("/admin/mascots/delete/<mascot>", methods=["POST"])
@org_login_required
def mascot_delete(mascot):
    year = get_year(request.blueprint)
    status, message = delete_mascot(mascot)
    if not status:
        flash(message, "error")
    else:
        flash('Maskot smazán', "info")
    return redirect(url_for("admin" + year['year'] + ".view_admin_mascots"))


@admin_blueprint.route("/admin/next_year/", methods=["GET"])
@org_login_required
def view_admin_next_year():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    next_year_id = int(year['year']) + 1
    next_year_form = NextYearForm()
    return render_template("admin/next_year.jinja", title="Nový ročník", year=year, menu=menu, years=years, next_year=next_year_id, form=next_year_form)


@admin_blueprint.route("/admin/next_year", methods=["POST"])
@org_login_required
def next_year():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    next_year_form = NextYearForm(request.form)
    next_year_id = int(year['year']) + 1

    if next_year_form.validate():
        status, message = copy_year(year, next_year_id)
        if not status:
            flash(message, "error")
        else:
            flash('Založen nový ročník. Restartuj aplikaci', "info")
    else:
        for _, errors in next_year_form.errors.items():
            for error in errors:
                if isinstance(error, dict) and (len(error) > 0):
                    for k in error.keys():
                        flash(f'{error[k][0]}', "error")
                else:
                    flash(f'{error}', "error")
                    return render_template("admin/next_year.jinja", title="Nový ročník", year=year, form=next_year_form, menu=menu, years=years, next_year=next_year_id)

    return redirect(url_for("main" + str(next_year_id) + ".view_page", pageurl='/'))


@admin_blueprint.route("/admin/switch_team/<int:idteam>", methods=["GET"])
@org_login_required
def switch_team(idteam):
    team = get_admin_team(idteam)
    if team is None:
        flash('Tým nenalezen', "error")
    else:
        flash(f'Přepnuto na tým {team["name"]}.', "info")
        session["org"] = False
        session["logged"] = True
        session["login"] = team['login']
        session["team"] = team['name']
        if team['ispaid'] == 0:
            session["ispaid"] = False
        else:
            session["ispaid"] = True
        if team['isbackup'] == 0:
            session["isbackup"] = False
        else:
            session["isbackup"] = True
    return redirect(url_for("main.view_index"))


@admin_blueprint.route("/admin/places/", methods=["GET"])
@org_login_required
def view_admin_places():
    year = get_year(request.blueprint)
    places = get_places(year['year'])
    return render_template("admin/places.jinja", title="Správa stanovišť", year=year, places=places)


@admin_blueprint.route("/admin/place/add", methods=["GET"])
@org_login_required
def view_place_add():
    year = get_year(request.blueprint)
    place_form = PlaceForm()
    return render_template("admin/place_create.jinja", title="Nové stanoviště", year=year, form=place_form)


@admin_blueprint.route("/admin/place/delete/<int:place_id>", methods=["GET"])
@org_login_required
def view_place_delete(place_id):
    year = get_year(request.blueprint)
    place = get_place(place_id)
    if not place:
        return render_template("errors/404.jinja", year=year), 404

    place_delete_form = PlaceDeleteForm()
    return render_template("admin/place_delete.jinja", title="Smazání maskota", year=year, form=place_delete_form, place=place)


@admin_blueprint.route("/admin/place/add", methods=["POST"])
@org_login_required
def create_place():
    year = get_year(request.blueprint)
    place_form = PlaceForm(request.form)

    if place_form.validate():
        status, message = insert_place(year['year'], place_form.name.data, place_form.latitude.data, place_form.longitude.data)
        if not status:
            flash(message, "error")
        else:
            flash('Stanoviště bylo přidáno', "info")
    else:
        for _, errors in place_form.errors.items():
            for error in errors:
                if isinstance(error, dict) and (len(error) > 0):
                    for k in error.keys():
                        flash(f'{error[k][0]}', "error")
                else:
                    flash(f'{error}', "error")
                    return render_template("admin/place_create.jinja", title="Nové stanoviště", year=year, form=place_form)

    return redirect(url_for("admin" + year['year'] + ".view_admin_places"))


@admin_blueprint.route("/admin/place/<int:place_id>", methods=["GET"])
@org_login_required
def view_place(place_id):
    year = get_year(request.blueprint)
    place = get_place(place_id)
    if not place:
        return render_template("errors/404.jinja", year=year), 404
    place_form = PlaceForm()
    place_form.name.data = place['name']
    place_form.latitude.data = place['latitude']
    place_form.longitude.data = place['longitude']
    return render_template("admin/place.jinja", title="Editace stanoviště", year=year, form=place_form, place=place)


@admin_blueprint.route("/admin/place/<int:place_id>", methods=["POST"])
@org_login_required
def edit_place(place_id):
    year = get_year(request.blueprint)
    place_form = PlaceForm(request.form)
    if place_form.validate():
        status, message = update_place(place_id, place_form.name.data, place_form.latitude.data, place_form.longitude.data)
        if not status:
            flash(message, "error")
        else:
            flash('Stanoviště upraveno', "info")
    else:
        for _, errors in place_form.errors.items():
            for error in errors:
                if isinstance(error, dict) and (len(error) > 0):
                    for k in error.keys():
                        flash(f'{error[k][0]}', "error")
                else:
                    flash(f'{error}', "error")
                    return render_template("admin/place.jinja", title="Editace stanoviště", year=year)
    return redirect(url_for("admin" + year['year'] + ".view_admin_places"))


@admin_blueprint.route("/admin/place/delete/<int:place_id>", methods=["POST"])
@org_login_required
def place_delete(place_id):
    year = get_year(request.blueprint)
    status, message = delete_place(place_id)
    if not status:
        flash(message, "error")
    else:
        flash('Stanoviště smazáno', "info")
    return redirect(url_for("admin" + year['year'] + ".view_admin_places"))


@admin_blueprint.route("/admin/puzzles/", methods=["GET"])
@org_login_required
def view_admin_puzzles():
    # year = get_year(request.blueprint)
    # years = get_years()
    # menu = get_menu(year)
    # mascots = get_mascots()
    # return render_template("admin/mascots.jinja", title="Správa maskotů", year=year, menu=menu, years=years, mascots=mascots)
    print('TBD puzzles')