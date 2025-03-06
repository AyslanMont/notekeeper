from flask import Blueprint, redirect, render_template, request, url_for, abort
from flask_login import current_user, login_required
from notekeeper.models.Note import Note
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from notekeeper.database.config import db_session

note_bp = Blueprint('note', __name__, url_prefix='/notes', template_folder='templates')


@note_bp.route('/create_note', methods=["GET", "POST"])
@login_required
def create_note():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']

        new_note = Note(title=title, text=text, user_id=current_user.id)
        new_note.save()
        return redirect(url_for('note.list_notes'))
    return render_template("create_note.html")

@note_bp.route('/list_notes', methods=["GET", "POST"])
@login_required
def list_notes():
    notes = Note.get_by_user(current_user.id)
    return render_template("list_notes.html", notes=notes)

@note_bp.route('/edit_notes/<int:id>', methods=["GET", "POST"])
@login_required
def edit_notes(id):
    note = db_session.query(Note).filter_by(id=id, user_id=current_user.id).first()

    if not note:
        abort(404)

    if request.method == "POST":
        note.title = request.form["title"]
        note.text = request.form["text"]
        db_session.commit()
        return redirect(url_for("note.list_notes"))

    return render_template("edit_notes.html", note=note)

@note_bp.route('/delete_note/<int:id>', methods=["POST"])
@login_required
def delete_note(id):
    note = db_session.query(Note).filter_by(id=id, user_id=current_user.id).first()

    if not note:
        abort(404)

    db_session.delete(note)
    db_session.commit()
    return redirect(url_for("note.list_notes"))