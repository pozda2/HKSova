'''
Year - model
'''
import re
from flask import current_app
from sqlalchemy import func
from ..database import db

class Year(db.Model):
    __tablename__ = 'year'
    idYear = db.Column(db.Integer, primary_key=True)


def get_current_year():
    '''
    Get last year defined in DB

    Returns
    -------
    str: year in YYYY form

    '''
    max_year = db.session.query(func.max(Year.idYear)).scalar()
    return str(max_year) if max_year else None


def get_years():
    '''
    Get all defined years

    Returns
    -------
    dict: all available years

    '''
    years = Year.query.order_by(Year.idYear.desc()).all()
    return [{'idyear': y.idYear} for y in years]


def get_year(blueprint_year):
    '''
    Try to parse year from bleprint.

    Parameters
    ----------
    blueprint_year: str: template to parse

    Returns
    -------
    dict: year with flags
    '''
    pattern = re.compile(r'.+?(\d+)$')
    year = {}
    if pattern.match(blueprint_year):
        year['year'] = str(pattern.search(blueprint_year).groups()[0])
        if year['year'] == get_current_year():
            year['is_current_year'] = True
        else:
            year['is_current_year'] = False
    else:
        year['year'] = get_current_year()
        year['is_current_year'] = True

    return year
