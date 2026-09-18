'''
Forum - model
'''
from datetime import datetime
from flask import current_app
from sqlalchemy import func
from ..database import db, db_error_message

class ForumSection(db.Model):
    __tablename__ = 'forum_section'
    idForumSection = db.Column(db.Integer, primary_key=True)
    idYear = db.Column(db.Integer, nullable=False)
    section = db.Column(db.String(100), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    isVisible = db.Column(db.Boolean, nullable=False)

class Forum(db.Model):
    __tablename__ = 'forum'
    idForum = db.Column(db.Integer, primary_key=True)
    idForumSection = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    insertedAt = db.Column(db.DateTime, nullable=False)
    ip = db.Column(db.String(15), nullable=False)
    dns = db.Column(db.String(255), nullable=False)
    browser = db.Column(db.String(255), nullable=False)


def get_forum_sections(year):
    sections = ForumSection.query.filter_by(idYear=year['year'], isVisible=True).order_by(ForumSection.order).all()
    data = []
    if sections:
        for section in sections:
            data.append({
                'idforumsection': section.idForumSection,
                'section': section.section,
                'order': section.order,
                'isvisible': 1 if section.isVisible else 0,
                'last_post': get_forum_section_last_post(section.idForumSection)
            })
    return data


def get_forum_section_last_post(id_forum_section):
    max_date = db.session.query(func.max(Forum.insertedAt)).filter_by(idForumSection=id_forum_section).scalar()
    if max_date:
        return max_date.strftime("%-d. %-m. %Y %-H:%M:%S")
    return ""


def get_forum(id_forum_section, startat, perpage):
    posts = Forum.query.filter_by(idForumSection=id_forum_section).order_by(Forum.insertedAt.desc()).offset(startat).limit(perpage).all()
    data = []
    for post in posts:
        data.append({
            'idforumsection': post.idForumSection,
            'name': post.name,
            'text': post.text,
            'insertedAt': post.insertedAt.strftime("%-d. %-m. %Y %-H:%M:%S") if post.insertedAt else "",
            'ip': post.ip,
            'dns': post.dns,
            'browser': post.browser
        })
    return data


def get_forum_post_count(id_forum_section):
    num = db.session.query(func.count(Forum.insertedAt)).filter_by(idForumSection=id_forum_section).order_by(Forum.insertedAt.desc()).scalar()
    return num if num else 0


def insert_post(id_forum_section, name, text, ip, dns, browser):
    now = datetime.now()
    try:
        new_post = Forum(idForumSection=id_forum_section, name=name, text=text, insertedAt=now, ip=ip, dns=dns, browser=browser)
        db.session.add(new_post)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, db_error_message(e, "uložit příspěvek")
    return True, ""
