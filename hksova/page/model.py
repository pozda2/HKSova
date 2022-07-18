'''
Page - model
'''
from flask import current_app


def get_page(year, url):
    '''
    Get page content from DB

    Parameters
    ----------
    year: dict: a desired year
    url: string: page URL

    Returns
    -------
    data: dict: page data from DB
    '''
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''select idpage, title, html, ispublic, isprivate, isvisible, idforumsection from page where idyear=%s and url=%s''', [year['year'], url])
    data = cursor.fetchone()
    return data
