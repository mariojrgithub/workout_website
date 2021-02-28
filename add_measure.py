from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, DateField, BooleanField, \
    SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, \
    Email, EqualTo, Length

class AddMeasureForm(FlaskForm):
                             
    weight = StringField(label=('Weight (lbs)'))

    bodyfat = StringField(label=('Body Fat %'))

    resting_heart_rate = StringField(label=('Resting Heart Rate'))

    goal1 = StringField(label=('Goal 1'),
                       validators=[Length(max=128)])
    goal2 = StringField(label=('Goal 2'),
                       validators=[Length(max=128)])                               
    goal3 = StringField(label=('Goal 3'),
                       validators=[Length(max=128)])

    date = DateField(label=('Today\'s Date'),
                     validators=[DataRequired()])

    submit = SubmitField(label=('Submit'))