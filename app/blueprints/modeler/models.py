from app import db
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField

class SelectEvent(FlaskForm):
    event_id = IntegerField
    event_submit = SubmitField("Run Event")