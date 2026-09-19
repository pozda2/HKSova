import secrets
import base64
import csv
import json
import io
import locale
import requests
from datetime import datetime
from flask import current_app
from sqlalchemy import func
from passlib.hash import sha256_crypt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


from .kimatch import load_ki, match_ki
from ..database import db, db_error_message
from ..page.model import Page
from ..menu.model import Menu
from ..forum.model import ForumSection, Forum
from ..settings.model import Setting, get_trakar_token, get_trakar_login
from ..year.model import Year
from ..team.model import Team, Player, Mascot, recalculate_teams
from ..place.model import Place
from ..puzzle.model import Puzzle


def translate_visibility(page):
    if page['isvisible'] == 1:
        return 'Viditelné'
    return 'Pouze pro orgy'


def translate_accces_right(page):
    if page['ispublic'] == 1:
        return 'Kdokoliv'
    elif page['isprivate'] == 1:
        return 'Náhradníci a hrající'
    elif page['isprivate'] == 2:
        return 'Hrající'
    elif page['isprivate'] == 3:
        return 'Zaplatili'
    else:
        return ''


def translate_menu_typ(item):
    if item['issystem'] == 1:
        if item['isnewpart']:
            return 'Systémová samostatná'
        return 'Systémová'
    else:
        if item['link'] is None:
            return "Skupina menu"
        elif item['idpage'] is None:
            if item['isnewpart']:
                return "Externí samostatná"
            return "Externí"
        else:
            if item['isnewpart']:
                return 'Interní samostatná'
            return 'Interní'


def translate_currentyear(item):
    if item['iscurrentyear'] == 1:
        return 'Jen letošní ročník'

    return 'I starší ročník'


def encode_access_rights(ispublic, isprivate):
    assert isinstance(isprivate, int) and isprivate >= 0 and isprivate <= 3
    assert isinstance(ispublic, int) and ispublic >= 1
    if ispublic == 1:
        return 0
    return isprivate


def decode_access_rights(rights):
    ispublic = 1
    isprivate = 0

    if rights == 0:
        ispublic = 1
        isprivate = 0
    elif rights == 1:
        ispublic = 0
        isprivate = 1
    elif rights == 2:
        ispublic = 0
        isprivate = 2
    elif rights == 3:
        ispublic = 0
        isprivate = 3
    return ispublic, isprivate


def encode_menu_item(menuitem):
    if menuitem['link'] is None:
        pagetype = 2
        issystem = 1
        page = 0
        link = ''
    elif menuitem['link'] == 'login':
        pagetype = 3
        issystem = 1
        page = 0
        link = menuitem['link']
    elif menuitem['link'] == 'logout':
        pagetype = 4
        issystem = 1
        page = 0
        link = menuitem['link']
    elif menuitem['link'] == 'team':
        pagetype = 5
        issystem = 1
        page = 0
        link = menuitem['link']
    elif menuitem['link'] == 'changepassword':
        pagetype = 6
        issystem = 1
        page = 0
        link = menuitem['link']
    elif menuitem['link'] == 'registration_cancel':
        pagetype = 7
        issystem = 1
        page = 0
        link = menuitem['link']
    elif menuitem['link'] == 'teams':
        pagetype = 8
        issystem = 1
        page = 0
        link = menuitem['link']
    elif menuitem['link'] == 'forum':
        pagetype = 9
        issystem = 1
        page = 0
        link = menuitem['link']
    elif menuitem['link'] == 'registration':
        pagetype = 10
        issystem = 1
        page = 0
        link = menuitem['link']
    elif menuitem['idpage'] is not None:
        pagetype = 0
        issystem = 0
        page = menuitem['idpage']
        link = menuitem['link']
    elif menuitem['idpage'] is None and menuitem['link']:
        pagetype = 1
        issystem = 0
        page = 0
        link = menuitem['link']

    else:
        pagetype = 0
        issystem = 0
        link = ''
        page = 0

    return pagetype, link, page, issystem


def decode_menu_item(pagetype, page, link):
    if pagetype == 2:
        idpage = None
        link = None
        issystem = 0
    elif pagetype == 3:
        idpage = None
        link = 'login'
        issystem = 1
    elif pagetype == 4:
        idpage = None
        link = 'logout'
        issystem = 1
    elif pagetype == 5:
        idpage = None
        link = 'team'
        issystem = 1
    elif pagetype == 6:
        idpage = None
        link = 'changepassword'
        issystem = 1
    elif pagetype == 7:
        idpage = None
        link = 'registration_cancel'
        issystem = 1
    elif pagetype == 8:
        idpage = None
        link = 'teams'
        issystem = 1
    elif pagetype == 9:
        idpage = None
        link = 'forum'
        issystem = 1
    elif pagetype == 10:
        idpage = None
        link = 'registration'
        issystem = 1
    elif pagetype == 0:
        idpage = page
        page = get_admin_page(idpage)
        link = page['url']
        issystem = 0
    elif pagetype == 1:
        idpage = None
        # link = link # redundant?
        issystem = 0
    else:
        idpage = None
        link = None
        issystem = 0

    return idpage, link, issystem


def get_admin_pages(year):
    pages = Page.query.filter_by(idYear=year['year']).order_by(Page.idPage).all()
    data = []
    if pages:
        for p in pages:
            page_dict = {
                'idpage': p.idPage, 'idyear': p.idYear, 'title': p.title, 'url': p.url,
                'texy': p.texy, 'html': p.html, 'ispublic': 1 if p.isPublic else 0,
                'isprivate': p.isPrivate, 'isvisible': 1 if p.isVisible else 0,
                'idforumsection': p.idForumSection
            }
            page_dict['visibility'] = translate_visibility(page_dict)
            page_dict['access_right'] = translate_accces_right(page_dict)
            data.append(page_dict)
    return data


def get_admin_page(idpage):
    p = Page.query.get(idpage)
    if p:
        return {
            'idpage': p.idPage, 'idyear': p.idYear, 'title': p.title, 'url': p.url,
            'texy': p.texy, 'html': p.html, 'ispublic': 1 if p.isPublic else 0,
            'isprivate': p.isPrivate, 'isvisible': 1 if p.isVisible else 0,
            'idforumsection': p.idForumSection
        }
    return None


def update_page(idpage, title, url, texy, html, ispublic, isprivate, isvisible, idforumsection):
    try:
        page = Page.query.get(idpage)
        if page:
            page.title = title
            page.url = url
            page.texy = texy
            page.html = html
            page.isPublic = bool(ispublic)
            page.isPrivate = isprivate
            page.isVisible = bool(isvisible)
            page.idForumSection = idforumsection if idforumsection else None
            db.session.commit()
            return True, ""
        return False, "Page not found"
    except Exception as e:
        db.session.rollback()
        return False, db_error_message(e, "uložit úpravy stránky")


def delete_page(idpage):
    try:
        Page.query.filter_by(idPage=idpage).delete()
        db.session.commit()
        return True, ""
    except Exception as e:
        db.session.rollback()
        return False, db_error_message(e, "smazat stránku")


def insert_page(year, title, url, texy, html, ispublic, isprivate, isvisible, idforumsection):
    try:
        new_page = Page(
            idYear=year['year'], title=title, url=url, texy=texy, html=html,
            isPublic=bool(ispublic), isPrivate=isprivate, isVisible=bool(isvisible),
            idForumSection=idforumsection if idforumsection else None
        )
        db.session.add(new_page)
        db.session.commit()
        return True, ""
    except Exception as e:
        db.session.rollback()
        return False, db_error_message(e, "vytvořit stránku")


def get_admin_menu(year):
    menus = Menu.query.filter_by(idYear=year['year']).order_by(Menu.order).all()
    data = []
    if menus:
        for m in menus:
            menu_dict = {
                'idmenu': m.idMenu, 'idpage': m.idPage, 'menu': m.menu, 'link': m.link,
                'order': m.order, 'param': m.param, 'isnewpart': 1 if m.isNewPart else 0,
                'ispublic': 1 if m.isPublic else 0, 'isprivate': m.isPrivate,
                'isvisible': 1 if m.isVisible else 0, 'issystem': 1 if m.isSystem else 0,
                'iscurrentyear': 1 if m.isCurrentYear else 0
            }
            menu_dict['visibility'] = translate_visibility(menu_dict)
            menu_dict['access_right'] = translate_accces_right(menu_dict)
            menu_dict['currentyear'] = translate_currentyear(menu_dict)
            menu_dict['menutyp'] = translate_menu_typ(menu_dict)
            data.append(menu_dict)
    return data


def get_admin_menu_item(year, idmenu):
    m = Menu.query.filter_by(idYear=year['year'], idMenu=idmenu).first()
    if m:
        menu_dict = {
            'idmenu': m.idMenu, 'idpage': m.idPage, 'menu': m.menu, 'link': m.link,
            'order': m.order, 'param': m.param, 'isnewpart': 1 if m.isNewPart else 0,
            'ispublic': 1 if m.isPublic else 0, 'isprivate': m.isPrivate,
            'isvisible': 1 if m.isVisible else 0, 'issystem': 1 if m.isSystem else 0,
            'iscurrentyear': 1 if m.isCurrentYear else 0
        }
        menu_dict['visibility'] = translate_visibility(menu_dict)
        menu_dict['access_right'] = translate_accces_right(menu_dict)
        menu_dict['currentyear'] = translate_currentyear(menu_dict)
        menu_dict['system'] = translate_menu_typ(menu_dict)
        return menu_dict
    return None


def update_menu_item(idmenu, year, idpage, menu, link, order, isnewpart, ispublic, isprivate, isvisible, issystem, iscurrentyear):
    try:
        m = Menu.query.get(idmenu)
        if m:
            m.idYear = year['year']
            m.idPage = idpage if idpage else None
            m.menu = menu
            m.link = link
            m.order = order
            m.isNewPart = bool(isnewpart)
            m.isPublic = bool(ispublic)
            m.isPrivate = isprivate
            m.isVisible = bool(isvisible)
            m.isSystem = bool(issystem)
            m.isCurrentYear = bool(iscurrentyear)
            db.session.commit()
            return True, ""
        return False, "Menu item not found"
    except Exception as e:
        db.session.rollback()
        return False, db_error_message(e, "uložit úpravy položky menu")


def delete_menu_item(idmenu):
    try:
        Menu.query.filter_by(idMenu=idmenu).delete()
        db.session.commit()
        return True, ""
    except Exception as e:
        db.session.rollback()
        return False, db_error_message(e, "smazat položku menu")


def insert_menu_item(year, idpage, menu, link, order, isnewpart, ispublic, isprivate, isvisible, issystem, iscurrentyear):
    try:
        new_menu = Menu(
            idYear=year['year'], idPage=idpage if idpage else None, menu=menu, link=link, order=order,
            isNewPart=bool(isnewpart), isPublic=bool(ispublic), isPrivate=isprivate,
            isVisible=bool(isvisible), isSystem=bool(issystem), isCurrentYear=bool(iscurrentyear)
        )
        db.session.add(new_menu)
        db.session.commit()
        return True, ""
    except Exception as e:
        db.session.rollback()
        return False, db_error_message(e, "vytvořit položku menu")


def get_admin_forum_sections(year):
    sections = ForumSection.query.filter_by(idYear=year['year']).order_by(ForumSection.order).all()
    data = []
    if sections:
        for s in sections:
            section_dict = {
                'idforumsection': s.idForumSection, 'section': s.section,
                'order': s.order, 'isvisible': 1 if s.isVisible else 0
            }
            section_dict['visibility'] = translate_visibility(section_dict)
            data.append(section_dict)
    return data


def get_admin_forum_section(idforumsection):
    s = ForumSection.query.get(idforumsection)
    if s:
        return {
            'idforumsection': s.idForumSection, 'section': s.section,
            'order': s.order, 'isvisible': 1 if s.isVisible else 0
        }
    return None


def update_forum_section(idsection, section, order, isvisible):
    try:
        s = ForumSection.query.get(idsection)
        if s:
            s.section = section
            s.order = order
            s.isVisible = bool(isvisible)
            db.session.commit()
            return True, ""
        return False, "Section not found"
    except Exception as e:
        db.session.rollback()
        return False, db_error_message(e, "uložit úpravy sekce fóra")


def delete_forum_section(idforumsection):
    try:
        Forum.query.filter_by(idForumSection=idforumsection).delete()
        ForumSection.query.filter_by(idForumSection=idforumsection).delete()
        db.session.commit()
        return True, ""
    except Exception as e:
        db.session.rollback()
        return False, db_error_message(e, "smazat sekci fóra")


def insert_forum_section(year, section, order, isvisible):
    try:
        new_section = ForumSection(
            idYear=year['year'], section=section, order=order, isVisible=bool(isvisible)
        )
        db.session.add(new_section)
        db.session.commit()
        return True, ""
    except Exception as e:
        db.session.rollback()
        return False, db_error_message(e, "vytvořit sekci fóra")


def change_admin_pass(password_old, password_new):
    if check_password_org(password_old):
        salt = secrets.token_hex(20)
        hash_new = sha256_crypt.hash(current_app.config['SECRET_PEPPER'] + password_new + salt)
        try:
            p_setting = Setting.query.filter(Setting.idYear == None, Setting.param == 'org-pass').first()
            if p_setting:
                p_setting.value = hash_new
            else:
                db.session.add(Setting(param='org-pass', value=hash_new))

            s_setting = Setting.query.filter(Setting.idYear == None, Setting.param == 'org-salt').first()
            if s_setting:
                s_setting.value = salt
            else:
                db.session.add(Setting(param='org-salt', value=salt))

            db.session.commit()
            return True, ""
        except Exception as e:
            db.session.rollback()
            return False, db_error_message(e, "změnit heslo")

    return False, "Nesprávné staré heslo"


def check_password_org(password):
    try:
        settings = Setting.query.filter(Setting.idYear == None).all()
        hash_in_setting = None
        salt_in_setting = None

        for s in settings:
            if s.param == 'org-pass':
                hash_in_setting = s.value
            elif s.param == 'org-salt':
                salt_in_setting = s.value

        if hash_in_setting and salt_in_setting:
            return sha256_crypt.verify(current_app.config['SECRET_PEPPER'] + password + salt_in_setting, hash_in_setting)

        return False
    except Exception:
        return False


def get_team_players(idteam):
    players = Player.query.filter_by(idTeam=idteam).order_by(Player.order).all()
    return [{'idteam': p.idTeam, 'name': p.name, 'publicname': p.publicName, 'city': p.city, 'age': p.age, 'order': p.order} for p in players]


# key: 'name' or 'publicname'
def players_to_string(players, key='name'):
    hraci = []
    for player in players:
        if player[key]:
            name = player[key]
        else:
            name = 'Anonymous'

        hraci.append(name)

    return ', '.join(hraci)


def translate_team_paid(team):
    if team['ispaid'] == 1:
        return 'Zaplaceno'
    return 'Neplaceno'


def translate_team_status(team):
    if team['isdeleted'] == 1:
        return "Smazaní"
    if team['isbackup'] == 1:
        return 'Náhradníci'

    return 'Hrající'


def is_unique_name(year, name, login):
    q = Team.query.filter_by(idYear=year['year'], name=name)
    if login is not None:
        q = q.filter(Team.login != login)
    return q.count() == 0


def is_unique_loginname(year, name):
    return Team.query.filter_by(idYear=year['year'], login=name).count() == 0


def is_unique_email(year, email, login):
    q = Team.query.filter_by(idYear=year['year'], email=email)
    if login is not None:
        q = q.filter(Team.login != login)
    return q.count() == 0


def is_minimum_players(players, min_players):
    players_count = 0

    for player in players:
        if player['name'] != '':
            players_count += 1

    return bool(players_count >= min_players)


def get_admin_teams(year):
    teams = Team.query.filter_by(idYear=year['year']).order_by(Team.registeredAt).all()
    data = []
    if teams:
        for t in teams:
            data.append({
                'idteam': t.idTeam, 'name': t.name, 'login': t.login, 'mascot': t.mascot,
                'email': t.email, 'mobil': t.mobil, 'weburl': t.webUrl, 'reporturl': t.reportUrl,
                'ispaid': 1 if t.isPaid else 0, 'isbackup': 1 if t.isBackup else 0,
                'isdeleted': 1 if t.isDeleted else 0, 'registeredat': t.registeredAt
            })

    # 22:45:07 - Tom: Pro týmy jde nasazení získat i jako JSON, viz:
    # https://statek.seslost.cz/hradecka-sova-2023/nasazeni/conservative.json

    # Kuca index checking
    kidata = load_ki(fn='./hksova/ki2022-7-17.csv')

    # podrobnosti o tymu
    if data:
        i = 1
        for team in data:
            players = get_team_players(team['idteam'])

            kiplayers = match_ki(kidata, players, team['name'])
            #for kp in kiplayers:
            #    print(kp)

            avgki = sum([p['KI'] for p in kiplayers if p.get('KI') is not None]) / len(kiplayers)
            # print(avgki)

            team['players'] = kiplayers
            # real
            team['players_private'] = players_to_string(kiplayers)
            # for our website & statek
            team['players_public'] = players_to_string(kiplayers, key='publicname')
            team['avgki'] = avgki
            team['order'] = i
            team['zaplaceno'] = translate_team_paid(team)
            team['stav'] = translate_team_status(team)
            i += 1
    return data


def get_admin_team(idteam):
    t = Team.query.get(idteam)
    if t:
        team_dict = {
            'idteam': t.idTeam, 'name': t.name, 'login': t.login, 'mascot': t.mascot,
            'email': t.email, 'mobil': t.mobil, 'weburl': t.webUrl, 'reporturl': t.reportUrl,
            'ispaid': 1 if t.isPaid else 0, 'isbackup': 1 if t.isBackup else 0,
            'isdeleted': 1 if t.isDeleted else 0, 'registeredat': t.registeredAt
        }
        players = get_team_players(team_dict['idteam'])
        team_dict['players'] = players
        team_dict['players_private'] = players_to_string(players)
        team_dict['zaplaceno'] = translate_team_paid(team_dict)
        team_dict['stav'] = translate_team_status(team_dict)
        return team_dict
    return None


def update_admin_team(idteam, year, login, name, email, mobil, weburl, reporturl, ispaid, isdeleted, isbackup, new_players):
    team_dict = get_admin_team(idteam)
    if not team_dict:
        return False, "Team not found"
        
    try:
        t = Team.query.get(idteam)
        t.name = name
        t.email = email
        t.mobil = mobil
        t.webUrl = weburl
        t.reportUrl = reporturl
        t.isPaid = bool(ispaid)
        t.isDeleted = bool(isdeleted)
        t.isBackup = bool(isbackup)
        
        # update players
        for i, player in enumerate(new_players):
            player_in_database = any(saved['order'] == i for saved in team_dict['players'])

            age = player['age'].strip()
            age = int(age) if age.isnumeric() else None
            city = player['city'] if 'city' in player else None

            if player['name'].strip():
                if player_in_database:
                    p = Player.query.filter_by(idTeam=idteam, order=i).first()
                    if p:
                        p.name = player['name']
                        p.publicName = player.get('publicname', '')
                        p.city = city
                        p.age = age
                else:
                    new_p = Player(
                        idTeam=idteam, order=i, name=player['name'],
                        publicName=player.get('publicname', ''), city=city, age=age
                    )
                    db.session.add(new_p)
            else:
                if player_in_database:
                    Player.query.filter_by(idTeam=idteam, order=i).delete()
                    
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, db_error_message(e, "uložit úpravy týmu")

    # recalculate normal and backup teams
    recalculate_teams(year)
    return True, ""


def get_emails_list(year, _filter):
    try:
        q = Team.query.filter_by(idYear=year['year'], isDeleted=False)
        if _filter == "1":
            q = q.filter_by(isPaid=True)
        elif _filter == "2":
            q = q.filter_by(isPaid=False)
        elif _filter == "3":
            q = q.filter_by(isBackup=True)
            
        teams = q.all()
        return [{'email': t.email} for t in teams], True, ""
    except Exception as e:
        return None, False, db_error_message(e, "načíst seznam e-mailů")


def get_settings(year):
    settings = Setting.query.filter_by(idYear=year['year']).order_by(Setting.param).all()
    return [{'idsetting': s.idSetting, 'idyear': s.idYear, 'param': s.param, 'value': s.value} for s in settings]


def get_setting(idsetting):
    s = Setting.query.get(idsetting)
    print(f"IDSET: {idsetting}, S: {s}")
    if s:
        return {'idsetting': s.idSetting, 'idyear': s.idYear, 'param': s.param, 'value': s.value}
    return None


def publish_after_game(year):
    '''
    Assign a forum section to every puzzle of the year that doesn't have one yet.
    Called once the 'po-hre-zverejneno' setting is saved with the current year as
    its value, so section names (which can hint at a puzzle's nature) only appear
    on the forum once the game is over and puzzles are actually being published.
    '''
    try:
        puzzles = Puzzle.query.filter_by(year=year['year'], id_forum_section=None).order_by(Puzzle.position).all()
        if not puzzles:
            return True, ""
        next_order = (db.session.query(func.max(ForumSection.order)).filter_by(idYear=year['year']).scalar() or 0) + 1
        for puzzle in puzzles:
            label = f"Cíl - {puzzle.name}" if puzzle.final else f"Šifra {puzzle.position} - {puzzle.name}"
            section = ForumSection(idYear=year['year'], section=label, order=next_order, isVisible=True)
            db.session.add(section)
            db.session.flush()
            puzzle.id_forum_section = section.idForumSection
            next_order += 1
        db.session.commit()
        return True, ""
    except Exception as e:
        db.session.rollback()
        return False, db_error_message(e, "zveřejnit šifry po hře")


def insert_setting(year, param, value):
    if param == "email-smtp-password":
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=b'246', iterations=390000,)
        key = base64.urlsafe_b64encode(kdf.derive(str.encode(current_app.config['SECRET_PEPPER'])))
        cipher_suite = Fernet(key)
        encoded_text = cipher_suite.encrypt(str.encode(value))
        value = encoded_text.decode("utf-8")
    try:
        new_setting = Setting(idYear=year['year'], param=param, value=value)
        db.session.add(new_setting)
        db.session.commit()
        if param == "po-hre-zverejneno" and value == year['year']:
            publish_after_game(year)
        return True, ""
    except Exception as e:
        db.session.rollback()
        return False, db_error_message(e, "uložit nastavení")


def update_setting(idsetting, param, value):
    if param == "email-smtp-password":
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=b'246', iterations=390000, )
        key = base64.urlsafe_b64encode(kdf.derive(str.encode(current_app.config['SECRET_PEPPER'])))
        cipher_suite = Fernet(key)
        encoded_text = cipher_suite.encrypt(str.encode(value))
        value = encoded_text.decode("utf-8")
    try:
        s = Setting.query.get(idsetting)
        if s:
            s.param = param
            s.value = value
            db.session.commit()
            if param == "po-hre-zverejneno" and value == str(s.idYear):
                publish_after_game({'year': str(s.idYear)})
            return True, ""
        return False, "Setting not found"
    except Exception as e:
        db.session.rollback()
        return False, db_error_message(e, "uložit nastavení")


def delete_setting(idsetting):
    try:
        Setting.query.filter_by(idSetting=idsetting).delete()
        db.session.commit()
        return True, ""
    except Exception as e:
        db.session.rollback()
        return False, db_error_message(e, "smazat nastavení")


def get_mascots():
    mascots = Mascot.query.order_by(Mascot.mascot).all()
    return [{'mascot': m.mascot} for m in mascots]


def get_mascot(mascot):
    m = Mascot.query.get(mascot)
    if m:
        return {'mascot': m.mascot}
    return None


def insert_mascot(mascot):
    try:
        db.session.add(Mascot(mascot=mascot))
        db.session.commit()
        return True, ""
    except Exception as e:
        db.session.rollback()
        return False, db_error_message(e, "přidat maskota")


def update_mascot(oldmascot, newmascot):
    try:
        m = Mascot.query.get(oldmascot)
        if m:
            # Note: changing PK requires cascade or might have issues, usually it's safer to delete and insert if mascot is PK. 
            # However, since the relationships aren't strictly referencing it if it's just a string, it may work. Let's do a simple delete/insert.
            m.mascot = newmascot 
            Mascot.query.filter_by(mascot=oldmascot).delete()
            db.session.add(Mascot(mascot=newmascot))
            db.session.commit()
            return True, ""
        return False, "Mascot not found"
    except Exception as e:
        db.session.rollback()
        return False, db_error_message(e, "upravit maskota")


def delete_mascot(mascot):
    try:
        Mascot.query.filter_by(mascot=mascot).delete()
        db.session.commit()
        return True, ""
    except Exception as e:
        db.session.rollback()
        return False, db_error_message(e, "smazat maskota")


def copy_year(year, next_year):
    try:
        # year
        new_year = Year(idYear=next_year)
        db.session.add(new_year)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, db_error_message(e, "založit nový ročník")

    try:
        # settings
        settings = get_settings(year)
        for setting in settings:
            db.session.add(Setting(idYear=next_year, param=setting['param'], value=setting['value']))
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, db_error_message(e, "zkopírovat nastavení do nového ročníku")

    try:
        # forum_section
        forums = get_admin_forum_sections(year)
        forum_keys = {}
        isvisible = True
        for section in forums:
            new_section = ForumSection(idYear=next_year, section=section['section'], order=section['order'], isVisible=isvisible)
            db.session.add(new_section)
            db.session.flush()
            isvisible = False
            forum_keys[section['idforumsection']] = new_section.idForumSection
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, db_error_message(e, "zkopírovat sekce fóra do nového ročníku")

    try:
        # pages
        pages = get_admin_pages(year)
        pages_keys = {}
        for page in pages:
            forum_section = None
            if page['idforumsection'] and page['idforumsection'] in forum_keys:
                forum_section = forum_keys[page['idforumsection']]

            new_page = Page(
                idYear=next_year, title=page['title'], url=page['url'], texy=page['texy'],
                html=page['html'], isPublic=bool(page['ispublic']), isPrivate=page['isprivate'],
                isVisible=bool(page['isvisible']), idForumSection=forum_section
            )
            db.session.add(new_page)
            db.session.flush()
            pages_keys[page['idpage']] = new_page.idPage
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, db_error_message(e, "zkopírovat stránky do nového ročníku")

    try:
        # menu
        menu = get_admin_menu(year)
        for item in menu:
            page_forum = None
            if item['idpage'] and item['idpage'] in pages_keys:
                page_forum = pages_keys[item['idpage']]

            new_menu = Menu(
                idYear=next_year, idPage=page_forum, menu=item['menu'], link=item['link'],
                param=item['param'], order=item['order'], isNewPart=bool(item['isnewpart']),
                isPublic=bool(item['ispublic']), isPrivate=item['isprivate'],
                isVisible=bool(item['isvisible']), isSystem=bool(item['issystem']),
                isCurrentYear=bool(item['iscurrentyear'])
            )
            db.session.add(new_menu)
        db.session.commit()
        return True, ""
    except Exception as e:
        db.session.rollback()
        return False, db_error_message(e, "zkopírovat menu do nového ročníku")


def get_places(year, with_puzzles=False):
    if with_puzzles:
        results = db.session.query(Place, Puzzle.name, Puzzle.position).outerjoin(Puzzle, Puzzle.id_place == Place.id).filter(Place.year == year).order_by(Puzzle.position).all()
        return [{'id': p.id, 'year': p.year, 'name': p.name, 'latitude': p.latitude, 'longitude': p.longitude, 'puzzle_name': pn, 'puzzle_position': pp} for p, pn, pp in results]
    else:
        places = Place.query.filter_by(year=year).order_by(Place.id).all()
        return [{'id': p.id, 'year': p.year, 'name': p.name, 'latitude': p.latitude, 'longitude': p.longitude} for p in places]


def get_place(pid):
    p = Place.query.get(pid)
    if p:
        return {'id': p.id, 'year': p.year, 'name': p.name, 'latitude': p.latitude, 'longitude': p.longitude}
    return None

def update_place(pid, name, lat, lon):
    try:
        p = Place.query.get(pid)
        if p:
            p.name = name
            p.latitude = float(lat)
            p.longitude = float(lon)
            db.session.commit()
            return True, ""
        return False, "Place not found"
    except Exception as e:
        db.session.rollback()
        return False, db_error_message(e, "uložit úpravy stanoviště")
    
    
def insert_place(year, name, lat, lon):
    try:
        new_place = Place(year=year, name=name, latitude=float(lat), longitude=float(lon))
        print(f"{lat=} {lon=}")
        db.session.add(new_place)
        db.session.commit()
        return True, ""
    except Exception as e:
        db.session.rollback()
        return False, db_error_message(e, "vytvořit stanoviště")


def delete_place(pid):
    try:
        Place.query.filter_by(id=pid).delete()
        db.session.commit()
        return True, ""
    except Exception as e:
        db.session.rollback()
        return False, db_error_message(e, "smazat stanoviště")


def get_puzzles(year):
    puzzles = Puzzle.query.filter_by(year=year).order_by(Puzzle.position).all()
    return [{
        'id': p.id, 'year': p.year, 'position': p.position, 'name': p.name,
        'final': 1 if p.final else 0, 'code': p.code, 'description': p.description,
        'id_place': p.id_place, 
        'place': p.place,
        'specification': p.specification, 'comment': p.comment,
        'url': p.url, 'hint': p.hint, 'hint_interval': p.hint_interval,
        'mandatory_additional_info': 1 if p.mandatory_additional_info else 0,
        'solution': p.solution, 'solution_interval': p.solution_interval,
        'solution_instructions': p.solution_instructions, 'solution_url': p.solution_url,
        'id_forum_section': p.id_forum_section
    } for p in puzzles]


def get_puzzle(pid):
    p = Puzzle.query.get(pid)
    if p:
        return {
            'id': p.id, 'year': p.year, 'position': p.position, 'name': p.name,
            'final': 1 if p.final else 0, 'code': p.code, 'description': p.description,
            'id_place': p.id_place,
            'place': p.place,
            'specification': p.specification, 'comment': p.comment,
            'url': p.url, 'hint': p.hint, 'hint_interval': p.hint_interval,
            'mandatory_additional_info': 1 if p.mandatory_additional_info else 0,
            'solution': p.solution, 'solution_interval': p.solution_interval,
            'solution_instructions': p.solution_instructions, 'solution_url': p.solution_url,
            'id_forum_section': p.id_forum_section
        }
    return None

def get_next_puzzle_position(year):
    puzzles = Puzzle.query.filter_by(year=year).order_by(Puzzle.position.desc()).first()
    if puzzles:
        return puzzles.position + 1
    return 1

def insert_puzzle(year, name, position, final, code, description, id_place, specification, comment, url, hint, hint_interval, mandatory_additional_info, solution, solution_interval, solution_instructions, solution_url, id_forum_section=None):
    try:
        new_puzzle = Puzzle(year=year, name=name, position=position, final=final, code=code, description=description, id_place=id_place, specification=specification, comment=comment, url=url, hint=hint, hint_interval=hint_interval, mandatory_additional_info=mandatory_additional_info, solution=solution, solution_interval=solution_interval, solution_instructions=solution_instructions, solution_url=solution_url, id_forum_section=id_forum_section)
        db.session.add(new_puzzle)
        db.session.commit()
        return new_puzzle.id, ""
    except Exception as e:
        db.session.rollback()
        return None, db_error_message(e, "vytvořit šifru")

def update_puzzle(pid, year, name, position, final, code, description, id_place, specification, comment, url, hint, hint_interval, mandatory_additional_info, solution, solution_interval, solution_instructions, solution_url, id_forum_section=None):
    try:
        p = Puzzle.query.get(pid)
        if p:
            p.year = year
            p.name = name
            p.position = position
            p.final = final
            p.code = code
            p.description = description
            p.id_place = id_place
            p.specification = specification
            p.comment = comment
            p.url = url
            p.hint = hint
            p.hint_interval = hint_interval
            p.mandatory_additional_info = mandatory_additional_info
            p.solution = solution
            p.solution_interval = solution_interval
            p.solution_instructions = solution_instructions
            p.solution_url = solution_url
            p.id_forum_section = id_forum_section
            db.session.commit()
            return True, ""
        return False, "Puzzle not found"
    except Exception as e:
        db.session.rollback()
        return False, db_error_message(e, "uložit úpravy šifry")

def delete_puzzle(pid):
    try:
        Puzzle.query.filter_by(id=pid).delete()
        db.session.commit()
        return True, ""
    except Exception as e:
        db.session.rollback()
        return False, db_error_message(e, "smazat šifru")


def sync_teams_trakar(year, teams):
    # prepare CSV
    output = io.StringIO()
    csv.register_dialect('sova', delimiter=';', quoting=csv.QUOTE_MINIMAL)
    writer = csv.writer(output, dialect='sova')

    # header
    # line = ['external_id', 'name', 'code', 'qr_token', 'phone', 'cancelled', 'members_str']
    line = ['name', 'code', 'qr_token', 'phone', 'cancelled', 'members_str']
    writer.writerow(line)

    # content
    locale.setlocale(locale.LC_ALL, 'cs_CZ.UTF-8')
    for team in sorted(teams, key=lambda x: locale.strxfrm(x['name'].lower())):
        if team['isdeleted'] == 1:
            continue
        # line = [team['idteam'], team['name'], team['mascot'], team['mascot'], team['mobil'], team['isdeleted'], team['players_private']]
        line = [team['name'], team['mascot'], team['mascot'], team['mobil'], team['isdeleted'], team['players_public']]
        # print('XXXXX', line)
        writer.writerow(line)
    output.seek(0)  # rewind to start

    csv_payload = output.getvalue()

    # print('-' * 80)
    # print(csv_payload)
    # print('-' * 80)
    # with open('tmp.csv', mode='wt', encoding='UTF-8') as f:
    #     f.write(csv_payload)

    # perform request to Trakar
    # DOC: https://databaze.seslost.cz/doc/tymy
    #url = f'https://databaze.seslost.cz/hry/hradecka-sova-{year["year"]}/tymy/import.csv?overwrite=1'
    #url = f'https://databaze.seslost.cz/hry/hradecka-sova-{year["year"]}/tymy/import.csv?update=1'
    url = f'https://databaze.seslost.cz/hry/hradecka-sova-{year["year"]}/tymy/import.csv'
    trakar_login = get_trakar_login(year)
    trakar_token = get_trakar_token(year)
    headers = {
        # 'Authorization': f'AUTH-TOKEN {trakar_token}',
        'X-Auth-Login': f'{trakar_login}',
        'X-Auth-Token': f'{trakar_token}',
        'Content-type': 'text/csv',
    }
    payload = csv_payload.encode('utf-8')
    print('request URL: ', url)
    print('request payload: ', payload)
    x = requests.post(url, headers=headers, data=payload)
    print('response: ', x)
    print('response body: ', x.text)
    try:
        json_object = json.loads(x.text)
        json_formatted_str = json.dumps(json_object, indent=2, ensure_ascii=False)
        # print(json_formatted_str)
    except:
        pass
    finally:
        json_formatted_str = f'unparsable JSON: {x.text}'
        pass

    return f'SENT DATA:\n{csv_payload}\nHTTP STATUS CODE: {x.status_code}\nJSON response:\n{json_formatted_str}\n'