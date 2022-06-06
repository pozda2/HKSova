from flask import session
from flask import redirect
from flask import url_for
from flask import flash
from flask import request
from ..year.model import *
from functools import wraps

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "logged" not in session:
            flash ("Musíte se přihlásit", "info")
            return redirect (url_for("team.view_login"))
        return func(*args, **kwargs)
    return decorated_function

def current_year_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        year=get_year(request.blueprint)
        if not year['is_current_year']:
            flash ("Stránka dostupná pouze v aktuálním ročníku", "error")
            return redirect (url_for("main.view_index"))
        return func(*args, **kwargs)
    return decorated_function

