from flask import current_app


def get_menu(year):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''SELECT idmenu, idpage, menu, link, isnewpart, ispublic, isprivate, isvisible, issystem,iscurrentyear FROM menu where idyear=%s order by `order`''', [year['year']])
    data = cursor.fetchall()

    # TODO: use dict to map link -> blueprint, function
    if data:
        for item in data:
            if item['link'] == 'login':
                item['blueprint'] = 'team'
                item['function'] = 'login_team'
                item['param'] = ""
            elif item['link'] == 'logout':
                item['blueprint'] = 'team'
                item['function'] = 'logout_team'
                item['param'] = ""
            elif item['link'] == 'team':
                item['blueprint'] = 'team'
                item['function'] = 'view_team'
                item['param'] = ""
            elif item['link'] == 'changepassword':
                item['blueprint'] = 'team'
                item['function'] = 'view_password_change'
                item['param'] = ""
            elif item['link'] == 'registration_cancel':
                item['blueprint'] = 'team'
                item['function'] = 'view_registration_cancel'
                item['param'] = ""
            elif item['link'] == 'teams':
                item['blueprint'] = 'team'
                item['function'] = 'view_teams'
                item['param'] = ""
            elif item['link'] == 'registration':
                item['blueprint'] = 'team'
                item['function'] = 'view_registration'
                item['param'] = ""
            elif item['link'] == 'forum':
                item['blueprint'] = 'forum'
                item['function'] = 'view_forum_section'
                item['param'] = ""
            elif item['idpage'] is not None:
                item['blueprint'] = 'main'
                item['function'] = 'view_page'
                item['param'] = item['link']
            elif item['link'] is None:
                item['blueprint'] = ''
                item['function'] = ''
                item['param'] = ''
            else:
                item['blueprint'] = ''
                item['function'] = ''
                item['param'] = item['link']
    return data
