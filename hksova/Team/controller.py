from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import flash

from .form import *
from .model import *
from ..Year.model import *

team = Blueprint("team", __name__)

@team.route("/login/", methods=["GET"])
def view_login():
    login_form = LoginForm()
    year=get_year(request.blueprint)
    return render_template("Team/login.jinja", form=login_form, title="Přihlášení", year=year)

@team.route("/login/", methods=["POST"])
def login_team():
    login_form = LoginForm(request.form)
    if login_form.validate():
        if (login_form.loginname.data=="admin" and login_form.password.data=="admin"):
            session["logged"] = True
            flash("Úspěšné přihlášení", "info")
            return redirect (url_for("main.view_index"))
        else:
            flash("Chybné uživatelské jméno nebo heslo.", "error")
            return render_template("Team/login.jinja", form=login_form)
    else:
        for error in login_form.errors:
            flash (f'{error} nezadán', "error")
            return redirect (url_for("Team/view_login"))

@team.route("/logout/", methods=["GET"])
def logout_team():
    session.pop("logged")
    flash("Úspěšné odhlášení", "info")
    return redirect (url_for("view_index"))

@team.route("/registration/", methods=["GET"])
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
        return render_template("Team/registration.jinja", form=registration_form, title="Registrace", year=year, reg_from=reg_from, reg_to=reg_to, min_players=min_players, max_players=max_players)
    else:
        return (render_template("Team/registration_close.jinja", reg_from=reg_from, reg_to=reg_to, title="Registrace", year=year))

@team.route("/registration/", methods=["POST"])
def register_team():
    year=get_year(request.blueprint)
    reg_from=get_registration_from(year)
    reg_to=get_registration_to(year)
    min_players=get_min_players(year)
    registration_form = RegistrationForm(request.form)

    if (not is_registration_open(year)):
        return (render_template("Team/registration_close.jinja", reg_from=reg_from, reg_to=reg_to, title="Registrace", year=year))

    if registration_form.validate():
        valid=True
    
        if ( not is_unique_name(year, registration_form.name.data)):
            valid=False
            flash (f'Zadané jméno týmu již existuje.', "error")

        if ( not is_unique_loginname(year, registration_form.name.data)):
            valid=False
            flash (f'Zadané jméno týmu již existuje.', "error")

        if ( not is_unique_email(year, registration_form.email.data)):
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
                session["logged"] = registration_form.name.data
                flash("Tým byl úspěšné registrován", "info")
                return redirect (url_for("main.view_index"))
        else:
            return render_template("Team/registration.jinja", form=registration_form, year=year)
    else:
        for _, errors in registration_form.errors.items():
            for error in errors:
                if isinstance(error, dict):
                    if (len(error)>0):
                        for k in error.keys():
                            flash (f'{error[k][0]}', "error")
                else:
                    flash (f'{error}', "error")
            
        return render_template("Team/registration.jinja", form=registration_form, year=year)


@team.route("/teams/", methods=["GET"])
def view_teams():
    year=get_year(request.blueprint)
    teams=get_teams(year)
#   print (teams)
    return render_template("Team/teams.jinja", title="Týmy", year=year, teams=teams)

