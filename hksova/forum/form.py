from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, TextAreaField
from wtforms.validators import InputRequired


class PostForm (FlaskForm):
    user = StringField("Jméno", validators=[InputRequired()])
    post = TextAreaField("Příspěvek", validators=[InputRequired()])
    source_url = HiddenField("source_url")
