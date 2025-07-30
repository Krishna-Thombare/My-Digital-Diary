from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from . import notes_bp
from datetime import date, datetime
from app.forms.notes_form import NoteForm, DeleteForm
from app.models import UserNotes, db
from flask import jsonify
from app.utils.decorators import login_required
import os
from werkzeug.utils import secure_filename
from flask import current_app

# Note Entries Listing
@notes_bp.route("/")
@login_required
def notes_list():
    username = session.get("username")
    notes = UserNotes.query.filter_by(username=username).order_by(UserNotes.date.desc()).all()
    delete_form = DeleteForm()
    return render_template("notes/notes_list.html", notes=notes, delete_form=delete_form)

# Add New Note
@notes_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_note():
    form = NoteForm()
    today = datetime.now()
    date_str = f"{today.day} {today.strftime('%B, %Y')}"
    
    if form.validate_on_submit():
        # For adding image functionality
        image_file = request.files.get('image')
        image_filename = None
        
        # Get remove flag
        remove_image_flag = request.form.get("remove_image") == "1"

        # Handle image only if it's not marked for removal
        if image_file and image_file.filename != "" and not remove_image_flag:
            filename = secure_filename(image_file.filename)
            name, ext = os.path.splitext(filename)   # Spliting name and extension of original filename
            filename_short = name[:25] + ext   # Limits the original filename length to 25 characters

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            user_id = session["user_id"]
            image_filename = f"user_{user_id}_{timestamp}_{filename_short}"

            image_path = os.path.join(current_app.root_path, 'static/uploads', image_filename)
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            image_file.save(image_path)
            
        # For adding new note
        new_note = UserNotes(
            user_id=session["user_id"],
            username=session["username"],
            note_name=form.note_name.data,
            notes=form.notes.data,
            source_links=form.source_links.data,
            date=date.today(),
            image_filename=image_filename
        )
        db.session.add(new_note)
        db.session.commit()
        flash("Note added successfully!", "success")
        return redirect(url_for("notes.notes_list"))
    return render_template("notes/notes_add.html", form=form, current_date=date_str)

# View Note Entry
@notes_bp.route("/view/<int:note_id>")
@login_required
def view_note(note_id):
    entry = UserNotes.query.get_or_404(note_id)
    return render_template("notes/notes_read.html", entry=entry)

# Edit/Update Note Entry
@notes_bp.route("/view/<int:note_id>/edit", methods=["GET", "POST"])
@login_required
def edit_note(note_id):
    entry = UserNotes.query.get_or_404(note_id)
    form = NoteForm(obj=entry)

    if form.validate_on_submit():
        remove_image_checked = 'remove_image' in request.form
        
        # Handle image removal
        if remove_image_checked and entry.image_filename:
            image_path = os.path.join(current_app.root_path, 'static/uploads', entry.image_filename)
            if os.path.exists(image_path):
                os.remove(image_path)
            entry.image_filename = None

        # Handle new image upload (replaces existing one if any)
        image_file = request.files.get('image')
        if image_file and image_file.filename and not remove_image_checked:
            filename = secure_filename(image_file.filename)
            name, ext = os.path.splitext(filename)
            filename_short = name[:25] + ext

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            user_id = session["user_id"]
            image_filename = f"user_{user_id}_{timestamp}_{filename_short}"

            image_path = os.path.join(current_app.root_path, 'static/uploads', image_filename)
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            image_file.save(image_path)

            # Remove old image if replacing
            if entry.image_filename:
                old_path = os.path.join(current_app.root_path, 'static/uploads', entry.image_filename)
                if os.path.exists(old_path):
                    os.remove(old_path)

            entry.image_filename = image_filename

        # Update note fields
        entry.note_name = form.note_name.data
        entry.notes = form.notes.data
        entry.source_links = form.source_links.data
        
        db.session.commit()
        flash("Note entry updated!", "success")
        return redirect(url_for("notes.view_note", note_id=note_id))

    return render_template("notes/notes_edit.html", form=form, note_id=note_id, entry=entry)

# Delete Note Entry
@notes_bp.route("/delete/<int:note_id>", methods=["POST"])
@login_required
def delete_note(note_id):
    entry = UserNotes.query.get_or_404(note_id)

    # Delete image file if exists
    if entry.image_filename:
        image_path = os.path.join(current_app.root_path, 'static/uploads', entry.image_filename)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(entry)
    db.session.commit()
    flash("Note entry deleted.", "info")
    return redirect(url_for("notes.notes_list"))

# Summarize Notes - *(AI Summarization Feature)*
@notes_bp.route("/get-notes-content/<int:note_id>")
def get_notes_content(note_id):
    entry = UserNotes.query.get_or_404(note_id)
    return jsonify({"notes": entry.notes})  

