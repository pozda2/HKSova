from flask import current_app
import secrets
from passlib.hash import sha256_crypt

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