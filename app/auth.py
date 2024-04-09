from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint("auth", __name__)

@auth.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        signup_data = request.get_json()
        # validate if user is already register or not
        user_exists = User.query.filter_by(email=signup_data["email"]).first()
        if user_exists:
            return jsonify({
                "status": 409,
                "message": "Email Already Registered!"
            })
        else:
            new_user = User(username = signup_data["username"],
                        email = signup_data["email"],
                        password = generate_password_hash(signup_data["password"]))
            db.session.add(new_user)
            db.session.commit()
            db.session.close()
            return jsonify({"status": 200, "message": "Your Account Have Been Created! Login Here"})
    else:
        return jsonify({"status": 405})


@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        is_user = User.query.filter_by(email = email).first() #check email is exists
        if is_user:
            # if email exist and check password 
            if check_password_hash(is_user.password, password):
                session["current_user"] = {
                    "user_id": is_user.user_id,
                    "email": is_user.email,
                    "password": is_user.password
                }
                return redirect(url_for("views.index"))
            return redirect(url_for("views.login", message="Username or Password Wrong"))
        else:
            return redirect(url_for("views.login", message="Email haven't registered Yet!"))
    else: 
        return render_template("errors/method_not_allowed.html")


@auth.route("/logout")
def logout():
    if "current_user" in session:
        session.pop("current_user")
        return redirect(url_for("views.login"))
    return redirect(url_for("views.login"))