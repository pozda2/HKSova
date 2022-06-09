from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import IntegerField
from wtforms import BooleanField
from wtforms import SelectField
from wtforms import PasswordField
from wtforms import FieldList, FormField
from wtforms.validators import InputRequired
from wtforms.validators import DataRequired
from wtforms.validators import length
from wtforms.validators import InputRequired
from wtforms.validators import NumberRange
from wtforms.validators import Email, ValidationError
from flask_mdeditor import  MDEditorField

def validate_url(form, field):
    if field.data:
        regex = (
            r"^[a-z]+://"
            r"(?P<host>[^\/\?:]+)"
            r"(?P<port>:[0-9]+)?"
            r"(?P<path>\/.*?)?"
            r"(?P<query>\?.*)?$"
        )
        result=re.search(regex, field.data)
        if not result:
            raise ValidationError('URL je neplatné')
        else:
            return result

def validate_age(form, field, min=10, max=100):
    if field.data:
        if field.data.isnumeric():
            age=int(field.data)
            if (age < min or age > max):
                raise ValidationError(f"Věk není v rozsahu {min} až {max}.")
        else:
            raise ValidationError('Věk není číslo')

class PageForm (FlaskForm):
    title = StringField("Nadpis", validators=[InputRequired(), length(min=1, max=255, message='Délka názvu stránky musí být v rozsahu 1-255) znaků')])
    url = StringField("URL", validators=[InputRequired(), length(min=1, max=255, message='Délka URL musí být v rozsahu 1-255) znaků')])
    content = MDEditorField('Článek', validators=[DataRequired()])
    forum_section = SelectField('Sekce fóra')
    isvisible = BooleanField ("Zveřejněno", false_values=(False, 'false', 0, '0'))
    access_rights = SelectField('Přístupová práva', choices=[(0, 'Kdokoliv'), (1, 'Náhradníci a hrající'), (2, 'Hrající'), (3, 'Zaplatili')], coerce=int)

class MenuItemForm (FlaskForm):
    order = IntegerField("Pořadí", validators=[InputRequired(), InputRequired(), NumberRange(0, 1000, "Pořadí položky musí být v rozmezí 0-1000")])
    menu = StringField("Popis položky", validators=[InputRequired(), length(min=1, max=255, message='Délka názvu položky musí být v rozsahu 1-255) znaků')])
    link = StringField('URL odkaz (pro externí stránky)', validators=[length(min=0, max=255, message='Délka URL položky musí být v rozsahu 1-255) znaků')])
    pagetype = SelectField('Typ stránky', choices=[
        ('0', 'Interní stránka'), 
        ('1', 'Externí odkaz'), 
        ('2', 'Skupina v menu'),
        ('3', 'Přihlášení'),
        ('4', 'Odhlášení'),
        ('5', 'Údaje o týmu'),
        ('6', 'Změna hesla'),
        ('7', 'Zrušení registrace'),
        ('8', 'Týmy'),
        ('9', 'Fórum'),
        ('10', 'Registrace'),
    ] , coerce=int)
    pages = SelectField('Stránka')
    isnewpart = BooleanField ("Samostatná položka mimo dropdown menu", false_values=(False, 'false', 0, '0'))
    isvisible = BooleanField ("Zveřejněno", false_values=(False, 'false', 0, '0'))
    access_rights = SelectField('Přístupová práva', choices=[(0, 'Kdokoliv'), (1, 'Náhradníci a hrající'), (2, 'Hrající'), (3, 'Zaplatili')], coerce=int)
    current_year = BooleanField ("Zobrazit pouze v aktuálním ročníku", false_values=(False, 'false', 0, '0'))

class MenuItemDeleteForm(FlaskForm):
    agree = BooleanField ("Opravdu chcete smazat položku v menu?", validators=[InputRequired()] )

class ForumSectionForm (FlaskForm):
    order = IntegerField("Pořadí", validators=[InputRequired(), InputRequired(), NumberRange(0, 1000, "Pořadí položky musí být v rozmezí 0-1000")])
    section = StringField("Název sekce", validators=[InputRequired(), length(min=1, max=255, message='Délka názvu položky musí být v rozsahu 1-255) znaků')])
    isvisible = BooleanField ("Zveřejněno", false_values=(False, 'false', 0, '0'))

class ForumSectionDeleteForm(FlaskForm):
    agree = BooleanField ("Opravdu chcete smazat sekce ve fóru včetně všech příspěvků?", validators=[InputRequired()] )

class PageDeleteForm(FlaskForm):
    agree = BooleanField ("Opravdu chcete smazat stránku?", validators=[InputRequired()] )

class PasswordChangeForm (FlaskForm):
    password_old = PasswordField("Staré heslo", validators=[InputRequired(), length(min=6, max=100)])
    password1 = PasswordField("Nové heslo", validators=[InputRequired(), length(min=6, max=100)])
    password2 = PasswordField("Nové heslo znovu", validators=[InputRequired(), length(min=6, max=100)])

class PlayerForm(FlaskForm):
    name = StringField("Jméno hráče", validators=[length(max=100, message='Maximální délka jména je 100 znaků')])
    publicname = StringField("Veřejné jméno hráče", validators=[length(max=100, message='Maximální délka jména je 100 znaků')])
    city = StringField("Město", validators=[length(max=100, message='Maximální délka města je 100 znaků')])
    age = StringField("Věk", validators=[validate_age])

class EditTeamForm (FlaskForm):
    name = StringField("Název týmu", validators=[InputRequired(), length(min=1, max=100, message='Délka názvu týmu musí být v rozsahu 1-100) znaků')])
    login = StringField("Přihlašovací jméno", validators=[InputRequired(), length(min=4, max=100, message='Délka přihlašovacího jména musí být v rozsahu 4-100) znaků')])
    email = StringField("Email", validators=[InputRequired(), length(max=255, message='Maximální délka email je 255 znaků'), Email()])
    mobil = StringField("Telefon", validators=[InputRequired(), length(max=30, message='Maximální délka telefonu je 30 znaků')])
    weburl = StringField("Web stránka týmu (URL)", validators=[length(max=255, message='Maximální délka URL je 255 znaků'), validate_url])
    reporturl = StringField("Web stránka s reportáží (URL)", validators=[length(max=255, message='Maximální délka URL je 255 znaků')])
    ispaid = BooleanField ("Zaplaceno", false_values=(False, 'false', 0, '0'))
    isbackup = BooleanField ("Náhradník", false_values=(False, 'false', 0, '0'))
    isdeleted = BooleanField ("Smazáno", false_values=(False, 'false', 0, '0'))
    players = FieldList(FormField(PlayerForm))

class SettingForm (FlaskForm):
    param = StringField("Parametr", validators=[InputRequired(), length(min=1, max=255, message='Název parametru')])
    value = StringField("Hodnota", validators=[InputRequired(), length(min=1, max=255, message='Hodnota parametru')])

class SettingDeleteForm(FlaskForm):
    agree = BooleanField ("Opravdu chcete smazat parametr z nastavení?", validators=[InputRequired()] )