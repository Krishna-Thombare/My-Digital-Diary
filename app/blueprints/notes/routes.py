from flask import Blueprint, current_app, render_template, redirect, url_for, request, flash
from . import notes_bp
from datetime import date, datetime
from app.forms.notes_form import NoteForm, DeleteForm
from app.models import UserNotes, db
from flask import jsonify
from flask_login import login_required, current_user
from app.utils.cloudinary_images import destroy_image, upload_image

# Note Entries Listing
@notes_bp.route("/")
@login_required
def notes_list():
    notes = UserNotes.query.filter_by(username=current_user.username).order_by(UserNotes.date.desc()).all()
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
        image_file = request.files.get("image")
        image_filename = None

        if image_file and image_file.filename and request.form.get("cancel_image_upload") != "1":
            try:
                image_filename = upload_image(
                    image_file,
                    folder="my_digital_diary/notes",
                    public_id=f"user_{current_user.id}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
                )
            except (ValueError, RuntimeError) as exc:
                flash(str(exc), "error")
                return render_template("notes/notes_add.html", form=form, current_date=date_str)
            except Exception as exc:
                flash("Image upload failed. Please try again.", "error")
                current_app.logger.error("Cloudinary note upload failed: %s", exc)
                return render_template("notes/notes_add.html", form=form, current_date=date_str)
            
        # For adding new note
        new_note = UserNotes(
            user_id=current_user.id,
            username=current_user.username,
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
    entry = UserNotes.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    return render_template("notes/notes_read.html", entry=entry)

# Edit/Update Note Entry
@notes_bp.route("/view/<int:note_id>/edit", methods=["GET", "POST"])
@login_required
def edit_note(note_id):
    entry = UserNotes.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    form = NoteForm(obj=entry)

    if form.validate_on_submit():
        image_file = request.files.get("image")
        has_new_image = image_file and image_file.filename and request.form.get("cancel_image_upload") != "1"

        if has_new_image:
            try:
                new_image_url = upload_image(
                    image_file,
                    folder="my_digital_diary/notes",
                    public_id=f"user_{current_user.id}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
                )
            except (ValueError, RuntimeError) as exc:
                flash(str(exc), "error")
                return render_template("notes/notes_edit.html", form=form, note_id=note_id, entry=entry)
            except Exception as exc:
                flash("Image upload failed. Please try again.", "error")
                current_app.logger.error("Cloudinary note upload failed: %s", exc)
                return render_template("notes/notes_edit.html", form=form, note_id=note_id, entry=entry)

            if entry.image_filename:
                destroy_image(entry.image_filename)
            entry.image_filename = new_image_url
        elif request.form.get("remove_image") == "on" and entry.image_filename:
            destroy_image(entry.image_filename)
            entry.image_filename = None

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
    entry = UserNotes.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()

    if entry.image_filename:
        destroy_image(entry.image_filename)

    db.session.delete(entry)
    db.session.commit()
    flash("Note entry deleted.", "info")
    return redirect(url_for("notes.notes_list"))

# Summarize Notes - *(AI Summarization Feature)*
@notes_bp.route("/get-notes-content/<int:note_id>")
@login_required
def get_notes_content(note_id):
    entry = UserNotes.query.get_or_404(note_id)
    return jsonify({"notes": entry.notes})  

