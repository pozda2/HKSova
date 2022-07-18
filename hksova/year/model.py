'''
Year - model
'''
import re
from flask import current_app


def get_current_year():
    '''
    Get last year defined in DB

    Returns
    -------
    str: year in YYYY form

    '''
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''SELECT max(idYear) as idYear FROM year''')
    data = cursor.fetchall()
    return str(data[0]['idYear'])


def get_years():
    '''
    Get all defined years

    Returns
    -------
    dict: all available years

    '''
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''SELECT idyear FROM year order by idyear desc''')
    data = cursor.fetchall()
    return data


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
