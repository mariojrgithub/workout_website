from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, DateField, BooleanField, \
    SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, \
    Email, EqualTo, Length


class AddCardioForm(FlaskForm):
   
    name = SelectField(label=('Name'), choices=['Walk', 'Run', 'Hike', 'Bike', 'Spin', 'Swim', 'Rowing', 'Stairs'],
                       validators=[DataRequired(),
                                   Length(max=64)])
    duration = IntegerField(label=('Duration (seconds)'),
                           validators=[DataRequired()])
    intensity = SelectField(label=('Intensity'), choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                             validators=[DataRequired()])
    date = DateField(label=('Date (YYYY-MM-DD)'),
                     validators=[DataRequired()])

    submit = SubmitField(label=('Submit'))

class AddResistanceForm(FlaskForm):
    name = SelectField(label=('Name'), 
                       choices=['Press', 'Pushup', 'Tricep Ext', 'Pull/Row', 'Pullup', 
                                'Pulldown', 'Bicep Curl', 'Squat', 'Stepup', 'Lunge', 'Bridge', 
                                'Hamstring Curl', 'Plank', 'Crunches', 'Side Plank', 'Ab Rotation'],
                       validators=[DataRequired(),
                                   Length(max=64)])
    weight = IntegerField(label=('Weight (lbs)'),
                             validators=[DataRequired()])
    sets = SelectField(label=('Sets'), choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                             validators=[DataRequired()])
    repetitions = IntegerField(label=('Repetitions'),
                             validators=[DataRequired()])
    rest = IntegerField(label=('Rest (seconds)'),
                             validators=[DataRequired()])
    date = DateField(label=('Date (YYYY-MM-DD)'),
                     validators=[DataRequired()])

    submit = SubmitField(label=('Submit'))
