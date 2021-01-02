from app import db
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

class ChooseEvent(FlaskForm):
    idno = IntegerField()
    get_event = SubmitField("Get Event Info")