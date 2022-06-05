from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms import TextAreaField
from wtforms.validators import InputRequired

class PostForm (FlaskForm):
    user = StringField("Jméno", validators=[InputRequired()])
    post = TextAreaField("Příspěvek", validators=[InputRequired()])
