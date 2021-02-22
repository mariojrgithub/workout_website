from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, DateField, BooleanField, \
    SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, \
    Email, EqualTo, Length

class AddVitalsForm(FlaskForm):
    
    sex = SelectField(label=('Sex'), choices=['Male', 'Female'],
                             validators=[DataRequired()])

    height = SelectField(label=('Height'), 
                        choices=[(54, "4'6\""),(55, "4'7\""),(56, "4'8\""),(57, "4'9\""),(58, "4'10\""),(59, "4'11\""),
                                (60, "5'0\""),(61, "5'1\""),(62, "5'2\""),(63, "5'3\""),(64, "5'4\""),(65, "5'5\""),(66, "5'6\""),
                                (67, "5'7\""),(68, "5'8\""),(69, "5'9\""),(70, "5'10\""),(71, "5'11\""),(72, "6'0\""),
                                (73, "6'1\""),(74, "6'2\""),(75, "6'3\""),(76, "6'4\""),(77, "6'5\""),(78, "6'6\"")],
                             validators=[DataRequired()])
                             
    weight = SelectField(label=('Weight (lbs)'), choices=[x for x in range(100, 251)],
                             validators=[DataRequired()])

    birthday = DateField(label=('Birthday'),
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

    date = DateField(label=('Today\'s Date'),
                     validators=[DataRequired()])

    submit = SubmitField(label=('Submit'))