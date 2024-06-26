from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify
from .login_required import check_user
from .models import Post, User
views = Blueprint("views", __name__)

@views.route('/')
def index():
    state, message, user_id = check_user()
    if state:
        return render_template('base.html', title="HOME")
    return redirect(url_for("views.login", message=message))

# home page text/html data with posts
@views.route("/home")
def home():
    state, message, user_id = check_user()
    if state:
        posts = Post.query.order_by(Post.post_id.desc()).all()
        post_datas = []
        for post in posts:
            posted_user = User.query.filter_by(user_id = post.user_id).first()
            data = {
                "post_id": post.post_id,
                "profile_uri": posted_user.profile_uri,
                "username": posted_user.username,
                "caption": post.caption,
                "image_uri": post.image_uri,
                "posted_date": post.posted_date,
                "comment_count": len(post.comments)
            }
            post_datas.append(data)
        return render_template('index.html', posts=post_datas, profile_uri=User.query.filter_by( user_id = user_id).first().profile_uri)
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

@views.route('/signup')
def signup():
    return render_template("signup.html")

@views.route('/login')
def login():
    return render_template("login.html")

# get comments data from post using unique post_id
@views.route("/get_all_comments", methods=["POST", "GET"])
def get_all_comments():
    """
    request parem: post_id( int ) from url pattern para
    response: related comment data with respective post_id 
    summery: will take post_id( int ) from requested parem and returning respective comments if post_id exists
    """
    state, message, user_id = check_user()
    if state:
        post_id = request.args.get("post_id")
        related_post = Post.query.filter_by( post_id = post_id ).first()
        datas = []
        for comment in related_post.comments:
            related_user = User.query.filter_by( user_id = comment.user_id ).first()
            data = {
                "profile_uri": related_user.profile_uri,
                "username": related_user.username,
                "comment_text": comment.text,
                "commented_date": comment.commented_date,
                "is_check": comment.is_check
            }
            datas.append(data)
            
        return jsonify({
            "status": 200,
            "comments": datas,
            "post_id": related_post.post_id
            })
    return redirect(url_for("views.login", message=message))
    
@views.route("/check_noti")
def check_notification():
    pass

@views.route("/stram_notification")
def stram_notification():
    state, message, user_id = check_user()
    if state:
        pass

if __name__ == '__main__':
    app.run(debug=True)
