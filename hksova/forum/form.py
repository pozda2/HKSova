from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import HiddenField
from wtforms import TextAreaField
from wtforms.validators import InputRequired

class PostForm (FlaskForm):
    user = StringField("Jméno", validators=[InputRequired()])
    post = TextAreaField("Příspěvek", validators=[InputRequired()])
    source_url = HiddenField("source_url")
