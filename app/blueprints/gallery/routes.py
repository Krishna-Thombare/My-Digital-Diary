from flask import render_template, redirect, url_for, request, flash, session, current_app, abort
from . import gallery_bp
from app.models import ImageFolder, UserImages, db
from app.utils.decorators import login_required
from app.forms.gallery_form import FolderForm, DeleteForm, UploadImageForm
from werkzeug.utils import secure_filename
from datetime import datetime, date
from sqlalchemy.exc import IntegrityError
import os

ALLOWED_EXT = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

# Folder List
@gallery_bp.route("/", methods=["GET", "POST"])
@login_required
def gallery_list():
    form = FolderForm()
    delete_form = DeleteForm()

    if form.validate_on_submit():
        name = form.name.data.strip()
        if not name:
            flash("Folder name required.", "error")
            return redirect(url_for("gallery.gallery_list"))

        new_folder = ImageFolder(name=name, user_id=session["user_id"], created_at=date.today())
        db.session.add(new_folder)
        try:
            db.session.commit()
            flash("Folder created.", "success")
        except IntegrityError:
            db.session.rollback()
            flash("Folder name already exists!", "error")
        return redirect(url_for("gallery.gallery_list"))

    folders = ImageFolder.query.filter_by(user_id=session["user_id"]).order_by(ImageFolder.created_at.desc()).all()
    return render_template("gallery/gallery_list.html", folders=folders, form=form, delete_form=delete_form)

# View Folder
@gallery_bp.route("/folder/<int:folder_id>", methods=["GET", "POST"])
@login_required
def gallery_view(folder_id):
    folder = ImageFolder.query.get_or_404(folder_id)
    if folder.user_id != session["user_id"]:
        abort(403)

    form = UploadImageForm()
    delete_form = DeleteForm()

    if request.method == "POST" and form.validate_on_submit():
        files = request.files.getlist("image")
        if not files or files[0].filename.strip() == "":
            flash("No file selected!", "error")
            return redirect(url_for("gallery.gallery_view", folder_id=folder_id))

        upload_count = 0
        for image_file in files:
            filename = secure_filename(image_file.filename)
            if not filename or not allowed_file(filename):
                continue  # Skip invalid files

            name, ext = os.path.splitext(filename)
            short = name[:30] + ext
            ts = datetime.now().strftime("%Y%m%d%H%M%S")
            user_id = session["user_id"]
            out_filename = f"user_{user_id}_{ts}_{short}"

            upload_dir = os.path.join(current_app.root_path, "static", "uploads", "gallery")
            os.makedirs(upload_dir, exist_ok=True)
            save_path = os.path.join(upload_dir, out_filename)
            image_file.save(save_path)

            ui = UserImages(filename=out_filename, folder_id=folder_id, uploaded_at=date.today())
            db.session.add(ui)
            upload_count += 1

        db.session.commit()

        if upload_count > 0:
            flash(f"{upload_count} image(s) uploaded!", "success")
        else:
            flash("No valid images uploaded.", "error")

        return redirect(url_for("gallery.gallery_view", folder_id=folder_id))

    images = UserImages.query.filter_by(folder_id=folder_id).order_by(UserImages.uploaded_at.desc()).all()
    return render_template("gallery/gallery_view.html", folder=folder, images=images, form=form, delete_form=delete_form)

# Delete Folder
@gallery_bp.route("/delete_folder/<int:folder_id>", methods=["POST"])
@login_required
def delete_folder(folder_id):
    folder = ImageFolder.query.get_or_404(folder_id)
    if folder.user_id != session["user_id"]:
        abort(403)

    # Path to the uploads folder
    upload_dir = os.path.join(current_app.root_path, "static", "uploads", "gallery")

    # Get all images in this folder
    images = UserImages.query.filter_by(folder_id=folder_id).all()

    # Delete image files from disk
    for img in images:
        file_path = os.path.join(upload_dir, img.filename)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                current_app.logger.error(f"Error deleting file {file_path}: {e}")

    # Delete image records from Database
    UserImages.query.filter_by(folder_id=folder_id).delete()

    # Delete folder record from Database
    db.session.delete(folder)
    db.session.commit()

    flash("Folder and its images deleted!", "success")
    return redirect(url_for("gallery.gallery_list"))

# Delete Image
@gallery_bp.route("/image/<int:image_id>/delete", methods=["POST"])
@login_required
def delete_image(image_id):
    form = DeleteForm()
    if not form.validate_on_submit():
        flash("Invalid request!", "error")
        return redirect(url_for("gallery.gallery_list"))

    img = UserImages.query.get_or_404(image_id)
    folder = ImageFolder.query.get_or_404(img.folder_id)
    if folder.user_id != session["user_id"]:
        abort(403)

    upload_dir = os.path.join(current_app.root_path, "static", "uploads", "gallery")
    path = os.path.join(upload_dir, img.filename)
    if os.path.exists(path):
        os.remove(path)

    folder_id = img.folder_id
    db.session.delete(img)
    db.session.commit()
    flash("Image deleted!", "success")
    return redirect(url_for("gallery.gallery_view", folder_id=folder_id))
