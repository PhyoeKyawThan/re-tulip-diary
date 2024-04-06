from flask import Blueprint, request, render_template, jsonify, current_app
from werkzeug.utils import secure_filename
import os
actions = Blueprint("actions", __name__)

def allowed_file(filename: str):
    ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'gif', 'png']
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@actions.route("/upload_image", methods=["POST", "GET"])
def upload_image():
    """
    Request data: formData
    response: json
    summery: will take image file and file type from client and save into each desire folder 
    """
    if request.method == "POST":
        image_type = request.form["image_type"]
        # check file is exist or not 
        if "image" not in request.files:
            return jsonify({
                "status": 404,
                "message": "File Not Found In Request Parameters"
            })
        # if profile is profile image
        if image_type == "profile_image":
            profile_image = request.files["image"]
            if profile_image and allowed_file(profile_image.filename):
                filename = secure_filename(profile_image.filename)
                profile_image.save(os.path.join(current_app.config["PROFILE_DIR"], filename))
                return jsonify({
                    "status": 200,
                    "message": "Profile Image Upload Success"
                })
            return jsonify({
                "status": 415,
                "message": "Unsupported file type"
            })
        # if image is post image 
        post_image = request.files["image"]
        if post_image and allowed_file(post_image.filename):
            filename = secure_filename(post_image.filename)
            post_image.save(os.path.join(current_app.config["POST_DIR"], filename))
            return jsonify({
                "status": 200,
                "message": "Post Image Upload Success"
            })
        return jsonify({
                "status": 415,
                "message": "Unsupported file type"
            })