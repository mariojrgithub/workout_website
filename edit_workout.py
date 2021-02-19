from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, DateField, BooleanField, \
    SubmitField
from wtforms.validators import ValidationError, DataRequired, \
    Email, EqualTo, Length


class EditCardioForm(FlaskForm):
    
    name = StringField(label=('Name'),
                       validators=[DataRequired(),
                                   Length(max=64)])
    duration = IntegerField(label=('Duration (seconds)'),
                           validators=[DataRequired()])
    intensity = IntegerField(label=('Intensity'),
                             validators=[DataRequired()])
    date = DateField(label=('Date (YYYY-MM-DD)'),
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
    date = DateField(label=('Date (YYYY-MM-DD)'),
                     validators=[DataRequired()])

    submit = SubmitField(label=('Submit'))