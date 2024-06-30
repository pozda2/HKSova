import base64
from datetime import datetime, timedelta
from dateutil import parser
from flask import current_app
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def get_settings_year(year, param):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''SELECT value FROM setting where idYear=%s and param=%s''', [year['year'], param])
    data = cursor.fetchall()
    if not data:
        return None
    value = data[0]['value']

    if param == "email-smtp-password":
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=b'246', iterations=390000, )
        key = base64.urlsafe_b64encode(kdf.derive(str.encode(current_app.config['SECRET_PEPPER'])))
        cipher_suite = Fernet(key)
        encoded_text = str.encode(data[0]['value'])
        decoded_text = cipher_suite.decrypt(encoded_text)
        value = decoded_text.decode("utf-8")
    return value


def get_settings_global(param):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('''SELECT value FROM setting where idYear is null and param=%s''', [param])
    data = cursor.fetchall()
    return data[0]['value']


def is_registration_open(year):
    reg_from = parser.parse(get_settings_year(year, 'reg-from'))
    reg_to = parser.parse(get_settings_year(year, 'reg-to'))
    today = datetime.now()

    return bool(today > reg_from and (today < reg_to + timedelta(days=1)))


def get_registration_from(year):
    return parser.parse(get_settings_year(year, "reg-from")).strftime("%-d. %-m. %Y")


def get_registration_to(year):
    return parser.parse(get_settings_year(year, "reg-to")).strftime("%-d. %-m. %Y")


def get_min_players(year):
    return int(get_settings_year(year, "min-players"))


def get_max_players(year):
    return int(get_settings_year(year, "max-players"))


def get_max_teams(year):
    return int(get_settings_year(year, "max-teams"))


def get_trakar_token(year):
    return get_settings_year(year, "trakar-token")


def get_trakar_login(year):
    return get_settings_year(year, "trakar-login")


def get_payment_information(year):
    data = {}
    data['account'] = get_settings_year(year, 'payment-account')
    data['iban'] = get_settings_year(year, "payment-iban")
    data['price'] = get_settings_year(year, 'payment-price')
    data['unit'] = get_settings_year(year, 'payment-unit')
    data['to'] = parser.parse(get_settings_year(year, "payment-to")).strftime("%-d. %-m. %Y")
    return data
