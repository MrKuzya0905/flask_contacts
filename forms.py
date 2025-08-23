from flask_wtf import FlaskForm
import wtforms

class SignUpForm(FlaskForm):
    username = wtforms.StringField(
        label='username', 
        validators=[wtforms.validators.length(min=3)]
        )
    password = wtforms.PasswordField(
        label='password', 
        validators=[wtforms.validators.length(min=6)]
        )
    full_name = wtforms.StringField(label='your full name (optional)')
    phone_number = wtforms.StringField(label='your phone number (optional)')
    submit = wtforms.SubmitField(label='Sign Up')

class SignInForm(FlaskForm):
    username = wtforms.StringField(
        label='username', 
        validators=[wtforms.validators.length(min=3)]
        )
    
    password = wtforms.PasswordField(
        label='password', 
        validators=[wtforms.validators.length(min=6)]
        )
    submit = wtforms.SubmitField(label='Sign In')
    
class ContactForm(FlaskForm):
    first_name = wtforms.StringField(label='First Name', validators=[wtforms.validators.DataRequired()])
    last_name = wtforms.StringField(label='Last Name', validators=[wtforms.validators.DataRequired()])
    phobe_number = wtforms.StringField(label='Phone Number', validators=[wtforms.validators.DataRequired()])
    city = wtforms.StringField(label='City (optional)')
    bio = wtforms.TextAreaField(label='Bio (optional)')
    file = wtforms.FileField(label='Profile Picture (optional)')
    submit = wtforms.SubmitField(label='Add Contact')