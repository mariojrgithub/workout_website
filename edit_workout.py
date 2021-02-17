from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, DateField, BooleanField, \
    SubmitField
from wtforms.validators import ValidationError, DataRequired, \
    Email, EqualTo, Length

class EditWorkoutForm(FlaskForm):
    name = StringField(label=('Name'), 
        validators=[DataRequired(), 
        Length(max=64)])
    duration = StringField(label=('Duration'), 
        validators=[DataRequired(), 
        Length(max=12)])
    intensity = IntegerField(label=('Intensity'), 
        validators=[DataRequired()])
    date = StringField(label=('Date (YYYY-MM-DD)'),
        validators=[DataRequired()])


    submit = SubmitField(label=('Submit'))