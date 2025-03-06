from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user
from notekeeper.models.User import User
from notekeeper.database.config import Base, engine
from notekeeper.auth.auth import auth_bp
from notekeeper.note.note import note_bp
import os
from dotenv import load_dotenv

load_dotenv() 

app = Flask(__name__, template_folder="templates")

app.register_blueprint(auth_bp)
app.register_blueprint(note_bp)


app.config["SECRET_KEY"] = str(os.getenv("SECRET_KEY"))
Base.metadata.create_all(bind=engine)

@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return render_template("index.html")

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)