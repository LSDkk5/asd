
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField,
                     SubmitField)
from wtforms.validators import Length, DataRequired, EqualTo, Email, ValidationError

from web.models import User

required = 'To pole jest wymagane!'


class RegistrationForm(FlaskForm):
    username = StringField('Nazwa użytkownika', [
        Length(min=3, max=50),
        DataRequired(message=required)])

    password = PasswordField('hasło', [
        Length(min=8),
        DataRequired(message=required),
        EqualTo('confirmPassword', message='Hasła muszą być takie same')])

    confirmPassword = PasswordField('Powtórz hasło', [
        Length(min=3),
        DataRequired(message=required)])

    email = StringField('Adres email', [
        Email('Podaj prawidłowy adres email'),
        DataRequired(message=required)])

    submit = SubmitField('Zarejestruj się')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'Użytkownik o podanej nazwie jest już zarejestrowany!')

    def validate_email(self, email):
        mail = User.query.filter_by(email=email.data).first()
        if mail:
            raise ValidationError(
                message='Podany adres jest już w naszej bazie!')


class LoginForm(FlaskForm):
    username = StringField('Nazwa użytkownika', [
        Length(min=3, max=50),
        DataRequired(message=required)])

    password = PasswordField('hasło', [
        Length(min=8),
        DataRequired(message=required)])

    rememberMe = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj się')


class ResetPasswordForm(FlaskForm):
    email = StringField('Adres email', [
        Email('Podaj prawidłowy adres email'),
        DataRequired(message=required)])

    submit = SubmitField('Zresetuj hasło')


class ResetPasswordChangeForm(FlaskForm):
    password = PasswordField('Hasło', [
        Length(min=8),
        DataRequired(message=required),
        EqualTo('repeatPassword', message='Hasła muszą być takie same!')])

    repeatPassword = PasswordField('Powtórz hasło', [
        Length(min=8),
        DataRequired(message=required)])

    submit = SubmitField('Zmień hasło')
