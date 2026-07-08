from pathlib import PurePosixPath
from urllib.parse import urlparse

import cloudinary.uploader
from flask import current_app
from werkzeug.utils import secure_filename


ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def is_allowed_image(filename):
    safe_name = secure_filename(filename or "")
    return "." in safe_name and safe_name.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


def require_cloudinary_config():
    missing = [
        key
        for key in ("CLOUDINARY_CLOUD_NAME", "CLOUDINARY_API_KEY", "CLOUDINARY_API_SECRET")
        if not current_app.config.get(key)
    ]
    if missing:
        raise RuntimeError(f"Missing Cloudinary config: {', '.join(missing)}")


def upload_image(file_storage, folder, public_id):
    if not file_storage or not file_storage.filename:
        return None

    if not is_allowed_image(file_storage.filename):
        raise ValueError("Unsupported image type. Please upload PNG, JPG, GIF, or WEBP.")

    require_cloudinary_config()
    upload_result = cloudinary.uploader.upload(
        file_storage,
        folder=folder,
        public_id=public_id,
        overwrite=True,
        resource_type="image",
    )
    return upload_result.get("secure_url")


def public_id_from_url(image_url):
    if not image_url:
        return None

    path_parts = PurePosixPath(urlparse(image_url).path).parts
    try:
        upload_index = path_parts.index("upload")
    except ValueError:
        return None

    public_parts = list(path_parts[upload_index + 1 :])
    if public_parts and public_parts[0].startswith("v") and public_parts[0][1:].isdigit():
        public_parts = public_parts[1:]

    if not public_parts:
        return None

    public_id = "/".join(public_parts)
    if "." in public_id:
        public_id = public_id.rsplit(".", 1)[0]
    return public_id


def destroy_image(image_url):
    public_id = public_id_from_url(image_url)
    if not public_id:
        return

    try:
        cloudinary.uploader.destroy(public_id, resource_type="image")
    except Exception as exc:
        current_app.logger.error("Error deleting Cloudinary image %s: %s", public_id, exc)
