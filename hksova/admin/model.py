from flask import current_app
import secrets
from passlib.hash import sha256_crypt
from ..team.model import *

def translate_visibility(page):
    if (page['isvisible']==1):
        return 'Viditelné'
    else:
        return 'Pouze pro orgy'

def translate_accces_right(page):
        if (page['ispublic']==1):
            return 'Kdokoliv'
        elif (page['isprivate']==1):
            return 'Náhradníci a hrající'
        elif (page['isprivate']==2):
             return 'Hrající'
        elif (page['isprivate']==3):
            return 'Zaplatili'
        else:
            return ''

def translate_menu_typ(item):
    if (item['issystem']==1):
        if item['isnewpart']:
            return 'Systémová samostatná'
        else:
            return 'Systémová'
    else:
        if item['link'] is None:
            return "Skupina menu"
        elif item['idpage'] is None:
            if item['isnewpart']:
                return "Externí samostatná"
            else:
                return "Externí"
        else:
            if item['isnewpart']:
                return 'Interní samostatná'
            else:
                return 'Interní'

def translate_currentyear(item):
    if (item['iscurrentyear']==1):
        return 'Jen letošní ročník'
    else:
        return 'I starší ročník'

def encode_access_rights(ispublic, isprivate):
    if ispublic==1: return 0
    if isprivate==1: return 1
    elif isprivate==2: return 2
    elif isprivate==3: return 3

def decode_access_rights (rights):
    ispublic=1
    isprivate=0

    if rights==0:
        ispublic=1
        isprivate=0
    elif rights==1:
        ispublic=0
        isprivate=1
    elif rights==2:
        ispublic=0
        isprivate=2
    elif rights==3:
        ispublic=0
        isprivate=3
    return ispublic, isprivate

def encode_menu_item(menuitem):
    if menuitem['link'] is None:
        pagetype=2
        issystem=1
        page=0
        link=''
    elif menuitem['link']=='login':
        pagetype=3
        issystem=1
        page=0
        link=menuitem['link']
    elif menuitem['link']=='logout':
        pagetype=4
        issystem=1
        page=0
        link=menuitem['link']
    elif menuitem['link']=='team':
        pagetype=5
        issystem=1
        page=0
        link=menuitem['link']
    elif menuitem['link']=='changepassword':
        pagetype=6
        issystem=1
        page=0
        link=menuitem['link']
    elif menuitem['link']=='registration_cancel':
        pagetype=7
        issystem=1
        page=0
        link=menuitem['link']
    elif menuitem['link']=='teams':
        pagetype=8
        issystem=1
        page=0
        link=menuitem['link']
    elif menuitem['link']=='forum':
        pagetype=9
        issystem=1
        page=0
        link=menuitem['link']
    elif menuitem['link']=='registration':
        pagetype=10
        issystem=1
        page=0
        link=menuitem['link']
    elif (menuitem['idpage'] is not None):
        pagetype=0
        issystem=0
        page=menuitem['idpage']
        link=menuitem['link']
    elif (menuitem['idpage'] is None and menuitem['link']):
        pagetype=1
        issystem=0
        page=0
        link=menuitem['link']
        
    else:
        pagetype=0
        issystem=0
        link=''
        page=0

    return pagetype, link, page, issystem

def decode_menu_item(pagetype, page, link):
    if pagetype==2:
        idpage=None
        link=None
        issystem=0
    elif pagetype==3:
        idpage=None
        link='login'
        issystem=1
    elif pagetype==4:
        idpage=None
        link='logout'
        issystem=1
    elif pagetype==5:
        idpage=None
        link='team'
        issystem=1
    elif pagetype==6:
        idpage=None
        link='changepassword'
        issystem=1
    elif pagetype==7:
        idpage=None
        link='registration_cancel'
        issystem=1
    elif pagetype==8:
        idpage=None
        link='teams'
        issystem=1
    elif pagetype==9:
        idpage=None
        link='forum'
        issystem=1
    elif pagetype==10:
        idpage=None
        link='registration'
        issystem=1
    elif pagetype==0:
        idpage=page
        page=get_admin_page(idpage)
        link=page['url']
        issystem=0
    elif pagetype==1:
        idpage=None
        link=link
        issystem=0
    else:
        idpage=None
        link=None
        issystem=0

    return idpage, link, issystem

def get_admin_pages(year):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''select idpage, title, url, texy, html, ispublic, isprivate, isvisible from page where idyear=%s order by idpage''', [year['year']])
    data=cursor.fetchall()

    if (data):
        for page in data:
            page['visibility']=translate_visibility(page)
            page['access_right']=translate_accces_right(page)
    return data

def get_admin_page(idpage):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''select idpage, idyear, title, url, texy, html, ispublic, isprivate, isvisible, idforumsection from page where idpage=%s ''', [idpage])
    data=cursor.fetchone()
    return data

def update_page (idpage, title, url, texy, html, ispublic, isprivate, isvisible, idforumsection):
    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute('''UPDATE page set title=%s, url=%s, texy=%s, html=%s, ispublic=%s, isprivate=%s, isvisible=%s, idforumsection=%s where idpage=%s''', [title, url,texy, html, ispublic, isprivate, isvisible, idforumsection, idpage])
    except Exception as e:
        return False, "Problem updating into db: " + str(e)
    current_app.mysql.connection.commit()
    return True, ""

def delete_page(idpage):
    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute('''DELETE FROM page where idpage=%s''', [idpage] )
    except Exception as e:
        return False, "Problem deleting from db: " + str(e)
    current_app.mysql.connection.commit()
    return True, ""

def insert_page(year, title, url, texy, html, ispublic, isprivate, isvisible, idforumsection):
    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute('''INSERT INTO page (idyear, title, url, texy, html, ispublic, isprivate, isvisible, idforumsection)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                       [year['year'], title, url, texy, html, ispublic, isprivate, isvisible, idforumsection] )
    except Exception as e:
        return False, "Problem inserting into db: " + str(e)
    current_app.mysql.connection.commit()
    return True, ""

def get_admin_menu(year):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''select idmenu, idpage, menu, link, `order`, isnewpart, ispublic, isprivate, isvisible, issystem, iscurrentyear from menu where idyear=%s order by `order`''', [year['year']])
    data=cursor.fetchall()

    if (data):
        for menu in data:
            menu['visibility']=translate_visibility(menu)
            menu['access_right']=translate_accces_right(menu)
            menu['currentyear']=translate_currentyear(menu)
            menu['menutyp']=translate_menu_typ(menu)
    return data

def get_admin_menu_item(year, idmenu):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''select idpage, menu, link, `order`, isnewpart, ispublic, isprivate, isvisible, issystem, iscurrentyear from menu where idyear=%s and idmenu=%s''', [year['year'], idmenu])
    data=cursor.fetchone()

    if (data):
        data['visibility']=translate_visibility(data)
        data['access_right']=translate_accces_right(data)
        data['currentyear']=translate_currentyear(data)
        data['system']=translate_menu_typ(data)
    return data

def update_menu_item(idmenu, year, idpage, menu, link, order, isnewpart, ispublic, isprivate, isvisible, issystem, iscurrentyear):
    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute('''UPDATE menu set idyear=%s, idpage=%s, menu=%s, link=%s, `order`=%s, isnewpart=%s, ispublic=%s, isprivate=%s, isvisible=%s, issystem=%s, iscurrentyear=%s where idmenu=%s''',
        [ year['year'], idpage, menu, link, order, isnewpart, ispublic, isprivate, isvisible, issystem, iscurrentyear, idmenu] )
    except Exception as e:
        return False, "Problem updating into db: " + str(e)
    current_app.mysql.connection.commit()
    return True, ""

def delete_menu_item(idmenu):
    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute('''DELETE FROM menu where idmenu=%s''', [idmenu] )
    except Exception as e:
        return False, "Problem deleting from db: " + str(e)
    current_app.mysql.connection.commit()
    return True, ""

def insert_menu_item(year, idpage, menu, link, order, isnewpart, ispublic, isprivate, isvisible, issystem, iscurrentyear):
    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute('''INSERT INTO menu (idyear, idpage, menu, link, `order`, isnewpart, ispublic, isprivate, isvisible, issystem, iscurrentyear)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                       [year['year'], idpage, menu, link, order, isnewpart, ispublic, isprivate, isvisible, issystem, iscurrentyear] )
    except Exception as e:
        return False, "Problem inserting into db: " + str(e)
    current_app.mysql.connection.commit()
    return True, ""

def get_admin_forum_sections(year):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''select idforumsection, section, `order`, isvisible from forum_section where idyear=%s order by `order`''', [year['year']])
    data=cursor.fetchall()

    if (data):
        for section in data:
            section['visibility']=translate_visibility(section)
    return data

def get_admin_forum_section(idforumsection):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''select section, `order`, isvisible from forum_section where idforumsection=%s ''', [idforumsection])
    data=cursor.fetchone()
    return data

def update_forum_section(idsection, section, order, isvisible):
    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute('''UPDATE forum_section set section=%s, `order`=%s, isvisible=%s where idforumsection=%s''',
        [ section, order, isvisible, idsection] )
    except Exception as e:
        return False, "Problem updating into db: " + str(e)
    current_app.mysql.connection.commit()
    return True, ""

def delete_forum_section(idforumsection):
    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute('''DELETE FROM forum where idforumsection=%s''', [idforumsection] )
    except Exception as e:
        return False, "Problem deleting from db: " + str(e)

    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute('''DELETE FROM forum_section where idforumsection=%s''', [idforumsection] )
    except Exception as e:
        return False, "Problem deleting from db: " + str(e)

    current_app.mysql.connection.commit()
    return True, ""

def insert_forum_section(year, section, order, isvisible):
    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute('''INSERT INTO forum_section (idyear, section, `order`, isvisible)
                       VALUES (%s, %s, %s, %s)''',
                       [year['year'], section, order, isvisible] )
    except Exception as e:
        return False, "Problem inserting into db: " + str(e)
    current_app.mysql.connection.commit()
    return True, ""

def change_admin_pass (password_old, password_new):
    if (check_password_org (password_old)):
        salt=secrets.token_hex(20)
        hash_new = sha256_crypt.hash(current_app.config['SECRET_PEPPER'] + password_new + salt)
        try:
            cursor = current_app.mysql.connection.cursor()
            cursor.execute('''UPDATE setting set `value`=%s where idyear is null and param=%s ''', [hash_new, 'org-pass'])
        except Exception as e:
            return False, "Problem updating db: " + str(e)

        try:
            cursor = current_app.mysql.connection.cursor()
            cursor.execute('''UPDATE setting set `value`=%s where idyear is null and param=%s ''', [salt, 'org-salt'])
        except Exception as e:
            return False, "Problem updating db: " + str(e)

        current_app.mysql.connection.commit()
        return True, ""
    else:
        return False, "Nesprávné staré heslo"

def check_password_org (password):
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

def translate_team_paid(team):
    if (team['ispaid']==1):
        return 'Zaplaceno'
    else:
        return 'Neplaceno'

def translate_team_status(team):
    if (team['isdeleted']==1):
        return "Smazaní"
    if (team['isbackup']==1):
        return 'Náhradníci'
    else:
        return 'Hrající'

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

def get_admin_teams(year):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''SELECT  idteam, name, login, mascot, email, mobil, weburl, reporturl, ispaid, isbackup, isdeleted, registeredat FROM team where idYear=%s order by registeredAt''', [year['year']])
    data=cursor.fetchall()

    # podrobnosti o tymu
    if (data):
        i=1
        for team in data:
            players=get_team_players(team['idteam'])
            team['player']=players
            team['players_private']=players_to_string(players)
            team['order']=i
            team['zaplaceno']=translate_team_paid(team)
            team['stav']=translate_team_status(team)
            i+=1
    return data

def get_admin_team(idteam):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''SELECT  idteam, name, login, mascot, email, mobil, weburl, reporturl, ispaid, isbackup, isdeleted, registeredat FROM team where idteam=%s ''', [idteam])
    data=cursor.fetchone()

    # podrobnosti o tymu
    if (data):
        players=get_team_players(data['idteam'])
        data['players']=players
        data['players_private']=players_to_string(players)
        data['zaplaceno']=translate_team_paid(data)
        data['stav']=translate_team_status(data)
    return data

def update_admin_team (idteam, year, login, name, email, mobil, weburl, reporturl, ispaid, isdeleted, isbackup, new_players):
    team=get_admin_team(idteam)
    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute('''UPDATE team set name=%s, email=%s, mobil=%s, weburl=%s, reporturl=%s, isPaid=%s, isDeleted=%s, isBackup=%s where idyear=%s and login=%s''',
            [name, email, mobil, weburl, reporturl, ispaid, isdeleted, isbackup, year['year'], login])
    except Exception as e:
        return False, "Problem updatint db: " + str(e)

    # recalculate normal and backup teams
    status, message = recalculate_teams(year)

    # update players
    for i, player in enumerate(new_players):

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

def get_emails_list(year, filter):
    try:
        cursor = current_app.mysql.connection.cursor()
        if (filter=="1"):
            cursor.execute('''SELECT  email FROM team where idYear=%s and isdeleted=0 and ispaid=1''', [year['year']])
        elif (filter=="2"):
            cursor.execute('''SELECT  email FROM team where idYear=%s and isdeleted=0 and ispaid=0''', [year['year']])
        elif (filter=="3"):
            cursor.execute('''SELECT  email FROM team where idYear=%s and isdeleted=0 and isbackup=1''', [year['year']])
        else:
            cursor.execute('''SELECT  email FROM team where idYear=%s and isdeleted=0 ''', [year['year']])
        data=cursor.fetchall()
    except Exception as e:
        return None, False, "Problem reading from db: " + str(e)
    return data, True, ""

def get_settings(year):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''select idsetting, idyear, param, value from setting where idyear=%s order by param''', [year['year']])
    data=cursor.fetchall()
    return data

def get_setting(idsetting):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''select idsetting, idyear, param, value from setting where idsetting=%s order by param''', [idsetting])
    data=cursor.fetchone()
    return data

def insert_setting(year, param, value):
    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute('''INSERT INTO setting (idyear, param, `value`)
                       VALUES (%s, %s, %s)''',
                       [year['year'], param, value] )
    except Exception as e:
        return False, "Problem inserting into db: " + str(e)
    current_app.mysql.connection.commit()
    return True, ""

def update_setting(idsetting, param, value):
    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute('''UPDATE setting set param=%s, `value`=%s where idsetting=%s''',
        [ param, value, idsetting] )
    except Exception as e:
        return False, "Problem updating into db: " + str(e)
    current_app.mysql.connection.commit()
    return True, ""

def delete_setting(idsetting):
    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute('''DELETE FROM setting where idsetting=%s''', [idsetting] )
    except Exception as e:
        return False, "Problem deleting from db: " + str(e)
    current_app.mysql.connection.commit()
    return True, ""

def get_mascots():
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''select mascot from mascot order by mascot''')
    data=cursor.fetchall()
    return data

def get_mascot(mascot):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''select mascot from mascot where mascot=%s''', [mascot])
    data=cursor.fetchone()
    return data

def insert_mascot(mascot):
    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute('''INSERT INTO mascot (mascot)
                       VALUES (%s)''',
                       [mascot] )
    except Exception as e:
        return False, "Problem inserting into db: " + str(e)
    current_app.mysql.connection.commit()
    return True, ""

def update_mascot(oldmascot, newmascot):
    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute('''UPDATE mascot set mascot=%s where mascot=%s''', [ newmascot, oldmascot] )
    except Exception as e:
        return False, "Problem updating into db: " + str(e)
    current_app.mysql.connection.commit()
    return True, ""

def delete_mascot(mascot):
    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute('''DELETE FROM mascot where mascot=%s''', [mascot] )
    except Exception as e:
        return False, "Problem deleting from db: " + str(e)
    current_app.mysql.connection.commit()
    return True, ""
