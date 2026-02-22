from flask import current_app
from ..database import db

class Menu(db.Model):
    __tablename__ = 'menu'
    idMenu = db.Column(db.Integer, primary_key=True)
    idYear = db.Column(db.Integer, nullable=False)
    idPage = db.Column(db.Integer, nullable=True)
    menu = db.Column(db.String(50), nullable=False)
    link = db.Column(db.String(255), nullable=True)
    param = db.Column(db.String(255), nullable=True)
    order = db.Column(db.Integer, nullable=False)
    isNewPart = db.Column(db.Boolean, nullable=False)
    isPublic = db.Column(db.Boolean, nullable=False)
    isPrivate = db.Column(db.Integer, nullable=False)
    isVisible = db.Column(db.Boolean, nullable=False)
    isSystem = db.Column(db.Boolean, nullable=False)
    isCurrentYear = db.Column(db.Boolean, nullable=False)


def get_menu(year):
    from sqlalchemy import text
    menus = Menu.query.filter_by(idYear=year['year']).order_by(Menu.order).all()
    
    data = []
    for m in menus:
        data.append({
            'idmenu': m.idMenu,
            'idpage': m.idPage,
            'menu': m.menu,
            'link': m.link,
            'isnewpart': 1 if m.isNewPart else 0, # Map to int as the template likely expects 1/0
            'ispublic': 1 if m.isPublic else 0,
            'isprivate': m.isPrivate,
            'isvisible': 1 if m.isVisible else 0,
            'issystem': 1 if m.isSystem else 0,
            'iscurrentyear': 1 if m.isCurrentYear else 0
        })

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
