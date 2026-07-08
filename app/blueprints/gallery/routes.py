from flask import current_app, render_template, redirect, url_for, request, flash, abort
from . import gallery_bp
from app.models import ImageFolder, UserImages, db
from flask_login import login_required, current_user
from app.forms.gallery_form import FolderForm, DeleteForm, UploadImageForm
from datetime import datetime, date
from sqlalchemy.exc import IntegrityError
from app.utils.cloudinary_images import destroy_image, is_allowed_image, upload_image

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

        new_folder = ImageFolder(name=name, user_id=current_user.id, created_at=date.today())
        db.session.add(new_folder)
        try:
            db.session.commit()
            flash("Folder created.", "success")
        except IntegrityError:
            db.session.rollback()
            flash("Folder name already exists!", "error")
        return redirect(url_for("gallery.gallery_list"))

    folders = ImageFolder.query.filter_by(user_id=current_user.id).order_by(ImageFolder.created_at.desc()).all()
    return render_template("gallery/gallery_list.html", folders=folders, form=form, delete_form=delete_form)

# View Folder
@gallery_bp.route("/folder/<int:folder_id>", methods=["GET", "POST"])
@login_required
def gallery_view(folder_id):
    folder = ImageFolder.query.get_or_404(folder_id)
    if folder.user_id != current_user.id:
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
            if not image_file.filename or not is_allowed_image(image_file.filename):
                continue  # Skip invalid files

            ts = datetime.now().strftime("%Y%m%d%H%M%S%f")
            try:
                image_url = upload_image(
                    image_file,
                    folder=f"my_digital_diary/gallery/folder_{folder_id}",
                    public_id=f"user_{current_user.id}_{ts}",
                )
            except (ValueError, RuntimeError) as exc:
                db.session.rollback()
                flash(str(exc), "error")
                return redirect(url_for("gallery.gallery_view", folder_id=folder_id))
            except Exception as exc:
                db.session.rollback()
                current_app.logger.error("Cloudinary gallery upload failed: %s", exc)
                flash("Image upload failed. Please try again.", "error")
                return redirect(url_for("gallery.gallery_view", folder_id=folder_id))

            ui = UserImages(filename=image_url, folder_id=folder_id, uploaded_at=date.today())
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
    if folder.user_id != current_user.id:
        abort(403)

    images = UserImages.query.filter_by(folder_id=folder_id).all()

    for img in images:
        destroy_image(img.filename)

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
    if folder.user_id != current_user.id:
        abort(403)

    destroy_image(img.filename)

    folder_id = img.folder_id
    db.session.delete(img)
    db.session.commit()
    flash("Image deleted!", "success")
    return redirect(url_for("gallery.gallery_view", folder_id=folder_id))
