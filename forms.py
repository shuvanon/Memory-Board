from flask_wtf import Form
from wtforms import StringField,PasswordField,TextAreaField
from wtforms.validators import (DataRequired,regexp,ValidationError,EqualTo, Email,Length)
from werkzeug import secure_filename
from flask_uploads import UploadSet,configure_uploads, IMAGES
from flask_wtf.file import FileField, FileAllowed, FileRequired

from models import User

#images = UploadSet('images', IMAGES)
#configure_uploads(app, images)

def name_exists(form, field):
    if User.select().where(User.username ==field.data).exists():
        raise ValidationError('User with that name already exists.')

def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')


class RegisterForm(Form):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should be one word, letters, numbers and underscores only.")
            ),
            name_exists
        ])
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ])
    password =PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6),
            EqualTo('password2', message='Passwords must match')
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired()
        ])



class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    
class PostForm(Form):
    content = TextAreaField("What's Up?", validators=[DataRequired()])
    photo = FileField('image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'bmp'], 'Images only!')
    ])

    