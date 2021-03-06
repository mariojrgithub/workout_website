from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, DateField, BooleanField, \
    SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, \
    Email, EqualTo, Length


class AddCardioForm(FlaskForm):
   
    name = SelectField(label=('Name'), choices=['Walk', 'Run', 'Hike', 'Bike', 'Spin', 'Swim', 'Rowing', 'Stairs'],
                       validators=[DataRequired(),
                                   Length(max=64)])
    duration = SelectField(label=('Duration (minutes)'), choices=[x for x in range(1, 121)],
                           validators=[DataRequired()])
    intensity = SelectField(label=('Intensity'), choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                             validators=[DataRequired()])
    date = DateField(label=('Date'),
                     validators=[DataRequired()])

    submit = SubmitField(label=('Submit'))

class AddResistanceForm(FlaskForm):
    name = SelectField(label=('Name'), 
                       choices=['Press', 'Pushup', 'Tricep Ext', 'Pull/Row', 'Pullup', 
                                'Pulldown', 'Bicep Curl', 'Squat', 'Stepup', 'Lunge', 'Bridge', 
                                'Hamstring Curl', 'Plank', 'Crunches', 'Side Plank', 'Ab Rotation'],
                       validators=[DataRequired(),
                                   Length(max=64)])
    weight = StringField(label=('Weight (lbs)'))

    sets = SelectField(label=('Sets'), choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                             validators=[DataRequired()])
    repetitions = SelectField(label=('Repetitions'), choices=[x for x in range(1, 51)],
                             validators=[DataRequired()])
    rest = SelectField(label=('Rest (seconds)'), choices=[x for x in range(30, 181)],
                             validators=[DataRequired()])
    date = DateField(label=('Date'),
                     validators=[DataRequired()])

    submit = SubmitField(label=('Submit'))
