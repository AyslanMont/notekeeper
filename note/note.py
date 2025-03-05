from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from notekeeper.models.Note import Note
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

note_bp = Blueprint('note', __name__, url_prefix='/notes', template_folder='templates')


@note_bp.route('/create_note', methods=["GET", "POST"])
@login_required
def create_note():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']

        new_note = Note(title=title, text=text, user_id=current_user.id)
        new_note.save()
    return render_template("create_note.html")

@note_bp.route('/list_notes', methods=["GET", "POST"])
@login_required
def list_notes():
    notes = Note.get_by_user(current_user.id)
    return render_template("list_notes.html", notes=notes)