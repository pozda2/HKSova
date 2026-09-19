import random
import secrets
from datetime import datetime
from flask import current_app, session
from passlib.hash import sha256_crypt
from sqlalchemy import func
from ..database import db, db_error_message

from ..settings.model import get_max_teams

class Mascot(db.Model):
    __tablename__ = 'mascot'
    mascot = db.Column(db.String(50), primary_key=True)

class Team(db.Model):
    __tablename__ = 'team'
    idTeam = db.Column(db.Integer, primary_key=True)
    idYear = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    mascot = db.Column(db.String(100), nullable=True)
    login = db.Column(db.String(100), nullable=False)
    pass_hash = db.Column('pass', db.String(100), nullable=False)
    salt = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(255), nullable=False)
    mobil = db.Column(db.String(30), nullable=False)
    webUrl = db.Column(db.String(255), nullable=True)
    reportUrl = db.Column(db.String(255), nullable=True)
    isPaid = db.Column(db.Boolean, nullable=False, default=False)
    isBackup = db.Column(db.Boolean, nullable=False, default=False)
    isDeleted = db.Column(db.Boolean, nullable=False, default=False)
    registeredAt = db.Column(db.DateTime, nullable=False)
    passResetCode = db.Column(db.String(100), nullable=True)
    passResetAt = db.Column(db.DateTime, nullable=True)
    
class Player(db.Model):
    __tablename__ = 'player'
    idPlayer = db.Column(db.Integer, primary_key=True)
    idTeam = db.Column(db.Integer, nullable=False)
    order = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    publicName = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gameIndex = db.Column(db.Integer, nullable=True)


def is_unique_name(year, name, login):
    query = Team.query.filter_by(idYear=year['year'], name=name)
    if login is not None:
        query = query.filter(Team.login != login)
    return query.count() == 0


def is_unique_loginname(year, name):
    return Team.query.filter_by(idYear=year['year'], login=name).count() == 0


def is_unique_email(year, email, login):
    query = Team.query.filter_by(idYear=year['year'], email=email)
    if login is not None:
        query = query.filter(Team.login != login)
    return query.count() == 0


def is_minimum_players(players, min_players):
    players_count = sum([1 for p in players if p['name'] != ''])
    return bool(players_count >= min_players)


def get_mascots():
    mascots = Mascot.query.all()
    return [{'mascot': m.mascot} for m in mascots]


def get_used_mascot(year):
    teams = Team.query.filter_by(idYear=year['year']).all()
    return [{'mascot': t.mascot} for t in teams if t.mascot]


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
    return Team.query.filter_by(idYear=year['year'], isBackup=False).count()


def check_password_team(year, login, password):
    # password for team stored in table team
    try:
        team = Team.query.filter_by(idYear=year['year'], login=login, isDeleted=False).first()
        if team and team.pass_hash and team.salt:
            return sha256_crypt.verify(current_app.config['SECRET_PEPPER'] + password + team.salt, team.pass_hash)
        return False
    except Exception:
        return False


def insert_team(form, year):
    salt = secrets.token_hex(20)
    password = sha256_crypt.hash(current_app.config['SECRET_PEPPER'] + form.password.data + salt)
    mascot = get_unique_mascot(year)
    today = datetime.now()

    if get_registred_number_teams(year) >= get_max_teams(year):
        is_backup = True
    else:
        is_backup = False

    try:
        new_team = Team(
            idYear=year['year'], name=form.name.data, mascot=mascot, login=form.loginname.data,
            pass_hash=password, salt=salt, email=form.email.data, mobil=form.mobil.data,
            webUrl=form.weburl.data, isBackup=is_backup, registeredAt=today
        )
        db.session.add(new_team)
        db.session.flush() # flush to get idTeam
        idteam = new_team.idTeam

        # insert players
        for i, player in enumerate(form.players.data):
            if player['name'].strip():
                city = player['city'].strip() if player['city'].strip() else None
                age = int(player['age']) if player['age'].isnumeric() else None
                
                new_player = Player(
                    idTeam=idteam, order=i, name=player['name'].strip(),
                    publicName=player['publicname'].strip(), city=city, age=age
                )
                db.session.add(new_player)
                
        db.session.commit()
        return True, ""
    except Exception as e:
        db.session.rollback()
        return False, db_error_message(e, "zaregistrovat tým")


def update_team(form, year, login):
    team_dict = get_team(year, login)
    if not team_dict:
        return False, "Tým nenalezen"
        
    try:
        team_obj = Team.query.get(team_dict['idteam'])
        team_obj.name = form.name.data
        team_obj.email = form.email.data
        team_obj.mobil = form.mobil.data
        team_obj.webUrl = form.weburl.data
        team_obj.reportUrl = form.reporturl.data

        for i, player_data in enumerate(form.players.data):
            player_in_database = False
            for saved_player in team_dict['players']:
                if saved_player['order'] == i:
                    player_in_database = True

            age = player_data['age'].strip()
            age = int(age) if age else None

            if player_data['name'].strip():
                if player_in_database:
                    player_obj = Player.query.filter_by(idTeam=team_dict['idteam'], order=i).first()
                    if player_obj:
                        player_obj.name = player_data['name']
                        player_obj.publicName = player_data['publicname']
                        player_obj.city = player_data['city']
                        player_obj.age = age
                else:
                    new_player = Player(
                        idTeam=team_dict['idteam'], name=player_data['name'],
                        publicName=player_data['publicname'], city=player_data['city'],
                        age=age, order=i
                    )
                    db.session.add(new_player)
            else:
                if player_in_database:
                    Player.query.filter_by(idTeam=team_dict['idteam'], order=i).delete()
                    
        db.session.commit()
        return True, ""
    except Exception as e:
        db.session.rollback()
        return False, db_error_message(e, "uložit úpravy týmu")


def get_team_players(idteam):
    players = Player.query.filter_by(idTeam=idteam).order_by(Player.order).all()
    return [{
        'idteam': p.idTeam,
        'name': p.name,
        'publicname': p.publicName,
        'city': p.city,
        'age': p.age,
        'order': p.order
    } for p in players]


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
    teams = Team.query.filter_by(idYear=year['year'], isDeleted=False).order_by(Team.isBackup, Team.registeredAt).all()
    data = []
    if teams:
        for i, team in enumerate(teams, 1):
            team_dict = {
                'idteam': team.idTeam, 'name': team.name, 'login': team.login, 'mascot': team.mascot,
                'email': team.email, 'mobil': team.mobil, 'weburl': team.webUrl or '',
                'reporturl': team.reportUrl, 'isPaid': 1 if team.isPaid else 0,
                'isBackup': 1 if team.isBackup else 0, 'isDeleted': 1 if team.isDeleted else 0,
                'registeredAt': team.registeredAt
            }
            players = get_team_players(team.idTeam)
            team_dict['player'] = players
            team_dict['players_public'] = players_to_public_string(players)
            team_dict['players_private'] = players_to_string(players)
            team_dict['order'] = i
            team_dict['zaplaceno'] = get_team_status_paid(team_dict)
            team_dict['stav'] = get_team_status(team_dict)
            data.append(team_dict)
    return data


def get_team(year, login):
    team = Team.query.filter_by(idYear=year['year'], login=login, isDeleted=False).order_by(Team.isBackup, Team.registeredAt).first()
    if team:
        team_dict = {
            'idteam': team.idTeam, 'name': team.name, 'login': team.login, 'mascot': team.mascot,
            'email': team.email, 'mobil': team.mobil, 'weburl': team.webUrl,
            'reporturl': team.reportUrl, 'isPaid': 1 if team.isPaid else 0,
            'isBackup': 1 if team.isBackup else 0, 'isDeleted': 1 if team.isDeleted else 0,
            'registeredAt': team.registeredAt
        }
        players = get_team_players(team.idTeam)
        team_dict['players'] = players
        team_dict['players_private'] = players_to_string(players)
        team_dict['players_public'] = players_to_public_string(players)
        team_dict['zaplaceno'] = get_team_status_paid(team_dict)
        team_dict['stav'] = get_team_status(team_dict)
        return team_dict
    return None


def get_team_by_email(year, email):
    team = Team.query.filter_by(idYear=year['year'], email=email, isDeleted=False).order_by(Team.isBackup, Team.registeredAt).first()
    if team:
        team_dict = {
            'idteam': team.idTeam, 'name': team.name, 'login': team.login, 'mascot': team.mascot,
            'email': team.email, 'mobil': team.mobil, 'weburl': team.webUrl,
            'reporturl': team.reportUrl, 'isPaid': 1 if team.isPaid else 0,
            'isBackup': 1 if team.isBackup else 0, 'isDeleted': 1 if team.isDeleted else 0,
            'registeredAt': team.registeredAt
        }
        players = get_team_players(team.idTeam)
        team_dict['players'] = players
        team_dict['players_private'] = players_to_string(players)
        team_dict['players_public'] = players_to_public_string(players)
        team_dict['zaplaceno'] = get_team_status_paid(team_dict)
        team_dict['stav'] = get_team_status(team_dict)
        return team_dict
    return None


def get_team_by_reset_code(code):
    team = Team.query.filter(Team.passResetCode == code, (db.func.current_timestamp() - Team.passResetAt) < 900).first()
    if team:
        return {
            'idteam': team.idTeam, 'name': team.name, 'login': team.login, 'mascot': team.mascot,
            'email': team.email, 'mobil': team.mobil, 'weburl': team.webUrl,
            'reporturl': team.reportUrl, 'isPaid': 1 if team.isPaid else 0,
            'isBackup': 1 if team.isBackup else 0, 'isDeleted': 1 if team.isDeleted else 0,
            'registeredAt': team.registeredAt
        }
    return None


def generate_reset_code(idteam):
    code = secrets.token_hex(50)
    try:
        team = Team.query.get(idteam)
        team.passResetCode = code
        team.passResetAt = db.func.current_timestamp()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return None, False, db_error_message(e, "vygenerovat kód pro reset hesla")
    return code, True, ""


def reset_team_pass(idteam, password_new):
    salt = secrets.token_hex(20)
    hash_new = sha256_crypt.hash(current_app.config['SECRET_PEPPER'] + password_new + salt)
    try:
        team = Team.query.get(idteam)
        team.pass_hash = hash_new
        team.salt = salt
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, db_error_message(e, "nastavit nové heslo")
    return True, ""


def get_city_statistics(year):
    stats = db.session.query(Player.city, func.count(Player.idPlayer).label('count')).\
        join(Team, Player.idTeam == Team.idTeam).\
        filter(Team.idYear == year['year'], Player.city != None, Team.isDeleted == False).\
        group_by(Player.city).\
        order_by(db.text('count DESC'), Player.city).all()
        
    return [{'city': s.city, 'count': s.count} for s in stats]


def get_teams_statistics(year):
    teams = Team.query.filter_by(idYear=year['year'], isDeleted=False).all()
    
    total_team = len(teams)
    paid_team = sum(1 for t in teams if t.isPaid)
    not_paid_team = total_team - paid_team
    backup_team = sum(1 for t in teams if t.isBackup)
    
    players_data = db.session.query(Team.isPaid, Team.isBackup).\
        join(Player, Player.idTeam == Team.idTeam).\
        filter(Team.idYear == year['year'], Team.isDeleted == False).all()
        
    total_players = len(players_data)
    paid_players = sum(1 for p in players_data if p.isPaid)
    not_paid_players = total_players - paid_players
    backup_players = sum(1 for p in players_data if p.isBackup)

    return {
        'total_team': total_team, 'paid_team': paid_team, 'notpaid_team': not_paid_team, 'backup_team': backup_team,
        'total_players': total_players, 'paid_players': paid_players, 'notpaid_players': not_paid_players, 'backup_players': backup_players
    }


# TODO: shloud be rewritten in more pythonic way (using Pandas.dataframe???)
def get_players_statistics(year):
    players = db.session.query(Player.age, Team.isPaid, Team.isBackup).\
        join(Team, Team.idTeam == Player.idTeam).\
        filter(Team.idYear == year['year'], Player.age != None, Team.isDeleted == False).all()

    stat = {
        'total_count': 0, 'total_sum': 0, 'total_min': 150, 'total_max': 0,
        'paid_count': 0, 'paid_sum': 0, 'paid_min': 150, 'paid_max': 0,
        'notpaid_count': 0, 'notpaid_sum': 0, 'notpaid_min': 150, 'notpaid_max': 0,
        'backup_count': 0, 'backup_sum': 0, 'backup_min': 150, 'backup_max': 0
    }

    if players:
        for player in players:
            stat['total_count'] += 1
            stat['total_sum'] += player.age
            stat['total_min'] = min(stat['total_min'], player.age)
            stat['total_max'] = max(stat['total_max'], player.age)

            if player.isPaid:
                stat['paid_count'] += 1
                stat['paid_sum'] += player.age
                stat['paid_min'] = min(stat['paid_min'], player.age)
                stat['paid_max'] = max(stat['paid_max'], player.age)
            else:
                stat['notpaid_count'] += 1
                stat['notpaid_sum'] += player.age
                stat['notpaid_min'] = min(stat['notpaid_min'], player.age)
                stat['notpaid_max'] = max(stat['notpaid_max'], player.age)

            if player.isBackup:
                stat['backup_count'] += 1
                stat['backup_sum'] += player.age
                stat['backup_min'] = min(stat['backup_min'], player.age)
                stat['backup_max'] = max(stat['backup_max'], player.age)

    for prefix in ['total', 'paid', 'notpaid', 'backup']:
        count = stat[f'{prefix}_count']
        if count > 0:
            stat[f'{prefix}_avg'] = f"{stat[f'{prefix}_sum'] / count:.2f}"
            if stat[f'{prefix}_min'] == 150:
                stat[f'{prefix}_min'] = "-"
            if stat[f'{prefix}_max'] == 0:
                stat[f'{prefix}_max'] = "-"
        else:
            stat[f'{prefix}_avg'] = "-"
            stat[f'{prefix}_min'] = "-"
            stat[f'{prefix}_max'] = "-"

    return stat


def get_reports(year):
    teams = Team.query.filter(Team.idYear == year['year'], Team.isDeleted == False, Team.reportUrl != None, Team.reportUrl != "").all()
    return [{'name': t.name, 'reporturl': t.reportUrl} for t in teams]


def change_team_pass(year, login, password_old, password_new):
    if check_password_team(year, login, password_old):
        salt = secrets.token_hex(20)
        hash_new = sha256_crypt.hash(current_app.config['SECRET_PEPPER'] + password_new + salt)
        try:
            team = Team.query.filter_by(idYear=year['year'], login=login).first()
            if team:
                team.pass_hash = hash_new
                team.salt = salt
                db.session.commit()
                return True, ""
        except Exception as e:
            db.session.rollback()
            return False, db_error_message(e, "změnit heslo")

    return False, "Nesprávné staré heslo"


def cancel_registration(year, login):
    try:
        team = Team.query.filter_by(idYear=year['year'], login=login).first()
        if team:
            team.isDeleted = True
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, db_error_message(e, "zrušit registraci")

    status, message = recalculate_teams(year)
    return status, message


def recalculate_teams(year):
    max_teams = get_max_teams(year)
    teams = Team.query.filter_by(idYear=year['year'], isDeleted=False).order_by(Team.isBackup, Team.registeredAt).all()
    count = 0
    
    try:
        for team in teams:
            team.isBackup = count >= max_teams
            count += 1
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, db_error_message(e, "přepočítat pořadí týmů")

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
