#Python Import

#Flask Import

#App Import
from apps import db
#Third-Party Import
from datetime import datetime


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
    def __repr__(self):
        return f'<SessionData {self.id} - User {self.version}>'


class FileUpload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    file_data = db.Column(db.LargeBinary, nullable=False)  # Store the file itself as binary data

    def __repr__(self):
        return f'<FileUpload {self.filename}>'