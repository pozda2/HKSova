from flask import session
from flask import redirect
from flask import url_for
from flask import flash
from flask import request
from ..year.model import *
from functools import wraps
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "logged" not in session:
            flash ("Musíte se přihlásit", "info")
            return redirect (url_for("team.view_login"))
        return func(*args, **kwargs)
    return decorated_function

def current_year_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        year=get_year(request.blueprint)
        if not year['is_current_year']:
            flash ("Stránka dostupná pouze v aktuálním ročníku", "error")
            return redirect (url_for("main.view_index"))
        return func(*args, **kwargs)
    return decorated_function

def send_reset_code(year, code, login, email):
    # read settings
    email_smtp_password=get_settings_year(year, 'email-smtp-password')
    email_smtp_user=get_settings_year(year, 'email-smtp-user')
    email_smtp_server=get_settings_year(year, 'email-smtp-server')
    email_smtp_port=get_settings_year(year, 'email-smtp-port')
    email_smtp_from=get_settings_year(year, 'email-smtp-from')
    email_smtp_auth=get_settings_year(year, 'email-smtp-auth')
    base_url=get_settings_year(year, 'base-url')
    
    if email_smtp_server is None: return False, "Nenastaven email-smtp-server"
    if email_smtp_port is None: return False, "Nenastaven email-smtp-port"
    if email_smtp_auth is None: return False, "Nenastaven email-smtp-auth"
    if email_smtp_user is None: return False, "Nenastaven email-smtp-user"
    if email_smtp_password is None: return False, "Nenastaven email-smtp-password"
    if email_smtp_from is None: return False, "Nenastaven email-smtp-from"
    if base_url is None: return False, "Nenastaven base-url"

    s, status, message=connect_to_smtp(email_smtp_server, email_smtp_port, email_smtp_auth, email_smtp_user, email_smtp_password)
    if not status:
        return False, message

    reset_link=base_url+"/resetpassword/"+code
    messages=[]
    msg = MIMEMultipart()
    msg['From'] = email_smtp_from
    msg['To'] = email
    msg['Subject']="Reset hesla - Hradecka sova"

    message = f"<HTML>\n<HEAD>\n<TITLE>Reset hesla - Hradecka sova</TITLE>"
    message+=f"<META HTTP-EQUIV=\'Content-Type\' CONTENT=\'text/html\'>\n"
    message+="</HEAD>\n<BODY>\n"
    message+="<p>Na stránkách Hradecké sovy, jste požádali o reset hesla. Zaslaný odkaz na zadání nového hesla je platný 15 minut."
    message+=f"<p>Přihlašovací jméno je: {login}"
    message+=f"<p>Odkaz na reset hesla: <a href='{reset_link}'>{reset_link}</a>"
    message+=f"<p><p>V případě problémů nás kontaktujte emailem."
    message+=f"<p><p>Orgové"
    message+="</BODY></HTML>"
    msg.attach(MIMEText(message, 'html'))
    messages.append(msg)

    for m in (messages):
        try:
            s.sendmail(email_smtp_from, email, m.as_string())
        except (smtplib.SMTPDataError, smtplib.SMTPRecipientsRefused) as e:
            return False, e
        except:
            return False, e

    disconnect_from_stmp(s)
    return True, ""

def connect_to_smtp(server, port, auth, user, password):
    if (auth.upper() == "BASIC"):
        try:
            s = smtplib.SMTP(server , str(port))
        except smtplib.SMTPException as e:
            return None, False, e
        return s, True, ""

    elif (auth.upper() == "SSL"):
        smtp_server=server + ":" + str(port)
        try:
            s = smtplib.SMTP_SSL(smtp_server)
            if (user  and password ):
                s.login(user, password)
        except smtplib.SMTPException as e:
            return None, False, e
        return s, True, ""
        
    elif (auth.upper() == "STARTTLS"):
        smtp_server=server + ":" + str(port)
        try:
            s = smtplib.SMTP(server , str(port))
            s.ehlo() 
            s.starttls()
            s.ehlo()
            if (user  and password ):
                s.login(user, password)
        except smtplib.SMTPException as e:
            return None, False, e
        return s, True, ""

def disconnect_from_stmp(connection):
    if connection is not None:
        connection.quit()

