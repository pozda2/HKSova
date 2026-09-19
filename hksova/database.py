from flask import current_app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def db_error_message(e, context):
    '''
    Log the full DB exception server-side and return a safe, generic message
    for the caller to show the user - raw driver/DB errors must never reach
    a flash() message, as they can leak schema details to visitors.
    '''
    current_app.logger.exception("DB error while trying to %s: %s", context, e)
    return f"Nepodařilo se {context}. Zkuste to prosím znovu."
