from .models import User
from flask import session, redirect, url_for
def check_user()->set:
    """
    this function take session data as input and no need to add manually 
    check the session with current_user is empty or not
    if session exists check the db with session creditical and return true if exists
    """
    if "current_user" in session:
        current_user = session["current_user"]
        user = User.query.filter_by(user_id = current_user["user_id"],
                                    email = current_user["email"], 
                                    password = current_user["password"]).first()
        if user:
            return (True, "User Found", user.user_id)
        else:
            return (False, "Your using wrong user data to access through session", None)
    return (False, "Your have to login first before access this content", None)
