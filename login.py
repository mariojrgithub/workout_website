from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, \
    SubmitField
from wtforms.validators import ValidationError, DataRequired, \
    Email, EqualTo, Length

class LoginForm(FlaskForm):
    name = StringField(label=('Username'), 
        validators=[DataRequired(), 
        Length(max=64)])
   
    password = PasswordField(label=('Password'), 
        validators=[DataRequired(), 
        Length(max=120)])


    submit = SubmitField(label=('Submit'))