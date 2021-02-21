from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, DateField, BooleanField, \
    SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, \
    Email, EqualTo, Length

class AddVitalsForm(FlaskForm):
    
    birthday = DateField(label=('Birthday (YYYY-MM-DD)'),
                             validators=[DataRequired()])
    sex = SelectField(label=('Sex'), choices=['Male', 'Female'],
                             validators=[DataRequired()])
    height = IntegerField(label=('Height (inches)'),
                             validators=[DataRequired()])
    weight = IntegerField(label=('Weight (lbs)'),
                             validators=[DataRequired()])
    zipcode = IntegerField(label=('ZIP Code'),
                             validators=[DataRequired()])

    goal1 = StringField(label=('Goal 1'),
                       validators=[DataRequired(),
                                   Length(max=128)])
    goal2 = StringField(label=('Goal 2'),
                       validators=[Length(max=128)])                               
    goal3 = StringField(label=('Goal 3'),
                       validators=[Length(max=128)])

    date = DateField(label=('Date'),
                     validators=[DataRequired()])

    submit = SubmitField(label=('Submit'))