from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from . import notes_bp
from datetime import date, datetime
from app.forms.notes_form import NoteForm, DeleteForm
from app.models import UserNotes, db
from flask import jsonify
from app.utils.decorators import login_required

@notes_bp.route("/")
@login_required
def notes_list():
    username = session.get("username")
    notes = UserNotes.query.filter_by(username=username).order_by(UserNotes.date.desc()).all()
    delete_form = DeleteForm()
    return render_template("notes/notes_list.html", notes=notes, delete_form=delete_form)

@notes_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_note():
    form = NoteForm()
    today = datetime.now()
    date_str = f"{today.day} {today.strftime('%B, %Y')}"
    if form.validate_on_submit():
        new_note = UserNotes(
            user_id=session["user_id"],
            username=session["username"],
            note_name=form.note_name.data,
            notes=form.notes.data,
            source_links=form.source_links.data,
            date=date.today()
        )
        db.session.add(new_note)
        db.session.commit()
        flash("Note added successfully!", "success")
        return redirect(url_for("notes.notes_list"))
    return render_template("notes/notes_add.html", form=form, current_date=date_str)

@notes_bp.route("/view/<int:note_id>")
@login_required
def view_note(note_id):
    entry = UserNotes.query.get_or_404(note_id)
    return render_template("notes/notes_read.html", entry=entry)

@notes_bp.route("/view/<int:note_id>/edit", methods=["GET", "POST"])
@login_required
def edit_note(note_id):
    entry = UserNotes.query.get_or_404(note_id)
    form = NoteForm(obj=entry)
    
    if form.validate_on_submit():
        entry.note_name = form.note_name.data
        entry.notes = form.notes.data
        entry.source_links = form.source_links.data
        db.session.commit()
        flash("Note entry updated!", "success")
        return redirect(url_for("notes.view_note", note_id=note_id))
    return render_template("notes/notes_edit.html", form=form, note_id=note_id)

@notes_bp.route("/delete/<int:note_id>", methods=["POST"])
@login_required
def delete_note(note_id):
    entry = UserNotes.query.get_or_404(note_id)
    db.session.delete(entry)
    db.session.commit()
    flash("Note entry deleted.", "info")
    return redirect(url_for("notes.notes_list"))

# Summariza Notes - (AI Summarization Feature)
@notes_bp.route("/get-notes-content/<int:note_id>")
def get_notes_content(note_id):
    entry = UserNotes.query.get_or_404(note_id)
    return jsonify({"notes": entry.notes})  

