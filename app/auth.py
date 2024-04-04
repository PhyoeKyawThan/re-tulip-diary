from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from .models import User
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
                        password = signup_data["password"])
            db.session.add(new_user)
            db.session.commit()
            db.session.close()
            return jsonify({"status": 200})
    else:
        return jsonify({"status": 405})


@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        is_user = User.query.filter_by(email = email, password = password ).first()
        if is_user:
            return redirect(url_for("index"))
        else:
            return redirect(url_for("login"))
    else: 
        return render_template("errors/method_not_allowed.html")