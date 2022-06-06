import sys
from flask import current_app
from datetime import datetime

def get_pages(year):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''select idpage, title, url, texy, html, ispublic, isprivate, isvisible from page where idyear=%s order by idpage''', [year['year']])
    data=cursor.fetchall()

    if (data):
        for page in data:
            page['visibility']=get_page_visibility(page)
            page['access_right']=get_page_accces_right(page)
    return data

def get_page_visibility(page):
    if (page['isvisible']==1):
        return 'Viditelné'
    else:
        return 'Pouze pro orgy'

def get_page_accces_right(page):
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

def get_admin_page(idpage):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''select idpage, idyear, title, url, texy, html, ispublic, isprivate, isvisible from page where idpage=%s ''', [idpage])
    data=cursor.fetchone()
    return data

def save_page (idpage, title, url, texy, html, ispublic, isprivate, isvisible):
    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute('''UPDATE page set title=%s, url=%s, texy=%s, html=%s, ispublic=%s, isprivate=%s, isvisible=%s where idpage=%s''', [title, url,texy, html, ispublic, isprivate, isvisible, idpage])
    except Exception as e:
        return False, "Problem updating into db: " + str(e)
    current_app.mysql.connection.commit()
    return True, ""