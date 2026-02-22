'''
Page - model
'''
from flask import current_app
from ..database import db

class Page(db.Model):
    __tablename__ = 'page'
    idPage = db.Column(db.Integer, primary_key=True)
    idYear = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    texy = db.Column(db.Text, nullable=True)
    html = db.Column(db.Text, nullable=False)
    isPublic = db.Column(db.Boolean, nullable=False)
    isPrivate = db.Column(db.Integer, nullable=False)
    isVisible = db.Column(db.Boolean, nullable=False)
    idForumSection = db.Column(db.Integer, nullable=True)


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
    page = Page.query.filter_by(idYear=year['year'], url=url).first()
    if page:
        return {
            'idpage': page.idPage,
            'title': page.title,
            'html': page.html,
            'ispublic': page.isPublic,
            'isprivate': page.isPrivate,
            'isvisible': page.isVisible,
            'idforumsection': page.idForumSection
        }
    return None
