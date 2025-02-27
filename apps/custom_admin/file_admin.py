# Python Import

# Flask Import
from flask import request, redirect, url_for, flash, send_file
from flask_admin import expose, BaseView
# App Import
from apps.models import FileUpload, AnalyticsData  # Import AnalyticsData
from apps import db
# Third-party Import
from werkzeug.utils import secure_filename
import io
import csv
from io import StringIO
from datetime import datetime
import hashlib

def generate_file_hash(file_data):
    """Generate a hash for the file content to check for duplicates."""
    hash_md5 = hashlib.md5()
    hash_md5.update(file_data)
    return hash_md5.hexdigest()

def parse_date(date_str):
    """Try multiple date formats to parse the date."""
    for fmt in ("%Y-%m-%d", "%Y/%m/%d"):  # Add more formats if needed
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Time data '{date_str}' does not match expected formats")

class FileAdminView(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def index_view(self):
        if request.method == 'POST' and 'file' in request.files:
            file = request.files['file']
            if file.filename:
                filename = secure_filename(file.filename)

                # Read the file data
                file_data = file.read()

                try:
                    # Check if a file with the same name already exists
                    existing_file = FileUpload.query.filter_by(filename=filename).first()

                    # If the file exists, delete old AnalyticsData entries related to the file
                    if existing_file:
                        analytics_data_entries = AnalyticsData.query.filter_by(file_id=existing_file.id).all()
                        for entry in analytics_data_entries:
                            db.session.delete(entry)
                        db.session.commit()

                        # Remove the old file from the database
                        db.session.delete(existing_file)
                        db.session.commit()

                    # Save the new file in the database as binary
                    new_file = FileUpload(filename=filename, file_data=file_data)
                    db.session.add(new_file)
                    db.session.commit()

                    # Extract and process data from the uploaded CSV file
                    file.seek(0)  # Reset file pointer to start
                    file_content = StringIO(file.read().decode('utf-8'))
                    csv_reader = csv.DictReader(file_content)

                    # Insert the new data into the AnalyticsData model
                    for row in csv_reader:
                        try:
                            # Extract and parse date
                            date_str = row.get('date', '').strip()
                            parsed_date = parse_date(date_str) if date_str else datetime.now().date()

                            new_entry = AnalyticsData(
                                version=row.get('version', 'N/A'),
                                user_id=row.get('user_id', 'N/A'),
                                college=row.get('college', 'N/A'),
                                location=row.get('location', 'N/A'),
                                module=row.get('module', 'N/A'),
                                submodule=row.get('submodule', ''),
                                time=row.get('time', datetime.now().strftime("%H:%M:%S")),
                                duration=row.get('duration', '0'),
                                date=parsed_date,
                                file_id=new_file.id  # Link the AnalyticsData entry to the file
                            )
                            db.session.add(new_entry)
                        except Exception as e:
                            flash(f"Error processing row {row}: {str(e)}", 'danger')
                            continue  # Skip this row and move to the next one

                    # Commit to the database
                    db.session.commit()

                    flash(f"File '{filename}' uploaded, old data overridden, and new data extracted successfully!", 'success')

                except Exception as e:
                    flash(f"An error occurred: {str(e)}", 'danger')
                    db.session.rollback()  # Rollback in case of error

                return redirect(url_for('.index_view'))

        # Retrieve all files to display on the admin panel
        files = FileUpload.query.all()
        return self.render('admin/file_admin.html', files=files)

    @expose('/download/<int:file_id>')
    def download_file(self, file_id):
        file_record = FileUpload.query.get_or_404(file_id)
        return send_file(
            io.BytesIO(file_record.file_data),
            as_attachment=True,
            download_name=file_record.filename
        )
    
    @expose('/delete/<int:file_id>')
    def delete_file(self, file_id):
        file_record = FileUpload.query.get_or_404(file_id)
        db.session.delete(file_record)
        db.session.commit()
        flash(f"File '{file_record.filename}' deleted successfully!", 'success')
        return redirect(url_for('.index_view'))
