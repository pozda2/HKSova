'''
Page - controller
'''
from flask import Blueprint, render_template, make_response, request, session, send_from_directory

from flask_paginate import Pagination, get_page_parameter

from .model import get_page

from ..year.model import get_year, get_years
from ..menu.model import get_menu
from ..forum.model import get_forum, get_forum_post_count
from ..forum.form import PostForm
from ..team.model import get_reports
from ..puzzle.model import get_puzzles, get_puzzle_by_position
from ..puzzle.utils import get_puzzle_upload_dir
from ..settings.model import is_after_game_published

main_blueprint = Blueprint("main", __name__)

PUZZLE_FILE_FIELD = {'zadani': 'description', 'reseni': 'solution_instructions'}


def check_authorization(page):
    ispublic = page['ispublic']
    isprivate = page['isprivate']
    isvisible = page['isvisible']

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


def set_custom_headers(response):
    response.headers.set('X-Content-Type-Options', 'nosniff')
    response.headers.set('X-Frame-Options', 'SAMEORIGIN')


@main_blueprint.route("/")
def view_index():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    page = get_page(year, 'index')
    r = make_response(render_template("page/page.jinja", title=page['title'], page=page, year=year, menu=menu, years=years))
    set_custom_headers(r)
    return r


@main_blueprint.route("/<pageurl>")
def view_page(pageurl):
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    page = get_page(year, pageurl)

    # page exists
    if page is not None:
        #  authorize user
        if not check_authorization(page):
            return render_template("errors/404.jinja", year=year, menu=menu, years=years, page=page), 404

        # special page: with forum
        if page['idforumsection']:
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

            r = make_response(render_template("page/page_forum.jinja", title=page['title'], page=page, year=year, years=years, menu=menu, section=forum_section, pagination=pagination, form=post_form, section_id=section_id))
            set_custom_headers(r)
            return r

        # special page: with reports
        if pageurl == "reportaze":
            reports = get_reports(year)
            r = make_response(render_template("page/page_reports.jinja", title=page['title'], page=page, year=year, years=years, menu=menu, reports=reports))
            set_custom_headers(r)
            return r

        # special page: after-game puzzles overview (map + list), driven live by place/puzzle tables
        if pageurl == "po-hre":
            published = is_after_game_published(year)
            puzzles = get_puzzles(year) if published else []
            r = make_response(render_template("page/page_after_game.jinja", title=page['title'], page=page, year=year, years=years, menu=menu, puzzles=puzzles, published=published))
            set_custom_headers(r)
            return r

        # general page
        r = make_response(render_template("page/page.jinja", title=page['title'], page=page, year=year, years=years, menu=menu))
        set_custom_headers(r)
        return r

    # page does not exists
    return render_template("errors/404.jinja", year=year, menu=menu, years=years), 404


@main_blueprint.route("/po-hre/<int:position>")
def view_after_game_puzzle(position):
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)

    if not is_after_game_published(year):
        return render_template("errors/404.jinja", year=year, menu=menu, years=years), 404

    puzzle = get_puzzle_by_position(year, position)
    if puzzle is None:
        return render_template("errors/404.jinja", year=year, menu=menu, years=years), 404

    positions = [p['position'] for p in get_puzzles(year)]
    prev_position = max([p for p in positions if p < position], default=None)
    next_position = min([p for p in positions if p > position], default=None)

    section = None
    pagination = None
    post_form = None
    section_id = puzzle['id_forum_section']
    if section_id:
        post_count = get_forum_post_count(section_id)
        post_form = PostForm()
        search = bool(request.args.get('q'))

        if session.get("forum_name"):
            post_form.user.data = session['forum_name']
        elif session.get('team'):
            post_form.user.data = session['team']

        forum_page = request.args.get(get_page_parameter(), type=int, default=1)
        pagination = Pagination(page=forum_page, total=post_count, per_page=10, search=search, record_name='sections')
        section = get_forum(section_id, pagination.skip, 10)
        post_form.source_url = f"po-hre/{position}"

    r = make_response(render_template(
        "page/page_after_game_puzzle.jinja", title=puzzle['name'], puzzle=puzzle, year=year, years=years, menu=menu,
        prev_position=prev_position, next_position=next_position,
        section=section, pagination=pagination, form=post_form, section_id=section_id))
    set_custom_headers(r)
    return r


@main_blueprint.route("/po-hre/soubor/<int:position>/<kind>")
def download_after_game_puzzle_file(position, kind):
    year = get_year(request.blueprint)
    menu = get_menu(year)
    years = get_years()

    field = PUZZLE_FILE_FIELD.get(kind)
    if field is None or not is_after_game_published(year):
        return render_template("errors/404.jinja", year=year, menu=menu, years=years), 404

    puzzle = get_puzzle_by_position(year, position)
    filename = puzzle[field] if puzzle else None
    if not filename:
        return render_template("errors/404.jinja", year=year, menu=menu, years=years), 404

    return send_from_directory(get_puzzle_upload_dir(), filename, as_attachment=True)
