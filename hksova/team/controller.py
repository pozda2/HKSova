from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import flash

from .form import *
from .model import *
from ..year.model import *
from .utils import login_required, current_year_required

team = Blueprint("team", __name__)

@team.route("/login/", methods=["GET"])
@current_year_required
def view_login():
    login_form = LoginForm()
    year=get_year(request.blueprint)
    return render_template("team/login.jinja", form=login_form, title="Přihlášení", year=year)

@team.route("/login/", methods=["POST"])
@current_year_required
def login_team():
    year=get_year(request.blueprint)

    login_form = LoginForm(request.form)
    if login_form.validate():
        if (check_password_team(year, login_form.loginname.data, login_form.password.data)):
            team=get_team(year, login_form.loginname.data)
            set_team_session(year, team['name'], login_form.loginname.data, False)
            flash("Úspěšné přihlášení", "info")
            return redirect (url_for("main.view_index"))
        elif (check_password_org(login_form.loginname.data, login_form.password.data)):
            set_team_session(year, "org", "org", True)
            flash("Úspěšné přihlášení", "info")
            return redirect (url_for("main.view_index"))
        else:
            flash("Chybné uživatelské jméno nebo heslo.", "error")
            return render_template("team/login.jinja", form=login_form, year=year)
    else:
        for error in login_form.errors:
            flash (f'{error} nezadán', "error")
        return redirect (url_for("team.view_login"))

@team.route("/logout/", methods=["GET"])
@login_required
@current_year_required
def logout_team():
    unset_team_session()
    flash("Úspěšné odhlášení", "info")
    return redirect (url_for("main.view_index"))

@team.route("/teams/", methods=["GET"])
def view_teams():
    year=get_year(request.blueprint)
    teams=get_teams_not_deleted(year)
    return render_template("team/teams.jinja", title="Týmy", year=year, teams=teams)

@team.route("/changepassword/", methods=["GET"])
@login_required
@current_year_required
def view_password_change():
    password_change_form = PasswordChangeForm()
    year=get_year(request.blueprint)

    return render_template("team/password_change.jinja", form=password_change_form, title="Změna hesla", year=year)

@team.route("/changepassword/", methods=["POST"])
@login_required
@current_year_required
def change_password():
    year=get_year(request.blueprint)
    
    valid=True
    password_change_form = PasswordChangeForm(request.form)

    if (password_change_form.password1.data != password_change_form.password2.data):
        valid=False
        flash (f'Zadaná hesla nejsou stejná.', "error")

    if password_change_form.validate() and valid:
        status, message= change_team_pass(year, session['login'],password_change_form.password_old.data, password_change_form.password1.data)
        if (status):
            flash("Změna hesla proběhla přihlášení", "info")
            return redirect (url_for("main.view_index"))
        else:
            flash(message, "error")
            return render_template("team/password_change.jinja", form=password_change_form, year=year)
    else:
        for error in password_change_form.errors:
            flash (f'{error} nezadán', "error")
        return redirect (url_for("team.view_password_change"))

@team.route("/team", methods=["GET"])
@login_required
@current_year_required
def view_team():
    year=get_year(request.blueprint)
    team=get_team(year, session['login'])
    payment=get_payment_information(year)
    return render_template("team/team.jinja", title="Údaje o týmu", year=year, team=team, payment=payment)

@team.route("/registration/", methods=["GET"])
@current_year_required
def view_registration():
    year=get_year(request.blueprint)
    reg_from=get_registration_from(year)
    reg_to=get_registration_to(year)
    min_players=get_min_players(year)
    max_players=get_max_players(year)
    registration_form = RegistrationForm()
    for _ in range(max_players):
        registration_form.players.append_entry()

    if (is_registration_open(year)):
        return render_template("team/registration.jinja", form=registration_form, title="Registrace", year=year, reg_from=reg_from, reg_to=reg_to, min_players=min_players, max_players=max_players)
    else:
        return (render_template("team/registration_closed.jinja", reg_from=reg_from, reg_to=reg_to, title="Registrace", year=year))

@team.route("/registration/", methods=["POST"])
@current_year_required
def register_team():
    year=get_year(request.blueprint)
    reg_from=get_registration_from(year)
    reg_to=get_registration_to(year)
    min_players=get_min_players(year)
    registration_form = RegistrationForm(request.form)

    if (not is_registration_open(year)):
        return (render_template("team/registration_close.jinja", reg_from=reg_from, reg_to=reg_to, title="Registrace", year=year))

    if registration_form.validate():
        valid=True
    
        if ( not is_unique_name(year, registration_form.name.data, None)):
            valid=False
            flash (f'Zadané jméno týmu již existuje.', "error")

        if ( not is_unique_loginname(year, registration_form.loginname.data)):
            valid=False
            flash (f'Zadané jméno týmu již existuje.', "error")

        if ( not is_unique_email(year, registration_form.email.data, None)):
            valid=False
            flash (f'Zadaný email je již letos registrován.', "error")

        if (registration_form.password.data != registration_form.password2.data):
            valid=False
            flash (f'Zadaná hesla nejsou stejná.', "error")

        if ( not is_minimum_players(registration_form.players.data, min_players)):
            valid=False
            flash (f'V týmu musí být minimálně {min_players} hráčů', "error")
        
        if (valid):
            status, error = create_team(registration_form, year)
            if not status:
                flash (f'{error}', "error")
                return render_template("Team/registration.jinja", form=registration_form, year=year)
            else:
                set_team_session(year, registration_form.name.data, registration_form.loginname.data, False)
                flash("Tým byl úspěšné registrován", "info")
                return redirect (url_for("main.view_index"))
        else:
            return render_template("team/registration.jinja", form=registration_form, year=year)
    else:
        for _, errors in registration_form.errors.items():
            for error in errors:
                if isinstance(error, dict):
                    if (len(error)>0):
                        for k in error.keys():
                            flash (f'{error[k][0]}', "error")
                else:
                    flash (f'{error}', "error")
            
        return render_template("team/registration.jinja", form=registration_form, year=year)

@team.route("/registration_cancel/", methods=["GET"])
@login_required
@current_year_required
def view_registration_cancel():
    registration_cancel_form = RegistrationCancelForm()
    year=get_year(request.blueprint)
    return render_template("team/registration_cancel.jinja", form=registration_cancel_form, title="Zrušení registrace", year=year)

@team.route("/registration_cancel/", methods=["POST"])
@login_required
@current_year_required
def registration_cancel():
    year=get_year(request.blueprint)
    
    registration_cancel_form = RegistrationCancelForm(request.form)

    if registration_cancel_form.validate() and registration_cancel_form.agree.data:
        status, message = cancel_registration (year, session['login'])
        if (status):
            unset_team_session()
            flash("Registrace týmu byla zrušena", "info")
            return redirect (url_for("main.view_index"))
        else:
            flash(message, "error")
            return render_template("team/registration_cancel.jinja", form=registration_cancel_form, year=year)
    else:
        for error in registration_cancel.errors:
            flash (f'{error} nezadán', "error")
        return redirect (url_for("team.view_registration_cancel"))

@team.route("/edit_team/", methods=["GET"])
@login_required
@current_year_required
def view_edit_team():
    year=get_year(request.blueprint)

    min_players=get_min_players(year)
    max_players=get_max_players(year)
    edit_team_form = EditTeamForm()
    for _ in range(max_players):
        edit_team_form.players.append_entry()

    team = get_team(year, session['login'])
    players=get_team_players(team['idteam'])
    edit_team_form['name'].data=team['name']
    edit_team_form['email'].data=team['email']
    edit_team_form['mobil'].data=team['mobil']
    edit_team_form['weburl'].data=team['weburl']
    edit_team_form['reporturl'].data=team['reporturl']

    for player in players:
        edit_team_form['players'][player['order']]['name'].data = player['name']
        edit_team_form['players'][player['order']]['publicname'].data = player['publicname']
        edit_team_form['players'][player['order']]['city'].data = player['city']
        edit_team_form['players'][player['order']]['age'].data = player['age']

    return render_template("team/edit_team.jinja", form=edit_team_form, title="Změna údajů", year=year, min_players=min_players, max_players=max_players)

@team.route("/edit_team/", methods=["POST"])
@login_required
@current_year_required
def edit_team():
    year=get_year(request.blueprint)

    min_players=get_min_players(year)
    edit_team_form = EditTeamForm(request.form)

    if edit_team_form.validate():
        valid=True
        if ( not is_unique_name(year, edit_team_form.name.data, session["login"])):
            valid=False
            flash (f'Zadané jméno týmu již existuje.', "error")

        if ( not is_unique_email(year, edit_team_form.email.data, session["login"])):
            valid=False
            flash (f'Zadaný email je již letos registrován.', "error")

        if ( not is_minimum_players(edit_team_form.players.data, min_players)):
            valid=False
            flash (f'V týmu musí být minimálně {min_players} hráčů', "error")
        
        if (valid):
            status, error = save_team(edit_team_form, year, session['login'])
            if not status:
                flash (f'{error}', "error")
                return render_template("Team/edit_team.jinja", form=edit_team_form, year=year)
            else:
                flash("Údaje o týmu byly úspěšně změněny", "info")
                return redirect (url_for("main.view_index"))
        else:
            return render_template("team/edit_team.jinja", form=edit_team_form, year=year)
    else:
        for _, errors in edit_team_form.errors.items():
            for error in errors:
                if isinstance(error, dict):
                    if (len(error)>0):
                        for k in error.keys():
                            flash (f'{error[k][0]}', "error")
                else:
                    flash (f'{error}', "error")
            
        return render_template("team/edit_team.jinja", form=edit_team_form, year=year)