import sys
import random
import secrets
from flask import current_app
from passlib.hash import sha256_crypt
from datetime import datetime
from flask import session

from hksova.settings.model import get_max_teams

def is_unique_name(year, name, login):
    cursor = current_app.mysql.connection.cursor()
    if login is not None:
        cursor.execute('''SELECT name FROM team where idYear=%s and name=%s and login<>%s''', [year['year'], name, login])
    else:
        cursor.execute('''SELECT name FROM team where idYear=%s and name=%s''', [year['year'], name])
    data = cursor.fetchall()
    if (len(data)==0):
        return True
    else:
        return False

def is_unique_loginname(year, name):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''SELECT name FROM team where idYear=%s and login=%s''', [year['year'], name])
    data = cursor.fetchall()
    if (len(data)==0):
        return True
    else:
        return False

def is_unique_email(year, email, login):
    cursor = current_app.mysql.connection.cursor()
    if login is not None:
        cursor.execute('''SELECT email FROM team where idYear=%s and email=%s and login <> %s''', [year['year'], email, login])
    else:
        cursor.execute('''SELECT email FROM team where idYear=%s and email=%s''', [year['year'], email])
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
    cursor.execute('''SELECT mascot FROM team where idYear=%s''', [year['year']])
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

def get_registred_number_teams(year):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''SELECT count(idTeam) as count FROM team where idYear=%s and isBackup=0''', [year['year']])
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
        cursor.execute('''select pass, salt from team where idyear = %s and login = %s and isDeleted=0''', [year['year'], login])
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

def insert_team (form, year):
    salt=secrets.token_hex(20)
    password = sha256_crypt.hash(current_app.config['SECRET_PEPPER'] + form.password.data + salt)
    mascot=get_unique_mascot(year)
    today=datetime.now()
    
    if (get_registred_number_teams(year) >= get_max_teams(year)):
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
            [year['year'], form.name.data, mascot, form.loginname.data, password, salt, form.email.data, form.mobil.data, form.weburl.data, isBackup, today])		
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

def update_team (form, year, login):
    team=get_team(year, login)
    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute('''UPDATE team set name=%s, email=%s, mobil=%s, weburl=%s, reporturl=%s where idyear=%s and login=%s''',
            [form.name.data, form.email.data, form.mobil.data, form.weburl.data, form.reporturl.data, year['year'], login])
    except Exception as e:
        return False, "Problem updatint db: " + str(e)

    # update players
    for i, player in enumerate(form.players.data):

        # check player in form is in database
        player_in_database=False
        for saved_player in team['players']:
            if saved_player['order']==i:
                player_in_database=True
        
        if player['age'].strip() == "":
            player['age']=None

        if (player['name'].strip()):
            if player_in_database:
                try:
                    cursor.execute('''UPDATE player set name=%s, publicname=%s, city=%s, age=%s where idteam=%s and `order`=%s''',
                    [player['name'], player['publicname'], player['city'], player['age'], team['idteam'], i])
                except Exception as e:
                    return False, "Problem updatint db: " + str(e)
            else:
                try:
                    cursor.execute('''INSERT into player (idteam, name, publicname, city, age, `order`) VALUES (%s, %s, %s, %s, %s, %s)''',
                    [team['idteam'], player['name'], player['publicname'], player['city'], player['age'], i])
                except Exception as e:
                    return False, "Problem updatint db: " + str(e)
        else:
            if player_in_database:
                try:
                    cursor.execute('''DELETE from player where idteam=%s and `order`=%s''',
                    [team['idteam'], i])
                except Exception as e:
                    return False, "Problem updatint db: " + str(e)
    current_app.mysql.connection.commit()
    return True, ""

def get_team_players(idteam):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''SELECT  idteam, name, publicname, city, age, `order` FROM player where idteam=%s order by `order`''', [idteam])
    return cursor.fetchall()

def players_to_string(players):
    hraci=''
    for player in players:
        if player['name']:
            name=player['name']
        else:
            name='Anonymous'
        if hraci:
            hraci+=", "+name
        else:
            hraci=name
    return hraci

def players_to_public_string(players):
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
    if (team['isBackup']==1):
        return 'Náhradníci'
    else:
        return 'Hrající'
    
def get_teams_not_deleted(year):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''SELECT  idteam, name, login, mascot, email, mobil, weburl, reporturl, isPaid, isBackup, isDeleted, registeredAt FROM team where idYear=%s and isdeleted=0 order by isBackup, registeredAt''', [year['year']])
    data=cursor.fetchall()

    # podrobnosti o tymu
    if (data):
        i=1
        for team in data:
            players=get_team_players(team['idteam'])
            team['player']=players
            team['players_public']=players_to_public_string(players)
            team['players_private']=players_to_string(players)
            team['order']=i
            team['zaplaceno']=get_team_status_paid(team)
            team['stav']=get_team_status(team)
            i+=1
    return data

def get_team(year, login):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''SELECT  idteam, name, login, mascot, email, mobil, weburl, reporturl, isPaid, isBackup, isDeleted, registeredAt FROM team where idYear=%s and isdeleted=0 and login=%s order by isBackup, registeredAt''', [year['year'], login])
    data=cursor.fetchall()

    # podrobnosti o tymu
    if (data):
        team=data[0]
        players=get_team_players(team['idteam'])
        team['players']=players
        team['players_private']=players_to_string(players)
        team['players_public']=players_to_public_string(players)
        team['zaplaceno']=get_team_status_paid(team)
        team['stav']=get_team_status(team)
        return team
    else:
        return None

def change_team_pass (year, login, password_old, password_new):
    if (check_password_team (year, login, password_old)):
        salt=secrets.token_hex(20)
        hash_new = sha256_crypt.hash(current_app.config['SECRET_PEPPER'] + password_new + salt)
        try:
            cursor = current_app.mysql.connection.cursor()
            cursor.execute('''UPDATE team set pass=%s, salt=%s where idyear=%s and login=%s ''', [hash_new, salt, year['year'], login])
            current_app.mysql.connection.commit()
        except Exception as e:
            return False, "Problem updating db: " + str(e)
        return True, ""
    else:
        return False, "Nesprávné staré heslo"

def cancel_registration (year, login):
    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute('''UPDATE team set isDeleted=%s where idyear=%s and login=%s ''', [1, year['year'], login])
    except Exception as e:
        return False, "Problem updating db: " + str(e)

    status, message = recalculate_teams(year)
    if status:
        current_app.mysql.connection.commit()
        return True, ""
    else:
        return False, message

def recalculate_teams(year):
    max_teams = get_max_teams(year)
    teams = get_teams_not_deleted(year)
    count=0
    cursor = current_app.mysql.connection.cursor()
    for team in teams:
        if count <= max_teams:
            isBackup=0
        else:
            isBackup=1
        count+=1
        try:
            cursor.execute('''UPDATE team set isBackup=%s where idyear=%s and login=%s ''', [isBackup, year['year'], team['login']])
        except Exception as e:
            return False, "Problem calculation db: " + str(e)
        
    return True, ""

def set_team_session(year, team_name, team_login, org):
    session["logged"] = True
    session["login"] = team_login
    session["team"] = team_name
    if (org):
        session["org"] = True
        session["ispaid"] = True
        session["isbackup"]=False
    else:
        session["org"] = False
        team=get_team(year, team_login)
        if team['isPaid']==0:
            session["ispaid"] = False
        else:
            session["ispaid"] = True

        if team['isBackup']==0:
            session["isbackup"] = False
        else:
            session["isbackup"] = True

def unset_team_session():
    session.pop("logged")
    if session.get("org"): session.pop("org")
    if session.get("team"): session.pop("team")
    if session.get("login"): session.pop("login")
    if session.get("ispaid"): session.pop("ispaid")
    if session.get("isbackup"): session.pop("isbackup")









