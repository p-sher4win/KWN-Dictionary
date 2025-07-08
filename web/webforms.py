from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# SEARCH WORD FORM
class SearchWordForm(FlaskForm):
    search_for = StringField("Searched", validators=[DataRequired()])
    search = SubmitField("Go")