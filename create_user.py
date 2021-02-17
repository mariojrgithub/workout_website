from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, \
    SubmitField
from wtforms.validators import ValidationError, DataRequired, \
    Email, EqualTo, Length

class CreateUserForm(FlaskForm):
    name = StringField(label=('Name'),
        validators=[DataRequired(), 
        Length(max=120)])
   
    password = PasswordField(label=('Password'), 
        validators=[DataRequired(), 
        Length(max=120)])


    submit = SubmitField(label=('Submit'))