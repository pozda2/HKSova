import random
import secrets
from datetime import datetime
from flask import current_app, session
from passlib.hash import sha256_crypt

from ..settings.model import get_max_teams


def is_unique_name(year, name, login):
    cursor = current_app.mysql.connection.cursor()
    if login is not None:
        cursor.execute('''SELECT name FROM team where idYear=%s and name=%s and login<>%s''', [year['year'], name, login])
    else:
        cursor.execute('''SELECT name FROM team where idYear=%s and name=%s''', [year['year'], name])
    data = cursor.fetchall()
    return bool(len(data) == 0)


def is_unique_loginname(year, name):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''SELECT name FROM team where idYear=%s and login=%s''', [year['year'], name])
    data = cursor.fetchall()
    return bool(len(data) == 0)


def is_unique_email(year, email, login):
    cursor = current_app.mysql.connection.cursor()
    if login is not None:
        cursor.execute('''SELECT email FROM team where idYear=%s and email=%s and login <> %s''', [year['year'], email, login])
    else:
        cursor.execute('''SELECT email FROM team where idYear=%s and email=%s''', [year['year'], email])
    data = cursor.fetchall()
    return bool(len(data) == 0)


def is_minimum_players(players, min_players):
    players_count = sum([1 for p in players if p['name'] != ''])
    return bool(players_count >= min_players)


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
    data = get_mascots()
    return data[random.randrange(0, len(data))]['mascot']


def get_unique_mascot(year):
    used_mascots = [x['mascot'] for x in get_used_mascot(year)]
    free_mascots = [x['mascot'] for x in get_mascots() if x['mascot'] not in used_mascots]
    return free_mascots[random.randrange(0, len(free_mascots))]
    # unique = False
    # while not unique:
    #     mascot = get_random_mascot()
    #     if mascot not in used_mascots:
    #         unique = True
    # return mascot


def get_registred_number_teams(year):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''SELECT count(idTeam) as count FROM team where idYear=%s and isBackup=0''', [year['year']])
    data = cursor.fetchall()
    return data[0]['count']


def check_password_org(login, password):
    # password for org stored in table settings
    if login == 'org':
        try:
            cursor = current_app.mysql.connection.cursor()
            cursor.execute('''select param, value from setting where idyear is null''')
            data = cursor.fetchall()
            hash_in_setting = None
            salt_in_setting = None

            for param in data:
                if param['param'] == 'org-pass':
                    hash_in_setting = param['value']
                elif param['param'] == 'org-salt':
                    salt_in_setting = param['value']

            if hash_in_setting and salt_in_setting:
                return sha256_crypt.verify(current_app.config['SECRET_PEPPER'] + password + salt_in_setting, hash_in_setting)
            return False
        except Exception:
            return False
    else:
        return False


def check_password_team(year, login, password):
    # password for team stored in table team
    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute('''select pass, salt from team where idyear = %s and login = %s and isDeleted=0''', [year['year'], login])
        data = cursor.fetchall()

        hash_in_table = None
        salt_in_table = None
        for team in data:
            hash_in_table = team['pass']
            salt_in_table = team['salt']

        if hash_in_table and salt_in_table:
            return sha256_crypt.verify(current_app.config['SECRET_PEPPER'] + password + salt_in_table, hash_in_table)
        return False
    except Exception:
        return False


def insert_team(form, year):
    salt = secrets.token_hex(20)
    password = sha256_crypt.hash(current_app.config['SECRET_PEPPER'] + form.password.data + salt)
    mascot = get_unique_mascot(year)
    today = datetime.now()

    if get_registred_number_teams(year) >= get_max_teams(year):
        is_backup = 1
    else:
        is_backup = 0

    # vlozeni tymu do tabulky team
    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute('''INSERT INTO team(
            idYear, name, mascot, login, pass, salt, email, mobil, webUrl, isBackup, registeredAt)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', [year['year'], form.name.data, mascot, form.loginname.data, password, salt, form.email.data, form.mobil.data, form.weburl.data, is_backup, today])
        idteam = cursor.lastrowid

    except Exception as e:
        return False, "Problem inserting into db: " + str(e)

    # vlozeni hracu tymu
    for i, player in enumerate(form.players.data):
        if player['name'].strip():
            if player['city'].strip():
                city = player['city'].strip()
            else:
                city = None
            if player['age'].isnumeric():
                age = int(player['age'])
            else:
                age = None
            try:
                cursor.execute('''INSERT INTO player (idTeam, `order`, name, publicName, city, age) VALUES (%s, %s, %s, %s, %s, %s)''',
                               [idteam, i, player['name'].strip(), player['publicname'].strip(), city, age])
            except Exception as e:
                return False, "Problem inserting into db: " + str(e)

    current_app.mysql.connection.commit()
    return True, ""


def update_team(form, year, login):
    team = get_team(year, login)
    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute('''UPDATE team set name=%s, email=%s, mobil=%s, weburl=%s, reporturl=%s where idyear=%s and login=%s''',
                       [form.name.data, form.email.data, form.mobil.data, form.weburl.data, form.reporturl.data, year['year'], login])
    except Exception as e:
        return False, "Problem updatint db: " + str(e)

    # update players
    for i, player in enumerate(form.players.data):

        # check player in form is in database
        player_in_database = False
        for saved_player in team['players']:
            if saved_player['order'] == i:
                player_in_database = True

        if player['age'].strip() == "":
            player['age'] = None

        if player['name'].strip():
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
                    cursor.execute('''DELETE from player where idteam=%s and `order`=%s''', [team['idteam'], i])
                except Exception as e:
                    return False, "Problem updatint db: " + str(e)
    current_app.mysql.connection.commit()
    return True, ""


def get_team_players(idteam):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''SELECT  idteam, name, publicname, city, age, `order` FROM player where idteam=%s order by `order`''', [idteam])
    return cursor.fetchall()


def players_to_string(players):
    hraci = []
    for player in players:
        if player['name']:
            hraci.append(player['name'])
        else:
            hraci.append('Anonymous')

    return ', '.join(hraci)


# TODO: repeating code; parametrize the filed name/publicname
def players_to_public_string(players):
    hraci = []
    for player in players:
        if player['publicname']:
            hraci.append(player['publicname'])
        else:
            hraci.append('Anonymous')

    return ', '.join(hraci)


def get_team_status_paid(team):
    if team['isPaid'] == 1:
        return 'Zaplaceno'
    return 'Neplaceno'


def get_team_status(team):
    if team['isBackup'] == 1:
        return 'Náhradníci'
    return 'Hrající'


def get_teams_not_deleted(year):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''SELECT  idteam, name, login, mascot, email, mobil, COALESCE(weburl, '') weburl, reporturl, isPaid, isBackup, isDeleted, registeredAt FROM team where idYear=%s and isdeleted=0 order by isBackup, registeredAt''', [year['year']])
    data = cursor.fetchall()

    # podrobnosti o tymu
    if data:
        i = 1
        for team in data:
            players = get_team_players(team['idteam'])
            team['player'] = players
            team['players_public'] = players_to_public_string(players)
            team['players_private'] = players_to_string(players)
            team['order'] = i
            team['zaplaceno'] = get_team_status_paid(team)
            team['stav'] = get_team_status(team)
            i += 1
    return data


def get_team(year, login):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''SELECT  idteam, name, login, mascot, email, mobil, weburl, reporturl, isPaid, isBackup, isDeleted, registeredAt FROM team where idYear=%s and isdeleted=0 and login=%s order by isBackup, registeredAt''', [year['year'], login])
    data = cursor.fetchall()

    # podrobnosti o tymu
    if data:
        team = data[0]
        players = get_team_players(team['idteam'])
        team['players'] = players
        team['players_private'] = players_to_string(players)
        team['players_public'] = players_to_public_string(players)
        team['zaplaceno'] = get_team_status_paid(team)
        team['stav'] = get_team_status(team)
        return team

    return None


def get_team_by_email(year, email):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''SELECT  idteam, name, login, mascot, email, mobil, weburl, reporturl, isPaid, isBackup, isDeleted, registeredAt FROM team where idYear=%s and isdeleted=0 and email=%s order by isBackup, registeredAt''', [year['year'], email])
    data = cursor.fetchall()

    # podrobnosti o tymu
    if data:
        team = data[0]
        players = get_team_players(team['idteam'])
        team['players'] = players
        team['players_private'] = players_to_string(players)
        team['players_public'] = players_to_public_string(players)
        team['zaplaceno'] = get_team_status_paid(team)
        team['stav'] = get_team_status(team)
        return team

    return None


def get_team_by_reset_code(code):
    # timeout_sec = 900
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''select idteam, name, login, mascot, email, mobil, weburl, reporturl, isPaid, isBackup, isDeleted, registeredAt from team where passresetcode=%s and  CURRENT_TIMESTAMP() - passresetat < 900;''', [code])
    data = cursor.fetchall()
    if data:
        team = data[0]
        return team

    return None


def generate_reset_code(idteam):
    code = secrets.token_hex(50)
    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute('''UPDATE team set passresetcode=%s, passresetat=current_timestamp() where idteam=%s''', [code, idteam])
    except Exception as e:
        return None, False, "Problem updatint db: " + str(e)

    current_app.mysql.connection.commit()
    return code, True, ""


def reset_team_pass(idteam, password_new):
    salt = secrets.token_hex(20)
    hash_new = sha256_crypt.hash(current_app.config['SECRET_PEPPER'] + password_new + salt)
    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute('''UPDATE team set pass=%s, salt=%s where idteam=%s ''', [hash_new, salt, idteam])
        current_app.mysql.connection.commit()
    except Exception as e:
        return False, "Problem updating db: " + str(e)
    return True, ""


def get_city_statistics(year):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''select city, count(*) as count from player p, team t where t.idteam = p.idteam and idyear=%s and city is not null and isdeleted =0 group by city order by 2 desc, 1 asc''', [year['year']])
    data = cursor.fetchall()
    return data


# TODO: shloud be rewritten in more pythonic way
def get_teams_statistics(year):
    total_team = 0
    paid_team = 0
    backup_team = 0
    not_paid_team = 0
    total_players = 0
    paid_players = 0
    backup_players = 0
    not_paid_players = 0

    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''select ispaid, isbackup from team t where idyear=%s and isdeleted=0;''', [year['year']])
    data = cursor.fetchall()

    if data:
        for team in data:
            total_team += 1
            if team['ispaid'] == 1:
                paid_team += 1
            else:
                not_paid_team += 1
            if team['isbackup']:
                backup_team += 1

    cursor.execute('''select ispaid, isbackup from player p, team t where t.idteam = p.idteam and idyear=%s and isdeleted=0;''', [year['year']])
    data = cursor.fetchall()
    if data:
        for team in data:
            total_players += 1
            if team['ispaid'] == 1:
                paid_players += 1
            else:
                not_paid_players += 1
            if team['isbackup']:
                backup_players += 1

    stat = {}
    stat['total_team'] = total_team
    stat['paid_team'] = paid_team
    stat['notpaid_team'] = not_paid_team
    stat['backup_team'] = backup_team
    stat['total_players'] = total_players
    stat['paid_players'] = paid_players
    stat['notpaid_players'] = not_paid_players
    stat['backup_players'] = backup_players

    return stat


# TODO: shloud be rewritten in more pythonic way (using Pandas.dataframe???)
def get_players_statistics(year):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''select age, ispaid, isbackup from player p, team t where t.idteam = p.idteam and idyear=%s and age is not null and isdeleted=0''', [year['year']])
    data = cursor.fetchall()

    stat = {}
    stat['total_count'] = 0
    stat['total_sum'] = 0
    stat['total_avg'] = 0
    stat['total_min'] = 150
    stat['total_max'] = 0
    stat['paid_count'] = 0
    stat['paid_sum'] = 0
    stat['paid_avg'] = 0
    stat['paid_min'] = 150
    stat['paid_max'] = 0
    stat['notpaid_count'] = 0
    stat['notpaid_sum'] = 0
    stat['notpaid_avg'] = 0
    stat['notpaid_min'] = 150
    stat['notpaid_max'] = 0
    stat['backup_count'] = 0
    stat['backup_sum'] = 0
    stat['backup_avg'] = 0
    stat['backup_min'] = 150
    stat['backup_max'] = 0

    if data:
        for player in data:
            stat['total_count'] += 1
            stat['total_sum'] += player['age']
            if player['age'] < stat['total_min']:
                stat['total_min'] = player['age']
            if player['age'] > stat['total_max']:
                stat['total_max'] = player['age']

            if player['ispaid'] == 1:
                stat['paid_count'] += 1
                stat['paid_sum'] += player['age']
                if player['age'] < stat['paid_min']:
                    stat['paid_min'] = player['age']
                if player['age'] > stat['paid_max']:
                    stat['paid_max'] = player['age']

            else:
                stat['notpaid_count'] += 1
                stat['notpaid_sum'] += player['age']
                if player['age'] < stat['notpaid_min']:
                    stat['notpaid_min'] = player['age']
                if player['age'] > stat['notpaid_max']:
                    stat['notpaid_max'] = player['age']

            if player['isbackup']:
                stat['backup_count'] += 1
                stat['backup_sum'] += player['age']
                if player['age'] < stat['backup_min']:
                    stat['backup_min'] = player['age']
                if player['age'] > stat['backup_max']:
                    stat['backup_max'] = player['age']

    if stat['total_count'] > 0:
        stat['total_avg'] = f"{stat['total_sum'] / stat['total_count']:.2f}"
    else:
        stat['total_avg'] = "-"
    if stat['total_min'] == 150:
        stat['total_min'] = "-"
    if stat['total_max'] == 0:
        stat['total_max'] = "-"

    if stat['paid_count'] > 0:
        stat['paid_avg'] = f"{stat['paid_sum'] / stat['paid_count']:.2f}"
    else:
        stat['paid_avg'] = "-"
    if stat['paid_min'] == 150:
        stat['paid_min'] = "-"
    if stat['paid_max'] == 0:
        stat['paid_max'] = "-"

    if stat['notpaid_count'] > 0:
        stat['notpaid_avg'] = f"{stat['notpaid_sum'] / stat['notpaid_count']:.2f}"
    else:
        stat['notpaid_avg'] = "-"
    if stat['notpaid_min'] == 150:
        stat['notpaid_min'] = "-"
    if stat['notpaid_max'] == 0:
        stat['notpaid_max'] = "-"

    if stat['backup_count'] > 0:
        stat['backup_avg'] = f"{stat['backup_sum'] / stat['backup_count']:.2f}"
    else:
        stat['backup_avg'] = "-"
    if stat['backup_min'] == 150:
        stat['backup_min'] = "-"
    if stat['backup_max'] == 0:
        stat['backup_max'] = "-"

    return stat


def get_reports(year):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''SELECT  name, reporturl FROM team where idYear=%s and isdeleted=0 and reporturl is not null and reporturl <> "" ''', [year['year']])
    data = cursor.fetchall()
    return data


def change_team_pass(year, login, password_old, password_new):
    if check_password_team(year, login, password_old):
        salt = secrets.token_hex(20)
        hash_new = sha256_crypt.hash(current_app.config['SECRET_PEPPER'] + password_new + salt)
        try:
            cursor = current_app.mysql.connection.cursor()
            cursor.execute('''UPDATE team set pass=%s, salt=%s where idyear=%s and login=%s ''', [hash_new, salt, year['year'], login])
            current_app.mysql.connection.commit()
        except Exception as e:
            return False, "Problem updating db: " + str(e)
        return True, ""

    return False, "Nesprávné staré heslo"


def cancel_registration(year, login):
    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute('''UPDATE team set isDeleted=%s where idyear=%s and login=%s ''', [1, year['year'], login])
    except Exception as e:
        return False, "Problem updating db: " + str(e)

    status, message = recalculate_teams(year)
    if status:
        current_app.mysql.connection.commit()
        return True, ""

    return False, message


def recalculate_teams(year):
    max_teams = get_max_teams(year)
    teams = get_teams_not_deleted(year)
    count = 0
    cursor = current_app.mysql.connection.cursor()
    for team in teams:
        if count <= max_teams:
            isBackup = 0
        else:
            isBackup = 1
        count += 1
        try:
            cursor.execute('''UPDATE team set isBackup=%s where idyear=%s and login=%s ''', [isBackup, year['year'], team['login']])
        except Exception as e:
            return False, "Problem calculation db: " + str(e)

    return True, ""


def set_team_session(year, team_name, team_login, org):
    session["logged"] = True
    session["login"] = team_login
    session["team"] = team_name
    if org:
        session["org"] = True
        session["ispaid"] = True
        session["isbackup"] = False
    else:
        session["org"] = False
        team = get_team(year, team_login)
        if team['isPaid'] == 0:
            session["ispaid"] = False
        else:
            session["ispaid"] = True

        if team['isBackup'] == 0:
            session["isbackup"] = False
        else:
            session["isbackup"] = True


def unset_team_session():
    session.pop("logged")
    keys = ['org', 'team', 'login', 'ispaid', 'isbackup']
    for k in keys:
        if session.get(k):
            session.pop(k)
