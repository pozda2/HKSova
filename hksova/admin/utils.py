from functools import wraps
from flask import session, redirect, url_for, flash

# Re-exported for existing callers (admin/controller.py); the real
# implementation lives in puzzle/utils.py so the public page blueprint can
# reuse it too, without depending on the admin package.
from ..puzzle.utils import get_puzzle_upload_dir, save_puzzle_file, delete_puzzle_file


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

