#Python Import

#Flask Import
#App Import
from apps import db
#Third-Party Import
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


'''This class represents a model for storing analytics data related to user sessions with attributes
such as version, user ID, college, location, module, submodule, time, duration, and date.'''
class AnalyticsData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String(155), nullable=False)
    user_id = db.Column(db.String(175),nullable=False)
    college = db.Column(db.String(175), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    module = db.Column(db.String(100), nullable=False)
    submodule = db.Column(db.String(100), nullable=True)
    time = db.Column(db.String(50), nullable=False, default=lambda: datetime.now().strftime("%H:%M:%S"))
    duration = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    file_id = db.Column(db.Integer, db.ForeignKey('file_upload.id'), nullable=True) 

    # def __repr__(self):
    #     return f'<SessionData {self.id} - User {self.version}>'
    def __repr__(self):
        return f'<AnalyticsData {self.id} - Version {self.version}>'


class FileUpload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    file_data = db.Column(db.LargeBinary, nullable=False)  # Store the file itself as binary data

    # def __repr__(self):
    #     return f'<FileUpload {self.filename}>'
    def __repr__(self):
        return f'<FileUpload {self.filename} - Uploaded on {self.uploaded_at}>'
 

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    posts = db.relationship("Post", back_populates="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="posts")