#Flask Imports
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required,current_user
#Appp Imports
from apps.models import User, db

auth_bp = Blueprint("auth", __name__, template_folder="templates")
"""
    The above code defines Flask routes for user login and logout functionality with authentication
"""

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.index"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            flash("Invalid username or password", "danger")
            return redirect(url_for("auth.login"))

        login_user(user)
        flash("Login successful!", "success")
        return redirect(url_for("admin.index"))

    return render_template("admin/login.html")



@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
