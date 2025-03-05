from flask import Blueprint, request, render_template, redirect, url_for
from notekeeper.models.User import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user

auth_bp = Blueprint('auth', __name__, template_folder='templates', url_prefix='/auth')

@auth_bp.route('/register', methods=["GET", "POST"])
def register():

    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        passwd = request.form['passwd']
        
        passwd = generate_password_hash(passwd)

        user = User.get_by_email(email)

        if not user:
            user = User(name=name, email=email, passwd=passwd)
            user.save()
            return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/login', methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form['email']
        passwd = request.form['passwd']

        user = User.get_by_email(email)

        if user and check_password_hash(user.passwd, passwd):
            login_user(user)
            return redirect(url_for('note.list_notes'))

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("auth.login"))