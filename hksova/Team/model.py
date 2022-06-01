import sys
import random
import secrets
from flask import current_app
from passlib.hash import sha256_crypt
from datetime import datetime

from hksova.settings.model import get_max_teams

def is_unique_name(year, name):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''SELECT name FROM team where idYear=%s and name=%s''', [year, name])
    data = cursor.fetchall()
    if (len(data)==0):
        return True
    else:
        return False

def is_unique_loginname(year, name):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''SELECT name FROM team where idYear=%s and login=%s''', [year, name])
    data = cursor.fetchall()
    if (len(data)==0):
        return True
    else:
        return False

def is_unique_email(year, email):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''SELECT email FROM team where idYear=%s and email=%s''', [year, email])
    data = cursor.fetchall()
    if (len(data)==0):
        return True
    else:
        return False

def is_minimum_players(players, min_players):
    players_count=0

    for player in players:
        if player['name'] != '':
            players_count+=1

    if (players_count >= min_players):
        return True
    else:
        return False

def get_mascots():
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''SELECT mascot FROM mascot''')
    data = cursor.fetchall()
    return data

def get_used_mascot(year):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''SELECT mascot FROM team where idYear=%s''', [year])
    data = cursor.fetchall()
    return data

def get_random_mascot():
    data =  get_mascots()
    return (data[random.randrange(0, len(data))]['mascot'])

def get_unique_mascot(year):
    used_mascots=get_used_mascot(year)
    unique=False
    while not unique:
        mascot = get_random_mascot()
        if mascot not in used_mascots:
            unique=True
    return mascot

def get_registred_num_teams(year):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''SELECT count(idTeam) as count FROM team where idYear=%s and isBackup=0''', [year])
    data=cursor.fetchall()
    return data[0]['count']

def check_password_org (login, password):
    # password for org stored in table settings
    if (login == 'org'):
        try:
            cursor = current_app.mysql.connection.cursor()
            cursor.execute('''select param, value from setting where idyear is null''')
            data = cursor.fetchall()
            hash_in_setting=None
            salt_in_setting=None

            for param in data:
                if param['param']=='org-pass':
                    hash_in_setting=param['value']
                elif param['param']=='org-salt':
                    salt_in_setting=param['value']

            if hash_in_setting and salt_in_setting:
                return sha256_crypt.verify(current_app.config['SECRET_PEPPER'] + password + salt_in_setting, hash_in_setting)
            else:
                return False
        except Exception as e:
            return False
    else:
        return False

def check_password_team (year, login, password):
    # password for team stored in table team
    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute('''select pass, salt from team where idyear = %s and login = %s''', [year, login])
        data = cursor.fetchall()
        
        hash_in_table=None
        salt_in_table=None
        for team in data:
            hash_in_table=team['pass']
            salt_in_table=team['salt']

        if hash_in_table and salt_in_table:
            return sha256_crypt.verify(current_app.config['SECRET_PEPPER'] + password + salt_in_table, hash_in_table)
        else:
            return False
    except Exception as e:
        return False

def create_team (form, year):
    salt=secrets.token_hex(20)
    password = sha256_crypt.hash(current_app.config['SECRET_PEPPER'] + form.password.data + salt)
    mascot=get_unique_mascot(year)
    today=datetime.now()
    
    if (get_registred_num_teams(year) >= get_max_teams(year)):
        isBackup=1
    else:
        isBackup=0

    # vlozeni tymu do tabulky team
    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute('''INSERT INTO team (
            idYear, name, mascot, login, pass, salt, email, mobil, webUrl, isBackup, registeredAt)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', 
            [year, form.name.data, mascot, form.loginname.data, password, salt, form.email.data, form.mobil.data, form.weburl.data, isBackup, today])		
        idteam=cursor.lastrowid
        
    except Exception as e:
        return False, "Problem inserting into db: " + str(e)

    # vlozeni hracu tymu
    for i, player in enumerate(form.players.data):
        if (player['name'].strip()):
            if (player['city'].strip()):
                city=player['city'].strip()
            else:
                city=None
            if (player['age'].isnumeric()):
                age=int(player['age'])
            else:
                age=None
            try:
                cursor.execute('''INSERT INTO player (idTeam, `order`, name, publicName, city, age) VALUES (%s, %s, %s, %s, %s, %s)''', 
                                [idteam, i, player['name'].strip(), player['publicname'].strip(), city, age])
            except Exception as e:
                return False, "Problem inserting into db: " + str(e)

    current_app.mysql.connection.commit()
    return True, ""

def get_team_players(idteam):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''SELECT  idteam, name, publicname, city, age FROM player where idteam=%s order by `order`''', [idteam])
    return cursor.fetchall()

def players_to_string(players):
    hraci=''
    for player in players:
        if player['publicname']:
            name=player['publicname']
        else:
            name='Anonymous'
        if hraci:
            hraci+=", "+name
        else:
            hraci=name
    return hraci

def get_team_status_paid(team):
    if (team['isPaid']==1):
        return 'Zaplaceno'
    else:
        return 'Nezaplaceno'

def get_team_status(team):
    if (team['isPaid']==1):
        return 'Hracící'
    else:
        if (team['isBackup']==1):
            return 'Náhradníci'
        else:
            return 'Registrováni'
    
def get_teams(year):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''SELECT  idteam, name, mascot, email, mobil, weburl, reporturl, isPaid, isBackup, isDeleted, registeredAt FROM team where idYear=%s and isdeleted=0 order by isBackup, registeredAt''', [year])
    data=cursor.fetchall()

    # podrobnosti o tymu
    if (data):
        i=1
        for team in data:
            players=get_team_players(team['idteam'])
            team['players']=players_to_string(players)
            team['order']=i
            team['zaplaceno']=get_team_status_paid(team)
            team['stav']=get_team_status(team)
            i+=1
    return data





