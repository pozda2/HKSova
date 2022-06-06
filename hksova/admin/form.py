from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import BooleanField
from wtforms import SelectField
from wtforms.validators import InputRequired
from wtforms.validators import DataRequired
from flask_mdeditor import  MDEditorField

class PageForm (FlaskForm):
    title = StringField("Nadpis", validators=[InputRequired()])
    url = StringField("URL", validators=[InputRequired()])
    content = MDEditorField('Článek', validators=[DataRequired()])
    isvisible = BooleanField ("Zveřejněno", false_values=(False, 'false', 0, '0'))
    access_rights = SelectField(u'Přístupová práva', choices=[(0, 'Kdokoliv'), ('1', 'Náhradníci a hrající'), ('2', 'Hrající'), ('3', 'Zaplatili')])
