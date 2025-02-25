#Flask Imports
from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
# App Imports
from wtforms import PasswordField

"""
The `UserAdminView` class is a Flask admin view for managing user models with password field
encryption and access control based on user authentication and admin status.
"""

class UserAdminView(ModelView):
    form_extra_fields = {
        "password": PasswordField("New Password")
    }

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.set_password(form.password.data)
        super().on_model_change(form, model, is_created)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login"))
