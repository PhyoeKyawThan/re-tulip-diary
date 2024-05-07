from flask import Blueprint, request, render_template, jsonify, current_app, session
from werkzeug.utils import secure_filename
from .models import Post, User, Comment
from .login_required import check_user
from . import db
import os

actions = Blueprint("actions", __name__)
# function for checking file extension
def allowed_file(filename: str):
    """
    check the file extension for unreasonable risk
    """
    ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'gif', 'png']
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# comment (/action/comment)
@actions.route("/comment", methods=["POST", "GET"])
def comment():
    """
    request data type: json
    parameters: text( str ), post_id( int )
    response: json
    summery: will take json data from user and the key comment to save in database by each user id and each post
    """
    # check user is already logged in or not
    state, message, user_id = check_user()
    # if user not logged in yet
    if state == False:
        return jsonify({
            "status": 401,
            "message": message
        })
    # check request method for security purpose
    if request.method == "POST":
        # get json data from user
        comment_data = request.get_json()
        # check whether the post is exists or not
        post_exists = Post.query.filter_by(post_id = comment_data["post_id"]).first()
        # if post is exists 
        if post_exists:
            # initial new comment
            new_comment = Comment(text=comment_data["text"], post_id = comment_data["post_id"], user_id = user_id)
            db.session.add(new_comment)
            db.session.commit()
            db.session.close()
            socket.emit("commented", f"{comment_data['post_id']}")
            return jsonify({
                "status": 200, 
                "message": "Commented"
            })
        return jsonify({
            "status": 404,
            "message": "Post Not Found"
        })
    return render_template("errors/method_not_allowed.html")

# post(action/post_upload)
@actions.route("/post_upload", methods=["POST", "GET"])
def upload_post():
    """
    Request data: json 
    patameters: caption
    response: json
    summery: will take post data from client and save into database
    """
    # check request client is logged in or not if not 401
    state, message, user_id = check_user()
    if state == False:
        return jsonify({
            "status": 401,
            "message": message
        })
    # check user request method is post
    if request.method == "POST":
        post_data = request.get_json()
        if post_data["caption"]:
            new_post = Post(caption = post_data["caption"],
                            user_id = user_id
            )
            db.session.add(new_post)
            db.session.commit()
            response_data = {
                "status": 200,
                "message": "Successfully Uploaded",
                "post_id": new_post.post_id
            }
            db.session.close()
            return jsonify(response_data)
        return jsonify({
            "status": 204,
            "message": "Caption is empty"
        })
    return render_template("errors/method_not_allowed.html")
#
# image upload (/action/upload_image)
@actions.route("/upload_image", methods=["POST", "GET"])
def upload_image():
    """
    Request data: formData
    parameters: image_type( str ), image( file ), post_id( int ) 
    response: json
    summery: will take image file and file type from client and save into each desire folder 
    """
    # check request client is logged in or not if not 401
    state, message, user_id = check_user()
    if state == False:
        return jsonify({
            "status": 401,
            "message": message
        })
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
                # check user is exists
                user = User.query.filter_by(user_id = user_id ).first()
                #  if user is exists
                if user:
                    filename = secure_filename(profile_image.filename)
                    profile_image.save(os.path.join(current_app.config["PROFILE_DIR"], filename))
                    # update profile_uri
                    user.profile_uri = "/static/images/profile/" + filename
                    db.session.commit()
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
        post_id = request.form["post_id"]
        if post_image and allowed_file(post_image.filename):
            # post data to add path
            post = Post.query.filter_by(post_id = post_id).first()
            # if post is exists
            if post:
                filename = secure_filename(post_image.filename)
                post_image.save(os.path.join(current_app.config["POST_DIR"], filename))
                # add post image uri path to db
                post.image_uri = "/static/images/post/" +  filename
                # commit change
                db.session.commit()
                return jsonify({
                    "status": 200,
                    "message": "Post Image Upload Success"
                })
            return jsonify({
                "status": 404,
                "message": "Post Not Found"
            })
        return jsonify({
                "status": 415,
                "message": "Unsupported file type"
            })
    return render_template("errors/method_not_allowed.html")