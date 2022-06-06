import sys
from flask import current_app
from datetime import datetime

def get_page(year, url):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''select title, html, ispublic, isprivate, isvisible from page where idyear=%s and url=%s''', [year['year'], url])
    data=cursor.fetchone()
    return data
