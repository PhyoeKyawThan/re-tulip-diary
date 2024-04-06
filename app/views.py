from flask import Blueprint, render_template, redirect, url_for, session

views = Blueprint("views", __name__)

@views.route('/')
def index():
    if "current_user" not in session:
        return redirect(url_for("views.login"))
    return render_template('index.html', title="HOME")

@views.route('/post-area')
def post_area():
    if "current_user" not in session:
        return redirect(url_for("views.login"))
    return render_template('post_area.html', title='Post Area')

@views.route('/profile')
def profile():
    if "current_user" not in session:
        return redirect(url_for("views.login"))
    return render_template('profile.html', title='Profile')

@views.route('/signup')
def signup():
    return render_template("signup.html")

@views.route('/login')
def login():
    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)
