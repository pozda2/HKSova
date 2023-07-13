import base64
import io
import qrcode
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from ..year.model import get_year, get_years
from ..menu.model import get_menu
from ..settings.model import get_min_players, get_max_players, is_registration_open, get_registration_from, get_registration_to, get_payment_information

from .form import LoginForm, RegistrationForm, RegistrationCancelForm, EditTeamForm, PasswordChangeForm, ForgetPasswordForm, ResetPasswordForm
from .utils import login_required, current_year_required, send_reset_code
from .model import check_password_team, check_password_org, get_team, insert_team, update_team, get_team_by_email, get_team_by_reset_code
from .model import set_team_session, unset_team_session, generate_reset_code, change_team_pass, get_team_players, cancel_registration
from .model import reset_team_pass, get_teams_not_deleted, get_city_statistics, get_teams_statistics, get_players_statistics
from .model import is_unique_name, is_unique_email, is_unique_loginname, is_minimum_players

team_blueprint = Blueprint("team", __name__)


@team_blueprint.route("/login/", methods=["GET"])
@current_year_required
def view_login():
    login_form = LoginForm()
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    return render_template("team/login.jinja", form=login_form, title="Přihlášení", year=year, menu=menu, years=years)


@team_blueprint.route("/login/", methods=["POST"])
@current_year_required
def login_team():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)

    login_form = LoginForm(request.form)
    if login_form.validate():
        if check_password_team(year, login_form.loginname.data, login_form.password.data):
            team = get_team(year, login_form.loginname.data)
            set_team_session(year, team['name'], login_form.loginname.data, False)
            flash("Úspěšné přihlášení", "info")
            return redirect(url_for("main.view_index"))
        elif check_password_org(login_form.loginname.data, login_form.password.data):
            set_team_session(year, "org", "org", True)
            flash("Úspěšné přihlášení", "info")
            return redirect(url_for("main.view_index"))
        else:
            flash("Chybné uživatelské jméno nebo heslo.", "error")
            return render_template("team/login.jinja", form=login_form, year=year, menu=menu, years=years)
    else:
        for error in login_form.errors:
            flash(f'{error} nezadán', "error")
        return redirect(url_for("team.view_login"))


@team_blueprint.route("/logout/", methods=["GET"])
@login_required
@current_year_required
def logout_team():
    unset_team_session()
    flash("Úspěšné odhlášení", "info")
    return redirect(url_for("main.view_index"))


@team_blueprint.route("/changepassword/", methods=["GET"])
@login_required
@current_year_required
def view_password_change():
    password_change_form = PasswordChangeForm()
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    return render_template("team/password_change.jinja", form=password_change_form, title="Změna hesla", year=year, menu=menu, years=years)


@team_blueprint.route("/changepassword/", methods=["POST"])
@login_required
@current_year_required
def change_password():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    valid = True
    password_change_form = PasswordChangeForm(request.form)

    if password_change_form.password1.data != password_change_form.password2.data:
        valid = False
        flash('Zadaná hesla nejsou stejná.', "error")

    if password_change_form.validate() and valid:
        status, message = change_team_pass(year, session['login'], password_change_form.password_old.data, password_change_form.password1.data)
        if status:
            flash("Změna hesla proběhla přihlášení", "info")
            return redirect(url_for("main.view_index"))

        flash(message, "error")
        return render_template("team/password_change.jinja", form=password_change_form, year=year, menu=menu, years=years)
    else:
        for error in password_change_form.errors:
            flash(f'{error} nezadán', "error")
        return redirect(url_for("team.view_password_change"))


@team_blueprint.route("/forgetpassword/", methods=["GET"])
@current_year_required
def view_forget_password():
    forget_password_form = ForgetPasswordForm()
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    return render_template("team/password_forget.jinja", form=forget_password_form, title="Zapomenuté heslo", year=year, menu=menu, years=years)


@team_blueprint.route("/forgetpassword/", methods=["POST"])
@current_year_required
def forget_password():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    forget_password_form = ForgetPasswordForm(request.form)

    if forget_password_form.validate():
        team = get_team_by_email(year, forget_password_form.email.data)
        if team is None:
            flash("Neplatný kontaktní email", "error")
            return render_template("team/password_forget.jinja", form=forget_password_form, year=year, menu=menu, years=years)

        code, status, message = generate_reset_code(team['idteam'])
        if status:
            status, message = send_reset_code(year, code, team['login'], team['email'])
            if status:
                flash("Na kontaktní email byl odeslán odkaz na reset hesla.", "info")
            else:
                flash(f"Chyba při posílání emailu - {message}.", "error")
            return redirect(url_for("main.view_index"))
        else:
            flash(message, "error")
            return render_template("team/password_forget.jinja", form=forget_password_form, year=year, menu=menu, years=years)
    else:
        for error in forget_password_form.errors:
            flash(f'{error} nezadán', "error")
        return redirect(url_for("team.view_forget_password"))


@team_blueprint.route("/resetpassword/<resetcode>", methods=["GET"])
@current_year_required
def view_reset_password(resetcode):
    reset_password_form = ResetPasswordForm()
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    team = get_team_by_reset_code(resetcode)
    if team is None:
        return render_template("errors/404.jinja", year=year, menu=menu, years=years), 404

    return render_template("team/password_reset.jinja", form=reset_password_form, title="Reset hesla", year=year, menu=menu, years=years, team=team, resetcode=resetcode)


@team_blueprint.route("/resetpassword/<resetcode>", methods=["POST"])
@current_year_required
def reset_password(resetcode):
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    valid = True
    password_reset_form = ResetPasswordForm(request.form)

    team = get_team_by_reset_code(resetcode)
    if team is None:
        return render_template("errors/404.jinja", year=year, menu=menu, years=years), 404

    if password_reset_form.password1.data != password_reset_form.password2.data:
        valid = False
        flash('Zadaná hesla nejsou stejná.', "error")

    if password_reset_form.validate() and valid:
        status, message = reset_team_pass(team['idteam'], password_reset_form.password1.data)
        if status:
            flash("Reset hesla proběhl úspěšně", "info")
            return redirect(url_for("team.view_login"))
        else:
            flash(message, "error")
            return render_template("team/password_reset.jinja", form=password_reset_form, year=year, menu=menu, years=years, resetcode=resetcode)
    else:
        for error in password_reset_form.errors:
            flash(f'{error} nezadán', "error")
        return redirect(url_for("team.view_reset_password"))


@team_blueprint.route("/teams/", methods=["GET"])
def view_teams():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    teams = get_teams_not_deleted(year)
    city_stats = get_city_statistics(year)
    teams_stats = get_teams_statistics(year)
    players_stats = get_players_statistics(year)
    return render_template("team/teams.jinja", title="Týmy", year=year, menu=menu, years=years, teams=teams, city_stats=city_stats, teams_stats=teams_stats, players_stats=players_stats)


@team_blueprint.route("/team", methods=["GET"])
@login_required
@current_year_required
def view_team():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    team = get_team(year, session['login'])
    payment = get_payment_information(year)
    if payment['price'].isnumeric():
        qrcode_payment = f"SPD*1.0*ACC:{payment['iban']}*AM:{float(payment['price']):.2f}*CC:CZK*X-VS:{year['year']}{team['idteam']}*MSG:{team['name']}"
    else:
        qrcode_payment = "Zatím neplatte, sledujte informace na webu."
    return render_template("team/team.jinja", title="Údaje o týmu", year=year, team=team, payment=payment, menu=menu, years=years, qrcode_payment=qrcode_payment)


@team_blueprint.route("/registration/", methods=["GET"])
@current_year_required
def view_registration():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    reg_from = get_registration_from(year)
    reg_to = get_registration_to(year)
    min_players = get_min_players(year)
    max_players = get_max_players(year)
    registration_form = RegistrationForm()
    for _ in range(max_players):
        registration_form.players.append_entry()

    if is_registration_open(year):
        return render_template("team/registration.jinja", form=registration_form, title="Registrace", year=year, reg_from=reg_from, reg_to=reg_to, min_players=min_players, max_players=max_players, menu=menu, years=years)

    return render_template("team/registration_closed.jinja", reg_from=reg_from, reg_to=reg_to, title="Registrace", year=year, menu=menu, years=years)


@team_blueprint.route("/registration/", methods=["POST"])
@current_year_required
def register_team():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    reg_from = get_registration_from(year)
    reg_to = get_registration_to(year)
    min_players = get_min_players(year)
    registration_form = RegistrationForm(request.form)

    if not is_registration_open(year):
        return render_template("team/registration_close.jinja", reg_from=reg_from, reg_to=reg_to, title="Registrace", year=year, menu=menu, years=years)

    if registration_form.validate():
        valid = True

        if not is_unique_name(year, registration_form.name.data, None):
            valid = False
            flash('Zadané jméno týmu již existuje.', "error")

        if not is_unique_loginname(year, registration_form.loginname.data):
            valid = False
            flash('Zadané jméno týmu již existuje.', "error")

        if not is_unique_email(year, registration_form.email.data, None):
            valid = False
            flash('Zadaný email je již letos registrován.', "error")

        if registration_form.password.data != registration_form.password2.data:
            valid = False
            flash('Zadaná hesla nejsou stejná.', "error")

        if not is_minimum_players(registration_form.players.data, min_players):
            valid = False
            flash(f'V týmu musí být minimálně {min_players} hráčů', "error")

        if valid:
            status, error = insert_team(registration_form, year)
            if not status:
                flash(f'{error}', "error")
                return render_template("team/registration.jinja", form=registration_form, year=year, menu=menu, years=years)

            set_team_session(year, registration_form.name.data, registration_form.loginname.data, False)
            flash("Tým byl úspěšné registrován", "info")
            return redirect(url_for("main.view_index"))
        return render_template("team/registration.jinja", form=registration_form, year=year, menu=menu, years=years)
    else:
        for _, errors in registration_form.errors.items():
            for error in errors:
                if isinstance(error, dict):
                    if len(error) > 0:
                        for k in error.keys():
                            flash(f'{error[k][0]}', "error")
                else:
                    flash(f'{error}', "error")

        return render_template("team/registration.jinja", form=registration_form, year=year, menu=menu, years=years)


@team_blueprint.route("/registration_cancel/", methods=["GET"])
@login_required
@current_year_required
def view_registration_cancel():
    registration_cancel_form = RegistrationCancelForm()
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    return render_template("team/registration_cancel.jinja", form=registration_cancel_form, title="Zrušení registrace", year=year, menu=menu, years=years)


@team_blueprint.route("/registration_cancel/", methods=["POST"])
@login_required
@current_year_required
def registration_cancel():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    registration_cancel_form = RegistrationCancelForm(request.form)

    if registration_cancel_form.validate() and registration_cancel_form.agree.data:
        status, message = cancel_registration(year, session['login'])
        if status:
            unset_team_session()
            flash("Registrace týmu byla zrušena", "info")
            return redirect(url_for("main.view_index"))
        else:
            flash(message, "error")
            return render_template("team/registration_cancel.jinja", form=registration_cancel_form, year=year, menu=menu, years=years)
    else:
        for error in registration_cancel.errors:
            flash(f'{error} nezadán', "error")
        return redirect(url_for("team.view_registration_cancel"))


@team_blueprint.route("/edit_team/", methods=["GET"])
@login_required
@current_year_required
def view_edit_team():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    min_players = get_min_players(year)
    max_players = get_max_players(year)
    edit_team_form = EditTeamForm()
    for _ in range(max_players):
        edit_team_form.players.append_entry()

    team = get_team(year, session['login'])
    players = get_team_players(team['idteam'])
    edit_team_form['name'].data = team['name']
    edit_team_form['email'].data = team['email']
    edit_team_form['mobil'].data = team['mobil']
    edit_team_form['weburl'].data = team['weburl']
    edit_team_form['reporturl'].data = team['reporturl']

    for player in players:
        edit_team_form['players'][player['order']]['name'].data = player['name']
        edit_team_form['players'][player['order']]['publicname'].data = player['publicname']
        edit_team_form['players'][player['order']]['city'].data = player['city']
        edit_team_form['players'][player['order']]['age'].data = player['age']

    return render_template("team/edit_team.jinja", form=edit_team_form, title="Změna údajů", year=year, min_players=min_players, max_players=max_players, menu=menu, years=years)


@team_blueprint.route("/edit_team/", methods=["POST"])
@login_required
@current_year_required
def edit_team():
    year = get_year(request.blueprint)
    years = get_years()
    menu = get_menu(year)
    min_players = get_min_players(year)
    edit_team_form = EditTeamForm(request.form)

    if edit_team_form.validate():
        valid = True
        if not is_unique_name(year, edit_team_form.name.data, session["login"]):
            valid = False
            flash('Zadané jméno týmu již existuje.', "error")

        if not is_unique_email(year, edit_team_form.email.data, session["login"]):
            valid = False
            flash('Zadaný email je již letos registrován.', "error")

        if not is_minimum_players(edit_team_form.players.data, min_players):
            valid = False
            flash(f'V týmu musí být minimálně {min_players} hráčů', "error")

        if valid:
            status, error = update_team(edit_team_form, year, session['login'])
            if not status:
                flash(f'{error}', "error")
                return render_template("team/edit_team.jinja", form=edit_team_form, year=year, menu=menu, years=years)
            flash("Údaje o týmu byly úspěšně změněny", "info")
            return redirect(url_for("main.view_index"))

        return render_template("team/edit_team.jinja", form=edit_team_form, year=year, menu=menu, years=years)
    else:
        for _, errors in edit_team_form.errors.items():
            for error in errors:
                if isinstance(error, dict):
                    if len(error) > 0:
                        for k in error.keys():
                            flash(f'{error[k][0]}', "error")
                else:
                    flash(f'{error}', "error")

        return render_template("team/edit_team.jinja", form=edit_team_form, year=year, menu=menu, years=years)
