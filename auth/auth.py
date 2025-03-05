from flask import Blueprint, request, render_template, redirect, url_for
from notekeeper.models.User import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField
from wtforms.validators import DataRequired, EqualTo

auth_bp = Blueprint('auth', __name__, template_folder='templates', url_prefix='/auth')

class RegisterForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    email = EmailField('E-mail', validators=[DataRequired()])
    passwd = PasswordField('Senha', validators=[DataRequired(), EqualTo('confirm_passwd', message='As senhas devem ser iguais.')])
    confirm_passwd = PasswordField('Confirme a senha', validators=[DataRequired()])

class LoginForm(FlaskForm):
    email = EmailField('E-mail', validators=[DataRequired()])
    passwd = PasswordField('Senha', validators=[DataRequired()])

@auth_bp.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        passwd = form.passwd.data

        passwd = generate_password_hash(passwd)

        user = User.get_by_email(email)

        if not user:
            user = User(name=name, email=email, passwd=passwd)
            user.save()
            return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        passwd = form.passwd.data

        user = User.get_by_email(email)

        if user and check_password_hash(user.passwd, passwd):
            if user:
                login_user(user)
            return redirect(url_for('note.list_notes'))

    return render_template('login.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("auth.login"))