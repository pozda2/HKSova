import sys
from flask import current_app
from datetime import datetime
from dateutil import parser
from datetime import timedelta  

def get_settings_year(year, param):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''SELECT value  FROM setting where idYear=%s and param=%s''', [year, param])
    data = cursor.fetchall()
    return data[0]['value']

def get_settings_global(param):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''SELECT value FROM setting where idYear is null and param=%s''', [param])
    data = cursor.fetchall()
    return data[0]['value']

def is_registration_open(year):
    reg_from = parser.parse(get_settings_year(year, 'reg-from'))
    reg_to = parser.parse(get_settings_year(year, 'reg-to'))
    today=datetime.now() 

    if (today > reg_from and today < reg_to + timedelta(days=1)):
        return True
    else:
        return False

def get_registration_from(year):    
    return parser.parse(get_settings_year(year, "reg-from")).strftime("%-d. %-m. %Y")

def get_registration_to(year):
    return parser.parse(get_settings_year(year, "reg-to")).strftime("%-d. %-m. %Y")

def get_min_players(year):
    return int(get_settings_year(year, "min-players"))

def get_max_players(year):
    return int(get_settings_year(year, "max-players"))

def get_max_teams(year):
    return int(get_settings_year(year, "max-teams"))
