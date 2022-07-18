from functools import wraps
from flask import redirect, url_for, flash, request

from ..year.model import get_year


# TODO: duplicity with team/utils.py
def current_year_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        year = get_year(request.blueprint)
        if not year['is_current_year']:
            flash("Stránka dostupná pouze v aktuálním ročníku", "error")
            return redirect(url_for("main.view_index"))
        return func(*args, **kwargs)
    return decorated_function
