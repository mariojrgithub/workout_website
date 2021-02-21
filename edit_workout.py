from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, DateField, BooleanField, \
    SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, \
    Email, EqualTo, Length


class EditCardioForm(FlaskForm):
    
    name = StringField(label=('Name'),
                       validators=[DataRequired(),
                                   Length(max=64)])
    duration = IntegerField(label=('Duration (minutes)'),
                           validators=[DataRequired()])
    intensity = IntegerField(label=('Intensity'),
                             validators=[DataRequired()])
    date = StringField(label=('Date'),
                     validators=[DataRequired()])

    submit = SubmitField(label=('Submit'))

class EditResistanceForm(FlaskForm):

    name = StringField(label=('Name'),
                       validators=[DataRequired(),
                                   Length(max=64)])
    weight = IntegerField(label=('Weight (lbs)'),
                             validators=[DataRequired()])
    sets = IntegerField(label=('Sets'),
                             validators=[DataRequired()])
    repetitions = IntegerField(label=('Repetitions'),
                             validators=[DataRequired()])
    rest = IntegerField(label=('Rest (seconds)'),
                             validators=[DataRequired()])
    date = StringField(label=('Date'),
                     validators=[DataRequired()])

    submit = SubmitField(label=('Submit'))