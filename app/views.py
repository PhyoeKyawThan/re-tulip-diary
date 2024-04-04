from flask import Blueprint, render_template

views = Blueprint("views", __name__)

@views.route('/')
def index():
    return render_template('index.html', title="HOME")

@views.route('/post-area')
def post_area():
    return render_template('post_area.html', title='Post Area')

@views.route('/profile')
def profile():
    return render_template('profile.html', title='Profile')

@views.route('/signup')
def signup():
    return render_template("signup.html")


if __name__ == '__main__':
    app.run(debug=True)
