from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


# TEST FORM
class TestFrom(FlaskForm):
    test = StringField("Type")
    submit = SubmitField("Done")