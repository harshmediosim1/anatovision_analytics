#Python Import 

#Flask Import
from flask_admin.contrib.sqla import ModelView
#App Import
from apps import create_app
from apps.models import db
#Third-part Import

import os


'''This block of code is setting up a Flask application with Flask-Admin integration. Here's a
breakdown of what each part does:'''
app = create_app()


# Set the secret key using the environment variable
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')



if __name__ == "__main__":
    db.create_all()
    os.getenv("DEBUG")
    app.run(host="0.0.0.0", port=5000)  # Use 0.0.0.0 to allow external access