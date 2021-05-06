from flask_wtf import FlaskForm
from wtforms.fields import StringField, BooleanField, SubmitField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import AssessmentLog



