'''
Forum - model
'''
from datetime import datetime
from flask import current_app


def get_forum_sections(year):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''select idforumsection, section, `order`, isvisible from forum_section where isvisible=1 and idyear=%s order by `order`''', [year['year']])
    data = cursor.fetchall()

    if data:
        for section in data:
            section['last_post'] = get_forum_section_last_post(section['idforumsection'])
    return data


def get_forum_section_last_post(id_forum_section):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''select max(insertedAt) insertedAt from forum where idForumSection=%s''', [id_forum_section])
    data = cursor.fetchall()

    # TODO: probably wrong code - only first row is evaluated (return ends whole function)
    for section in data:
        if section['insertedAt'] is not None:
            return section['insertedAt'].strftime("%-d. %-m. %Y %-H:%M:%S")
        else:
            return ""


def get_forum(id_forum_section, startat, perpage):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''select idforumsection, name, text, insertedAt, ip, dns, browser from forum where idforumsection = %s order by insertedAt desc limit %s, %s''', [id_forum_section, startat, perpage])
    data = cursor.fetchall()

    for section in data:
        if section['insertedAt'] is not None:
            section['insertedAt'] = section['insertedAt'].strftime("%-d. %-m. %Y %-H:%M:%S")
        else:
            section['insertedAt'] = ""

    return data


def get_forum_post_count(id_forum_section):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''select count(insertedAt) num from forum where idforumsection = %s order by insertedAt desc''', [id_forum_section])
    data = cursor.fetchall()
    if data:
        return data[0]['num']
    return 0


def insert_post(id_forum_section, name, text, ip, dns, browser):
    now = datetime.now()

    try:
        cursor = current_app.mysql.connection.cursor()
        cursor.execute('''INSERT INTO forum (idforumsection, name, text, insertedAt, ip, dns, browser) VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                       [id_forum_section, name, text, now, ip, dns, browser])
    except Exception as e:
        return False, "Problem inserting into db: " + str(e)
    current_app.mysql.connection.commit()
    return True, ""
