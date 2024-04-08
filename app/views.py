from flask import Blueprint, render_template, redirect, url_for, session
from .login_required import check_user
views = Blueprint("views", __name__)

@views.route('/')
def index():
    state, message, user_id = check_user()
    if state:
        return render_template('index.html', title="HOME")
    return redirect(url_for("views.login", message=message))

@views.route('/post-area')
def post_area():
    state, message, user_id = check_user()
    if state:
        return render_template('post_area.html', title='Post Area')
    return redirect(url_for("views.login", message=message))

@views.route('/profile')
def profile():
    state, message, user_id = check_user()
    if state:
        return render_template('profile.html', title='Profile')
    return redirect(url_for("views.login", message=message))

@views.route("/upload")
def upload():
    return render_template("upload.html")

@views.route('/signup')
def signup():
    return render_template("signup.html")

@views.route('/login')
def login():
    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)
