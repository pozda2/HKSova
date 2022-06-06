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
        return 'Kdykoliv'
    else:
        if (page['isprivate']==1):
            return 'Náhradníci a hrající'
        elif (page['isprivate']==2):
             return 'Hrající'
        elif (page['isprivate']==3):
            return 'Zaplatili'
        else:
            return ''