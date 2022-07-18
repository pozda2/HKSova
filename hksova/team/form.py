import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, FieldList, FormField
from wtforms.validators import length, InputRequired, Email, ValidationError


def validate_url(form, field):
    if field.data:
        regex = (
            r"^[a-z]+://"
            r"(?P<host>[^\/\?:]+)"
            r"(?P<port>:[0-9]+)?"
            r"(?P<path>\/.*?)?"
            r"(?P<query>\?.*)?$"
        )
        result = re.search(regex, field.data)
        if not result:
            raise ValidationError('URL je neplatné')

        return result


# TODO: duplicity admin/form.py
# TODO: unused parameter form (is it mandatory?)
def validate_age(form, field, _min=10, _max=100):
    if field.data:
        if field.data.isnumeric():
            age = int(field.data)
            if age < _min or age > _max:
                raise ValidationError(f"Věk není v rozsahu {min} až {max}.")
        else:
            raise ValidationError('Věk není číslo')


class LoginForm(FlaskForm):
    loginname = StringField("Přihlašovací jméno", validators=[InputRequired(), length(max=100)])
    password = PasswordField("Heslo", validators=[InputRequired(), length(max=100)])


class PlayerForm(FlaskForm):
    name = StringField("Jméno hráče", validators=[length(max=100, message='Maximální délka jména je 100 znaků')])
    publicname = StringField("Veřejné jméno hráče", validators=[length(max=100, message='Maximální délka jména je 100 znaků')])
    city = StringField("Město", validators=[length(max=100, message='Maximální délka města je 100 znaků')])
    age = StringField("Věk", validators=[validate_age])


class RegistrationForm(FlaskForm):
    name = StringField("Název týmu", validators=[InputRequired(), length(min=1, max=100, message='Délka názvu týmu musí být v rozsahu 1-100) znaků')])
    loginname = StringField("Přihlašovací jméno", validators=[InputRequired(), length(min=4, max=100, message='Délka přihlašovacího jména musí být v rozsahu 4-100) znaků')])
    password = PasswordField("Heslo", validators=[InputRequired(), length(min=6, max=100, message='Délka hesla musí být v rozsahu (6-100) znaků')])
    password2 = PasswordField("Heslo znovu", validators=[InputRequired(), length(min=6, max=100, message='Délka hesla musí být v rozsahu (6-100) znaků')])
    email = StringField("Email", validators=[InputRequired(), length(max=255, message='Maximální délka email je 255 znaků'), Email()])
    mobil = StringField("Telefon", validators=[InputRequired(), length(max=30, message='Maximální délka telefonu je 30 znaků')])
    weburl = StringField("Web stránka týmu (URL)", validators=[length(max=255, message='Maximální délka URL je 255 znaků'), validate_url])
    reporturl = StringField("Web stránka s reportáží (URL)", validators=[length(max=255, message='Maximální délka URL je 255 znaků')])
    agree = BooleanField("Všichni hráči byli seznámeni a souhlasí s pravidly a charakterem hry.", validators=[InputRequired()])
    agree2 = BooleanField("Všichni účastnici dávají souhlas se shromažďováním osobních údajů pro účel uspořádání hry a evidenci hráčů, výsledků.", validators=[InputRequired()])
    players = FieldList(FormField(PlayerForm))


class RegistrationCancelForm(FlaskForm):
    agree = BooleanField("Opravdu chcete zrušit vaši účast na hře?", validators=[InputRequired()])


class EditTeamForm(FlaskForm):
    name = StringField("Název týmu", validators=[InputRequired(), length(min=1, max=100, message='Délka názvu týmu musí být v rozsahu 1-100) znaků')])
    email = StringField("Email", validators=[InputRequired(), length(max=255, message='Maximální délka email je 255 znaků'), Email()])
    mobil = StringField("Telefon", validators=[InputRequired(), length(max=30, message='Maximální délka telefonu je 30 znaků')])
    weburl = StringField("Web stránka týmu (URL)", validators=[length(max=255, message='Maximální délka URL je 255 znaků'), validate_url])
    reporturl = StringField("Web stránka s reportáží (URL)", validators=[length(max=255, message='Maximální délka URL je 255 znaků'), validate_url])
    players = FieldList(FormField(PlayerForm))


class PasswordChangeForm(FlaskForm):
    password_old = PasswordField("Staré heslo", validators=[InputRequired(), length(min=6, max=100)])
    password1 = PasswordField("Nové heslo", validators=[InputRequired(), length(min=6, max=100)])
    password2 = PasswordField("Nové heslo znovu", validators=[InputRequired(), length(min=6, max=100)])


class ForgetPasswordForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), length(max=255, message='Maximální délka email je 255 znaků'), Email()])


class ResetPasswordForm(FlaskForm):
    password1 = PasswordField("Nové heslo", validators=[InputRequired(), length(min=6, max=100)])
    password2 = PasswordField("Nové heslo znovu", validators=[InputRequired(), length(min=6, max=100)])
