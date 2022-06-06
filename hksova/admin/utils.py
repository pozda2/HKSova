from flask import session
from flask import redirect
from flask import url_for
from flask import flash
from functools import wraps

def org_login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "logged" not in session:
            flash ("Musíte se přihlásit", "info")
            return redirect (url_for("team.view_login"))
        if "org" not in session:
            flash ("Musíte se přihlásit", "info")
            return redirect (url_for("team.view_login"))
        return func(*args, **kwargs)
    return decorated_function
