from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, \
    SubmitField
from wtforms.validators import ValidationError, DataRequired, \
    Email, Length


class CreateUserForm(FlaskForm):
    name = StringField(label=('Name'),
                       validators=[DataRequired(),
                                   Length(max=120)])
                                
    email = StringField(label=('Email'),
                             validators=[DataRequired(), Email(),
                                         Length(max=120)])
  

    password = PasswordField(label=('Password'),
                             validators=[DataRequired(),
                                         Length(max=120)])
                    
    valpassword = PasswordField(label=('Confirm Password'),
                             validators=[DataRequired(),
                                         Length(max=120)])

    submit = SubmitField(label=('Submit'))
