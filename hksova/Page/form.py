from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms.validators import InputRequired
from wtforms.validators import DataRequired
from flask_mdeditor import  MDEditorField

class LoginForm (FlaskForm):
	username = StringField("Uživatelské jméno", validators=[InputRequired()])
	password = PasswordField("Heslo", validators=[InputRequired()])
	content = MDEditorField('Body', validators=[DataRequired()])
	submit = SubmitField()