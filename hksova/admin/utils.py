from functools import wraps
from flask import session, redirect, url_for, flash


def org_login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "logged" not in session:
            flash("Musíte se přihlásit", "info")
            return redirect(url_for("team.view_login"))
        if "org" not in session:
            flash("Musíte se přihlásit", "info")
            return redirect(url_for("team.view_login"))
        return func(*args, **kwargs)
    return decorated_function
