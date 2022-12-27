from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField 
from wtforms.validators import InputRequired, Length

# user name 6- 64
# password - 6 - 64


# Login Form
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=6,max=64) ])
    password = PasswordField(validators=[InputRequired(), Length(min=6,max=64)])
    submit = SubmitField("Login")


# Register Form
class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=6,max=64)])
    password = PasswordField(validators=[InputRequired(),Length(min=6,max=64)])
    password_re = PasswordField(validators=[InputRequired(),Length(min=6,max=64)])
    
    submit = SubmitField("Register")
