from flask_wtf import FlaskForm
from ..models import Admin
from wtforms import StringField, PasswordField, BooleanField,SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length,Regexp, ValidationError



class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Regexp('^[A-Za-z][A-Za-z0-9._]*$',0,'Username must only have letters, dots or underscores'), Length(min=2, max=16, message='Length should be within 2 to 16 charcters')])
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid email')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message='Password must be at least 8 characters')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password', message='Password must match')])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if Admin.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered")

    def validate_username(self, field):
        if Admin.query.filter_by(username=field.data).first():
            raise ValidationError("Username already in use")

     

class SigninForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid email')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message='Password must be at least 8 characters')])
    remember = BooleanField('Keep me logged in')
    submit = SubmitField('Submit')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired(), Length(min=8)])
    password = PasswordField('New Password', validators=[DataRequired(), EqualTo('password2', message='Password must match'), Length(min=8, message='Password must be at least 8 characters')])
    password2 = PasswordField('Confirm New Password', validators=[DataRequired()])
    submit = SubmitField('Update')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')

class PasswordResetForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=8, message='Password should be at least 8 characters'), EqualTo('password2', message='Password must match!')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ChangeEmailForm(FlaskForm):
    email = StringField('New Email', validators=[DataRequired(), Length(1,64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_email(self, field):
        if Admin.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already exists!')



