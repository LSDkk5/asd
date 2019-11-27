from flask import (Blueprint, render_template, flash, redirect, url_for)
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta

from web import db, bcrypt
from web.models import User
from web.home.routes import home_page
from utils.send_email import send_email
from utils.token import generate_confirmation_token, confirm_token
from web.auth.forms import LoginForm, RegistrationForm, ResetPasswordForm, ResetPasswordChangeForm


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(
                user.password, form.password.data):
            login_user(user)
            flash('Zostałeś pomyślnie zalogowany!', 'info')
            return redirect(url_for('home.home_page'))
        else:
            flash(
                'Błędny login lub hasło, sprawdz poprawność wprowadzonych danych',
                'danger')
    return render_template('/auth/login.html', form=form)


@auth.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home.home_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        newUser = User(
            username=form.username.data,
            email=form.email.data,
            password=bcrypt.generate_password_hash(
                form.password.data),
            registered_on=datetime.now().strftime('%m-%d-%Y'),
            registered_time=datetime.now().strftime('%H:%M'))
        print(newUser)
        db.session.add(newUser)
        db.session.commit()

        token = generate_confirmation_token(newUser.email)
        send_email(
            newUser.email,
            'Aktywacja Konta',
            render_template(
                'auth/activate.html',
                confirm_url=url_for(
                    'auth.confirm_account',
                    token=token,
                    _external=True)))
        login_user(newUser)
        flash('Twoje konto zostało pomyślnie utworzone! Na podany adres e-mail wyslaliśmy wiadomość z linkiem aktywacyjnym. Prosimy aktywować  swoje konto aby mieć dostęp do pełnej wersji strony', 'success')
        return redirect(url_for('home.home_page'))
    return render_template('/auth/register.html', form=form)


@auth.route('/account/confirm/<token>')
def confirm_account(token):
    try:
        email = confirm_token(token)
    except BaseException:
        flash('Link potwierdzający jest nieprawidłowy lub wygasł!.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Twoje konto zostało już wcześniej potwierdzone!', 'info')
    else:
        user.confirmed = True
        db.session.commit()
        flash('Aktywacja konta przebiegła pomyślnie. Dziękujemy!', 'success')
    return redirect(url_for('home.home_page'))


@auth.route('/password/forget', methods=['POST', 'GET'])
def forget_password():
    if current_user.is_authenticated:
        return redirect(url_for('home.home_page'))
    else:
        form = ResetPasswordForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user.last_change + timedelta(minutes=30) <= datetime.now():
                if user:
                    token = generate_confirmation_token(user.email)
                    send_email(
                        user.email,
                        'Zmiana hasła',
                        render_template(
                            'auth/activate.html',
                            confirm_url=url_for(
                                'auth.reset_password',
                                token=token,
                                _external=True)))
                    flash(
                        'Na podany adres email zostały wysłane dalesze instrukcje dotyczące zmiany hasła!',
                        'success')
                else:
                    flash(
                        'Do podanego adresu email nie zostało przypisane żadne konto!',
                        'danger')
            else:
                flash(
                    'Hasło można zresetować po upływie 30minut od ostatniej zmiany!',
                    'warning')
    return render_template('/auth/forgetPassword.html', form=form)


@auth.route('/reset/password/r<token>', methods=['POST', 'GET'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home.home_page'))
    form = ResetPasswordChangeForm()
    if form.validate_on_submit():
        try:
            email = confirm_token(token)
        except BaseException:
            flash(
                'Link resetujący hasło wygasł, lub jest nieprawidłowy!',
                'danger')
        user = User.query.filter_by(email=email).first_or_404()
        if user.last_change + timedelta(minutes=30) <= datetime.now():
            user.password = bcrypt.generate_password_hash(form.password.data)
            user.last_change = datetime.now()
            db.session.commit()
            flash(
                'Twoje hasło zostało pomyślnie zresetowane!, teraz możesz się zalogować.',
                'success')
            return redirect(url_for('auth.login'))
        else:
            flash(
                'Hasło można zresetować po upływie 30minut od ostatniej zmiany!',
                'warning')
            return redirect(url_for('home.home_page'))
    return render_template('/auth/resetPassword.html', form=form)


@auth.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('Zostałeś pomyślnie wylogowany', 'primary')
    else:
        return redirect(url_for('home.home_page'))
    return redirect(url_for('auth.login'))
