from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, DateField, BooleanField, \
    SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, \
    Email, EqualTo, Length

class AddVitalsForm(FlaskForm):
    name = StringField(label=('Name'),
                       validators=[DataRequired(),
                                   Length(max=64)])
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

    goal1 = StringField(label=('Name'),
                       validators=[DataRequired(),
                                   Length(max=128)])
    goal2 = StringField(label=('Name'),
                       validators=[DataRequired(),
                                   Length(max=128)])                               
    goal3 = StringField(label=('Name'),
                       validators=[DataRequired(),
                                   Length(max=128)])

    date = DateField(label=('Date (YYYY-MM-DD)'),
                     validators=[DataRequired()])

    submit = SubmitField(label=('Submit'))