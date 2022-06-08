from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import IntegerField
from wtforms import BooleanField
from wtforms import SelectField
from wtforms.validators import InputRequired
from wtforms.validators import DataRequired
from wtforms.validators import length
from wtforms.validators import InputRequired
from wtforms.validators import NumberRange
from flask_mdeditor import  MDEditorField

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
