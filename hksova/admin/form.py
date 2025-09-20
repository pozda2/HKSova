import re
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, BooleanField, SelectField, PasswordField, RadioField, FieldList, FormField
from wtforms.validators import length, InputRequired, DataRequired, NumberRange, Email, ValidationError
from flask_mdeditor import MDEditorField


# TODO: what should be returned when field.data is not evaluate as True?
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


def validate_age(form, field, _min=10, _max=100):
    if field.data:
        if field.data.isnumeric():
            age = int(field.data)
            if (age < _min or age > _max):
                raise ValidationError(f"Věk není v rozsahu {_min} až {_max}.")
        else:
            raise ValidationError('Věk není číslo')


class PageForm (FlaskForm):
    title = StringField("Nadpis", validators=[InputRequired(), length(min=1, max=255, message='Délka názvu stránky musí být v rozsahu 1-255) znaků')])
    url = StringField("URL", validators=[InputRequired(), length(min=1, max=255, message='Délka URL musí být v rozsahu 1-255) znaků')])
    content = MDEditorField('Článek', validators=[DataRequired()])
    forum_section = SelectField('Sekce fóra')
    isvisible = BooleanField("Zveřejněno", false_values=(False, 'false', 0, '0'))
    access_rights = SelectField('Přístupová práva', choices=[(0, 'Kdokoliv'), (1, 'Náhradníci a hrající'), (2, 'Hrající'), (3, 'Zaplatili')], coerce=int)


class PageDeleteForm(FlaskForm):
    agree = BooleanField("Opravdu chcete smazat stránku?", validators=[InputRequired()])


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
    ], coerce=int)
    pages = SelectField('Stránka')
    isnewpart = BooleanField("Samostatná položka mimo dropdown menu", false_values=(False, 'false', 0, '0'))
    isvisible = BooleanField("Zveřejněno", false_values=(False, 'false', 0, '0'))
    access_rights = SelectField('Přístupová práva', choices=[(0, 'Kdokoliv'), (1, 'Náhradníci a hrající'), (2, 'Hrající'), (3, 'Zaplatili')], coerce=int)
    current_year = BooleanField("Zobrazit pouze v aktuálním ročníku", false_values=(False, 'false', 0, '0'))


class MenuItemDeleteForm(FlaskForm):
    agree = BooleanField("Opravdu chcete smazat položku v menu?", validators=[InputRequired()])


class ForumSectionForm(FlaskForm):
    order = IntegerField("Pořadí", validators=[InputRequired(), InputRequired(), NumberRange(0, 1000, "Pořadí položky musí být v rozmezí 0-1000")])
    section = StringField("Název sekce", validators=[InputRequired(), length(min=1, max=255, message='Délka názvu položky musí být v rozsahu 1-255) znaků')])
    isvisible = BooleanField("Zveřejněno", false_values=(False, 'false', 0, '0'))


class ForumSectionDeleteForm(FlaskForm):
    agree = BooleanField("Opravdu chcete smazat sekce ve fóru včetně všech příspěvků?", validators=[InputRequired()])


class PasswordChangeForm(FlaskForm):
    password_old = PasswordField("Staré heslo", validators=[InputRequired(), length(min=6, max=100)])
    password1 = PasswordField("Nové heslo", validators=[InputRequired(), length(min=6, max=100)])
    password2 = PasswordField("Nové heslo znovu", validators=[InputRequired(), length(min=6, max=100)])


class PlayerForm(FlaskForm):
    name = StringField("Jméno hráče", validators=[length(max=100, message='Maximální délka jména je 100 znaků')])
    publicname = StringField("Veřejné jméno hráče", validators=[length(max=100, message='Maximální délka jména je 100 znaků')])
    city = StringField("Město", validators=[length(max=100, message='Maximální délka města je 100 znaků')])
    age = StringField("Věk", validators=[validate_age])


class EditTeamForm(FlaskForm):
    name = StringField("Název týmu", validators=[InputRequired(), length(min=1, max=100, message='Délka názvu týmu musí být v rozsahu 1-100) znaků')])
    login = StringField("Přihlašovací jméno", validators=[InputRequired(), length(min=4, max=100, message='Délka přihlašovacího jména musí být v rozsahu 4-100) znaků')])
    email = StringField("Email", validators=[InputRequired(), length(max=255, message='Maximální délka email je 255 znaků'), Email()])
    mobil = StringField("Telefon", validators=[InputRequired(), length(max=30, message='Maximální délka telefonu je 30 znaků')])
    weburl = StringField("Web stránka týmu (URL)", validators=[length(max=255, message='Maximální délka URL je 255 znaků'), validate_url])
    reporturl = StringField("Web stránka s reportáží (URL)", validators=[length(max=255, message='Maximální délka URL je 255 znaků')])
    ispaid = BooleanField("Zaplaceno", false_values=(False, 'false', 0, '0'))
    isbackup = BooleanField("Náhradník", false_values=(False, 'false', 0, '0'))
    isdeleted = BooleanField("Smazáno", false_values=(False, 'false', 0, '0'))
    players = FieldList(FormField(PlayerForm))


class SettingForm(FlaskForm):
    param = StringField("Parametr", validators=[InputRequired(), length(min=1, max=255, message='Název parametru')])
    value = StringField("Hodnota", validators=[InputRequired(), length(min=1, max=255, message='Hodnota parametru')])


class SettingDeleteForm(FlaskForm):
    agree = BooleanField("Opravdu chcete smazat parametr z nastavení?", validators=[InputRequired()])


class GeneratingEmailsForm(FlaskForm):
    filter = RadioField('Filtr', choices=[(0, 'Všechny týmy'), (1, 'Zaplatili'), (2, 'Nezaplatili'), (3, 'Náhradníci')], validators=[InputRequired()])


class MascotForm(FlaskForm):
    mascot = StringField("Maskot", validators=[InputRequired(), length(min=1, max=255, message='Maskot')])


class MascotDeleteForm(FlaskForm):
    agree = BooleanField("Opravdu chcete smazat maskota?", validators=[InputRequired()])


class NextYearForm(FlaskForm):
    agree = BooleanField("Opravdu chcete založit nový ročník?", validators=[InputRequired()])

class PlaceForm(FlaskForm):
    place = StringField("Název", validators=[InputRequired(), length(min=1, max=255, message='Název')])
    latitude = DecimalField("Zeměpisná šířka", validators=[NumberRange(-90, 90, "Zeměpisná šířka musí být v intervalu -90 až 90")])
    longitude = DecimalField("Zeměpisná délka", validators=[NumberRange(-180, 180, "Zeměpisná délka musí být v intervalu -180 až 180")])