
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField,SelectField
from wtforms.validators import DataRequired, Email, EqualTo



class SignupForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    email = EmailField('Your Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Repeat your password',
        validators=[DataRequired(), EqualTo('password', message='Passwords must match')]
    )
    submit = SubmitField('Register')



class LoginForm(FlaskForm):
    email = EmailField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class TaskForm(FlaskForm):
    task = StringField('Enter a task here', validators=[DataRequired()])
    priority = SelectField(
        'Select Priority',
        choices=[('low', 'Low Priority'), ('medium', 'Medium Priority'), ('high', 'High Priority')],
        validators=[DataRequired()]
    )
    save=SubmitField('save')