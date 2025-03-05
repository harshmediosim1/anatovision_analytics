#Python Import

#Flask Import
from flask import request, redirect, url_for, flash, send_file
from flask_admin import expose, BaseView
#App Import
from apps.models import FileUpload, AnalyticsData
from apps import db
#Third-Party Import
import io
import csv
import hashlib
from datetime import datetime
from werkzeug.utils import secure_filename
from io import StringIO


def generate_file_hash(file_data):
    """Generate a hash for the file content to check for duplicates."""
    hash_md5 = hashlib.md5()
    hash_md5.update(file_data)
    return hash_md5.hexdigest()


def parse_date(date_str):
    """Try multiple date formats to correctly parse the date from CSV."""
    date_formats = ["%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y", "%m-%d-%Y", "%m/%d/%Y"]

    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    
    print(f"Warning: Unable to parse date '{date_str}', storing as NULL")
    return None  # Return None instead of defaulting to today’s date

# The `FileAdminView` class in Python defines methods for uploading, processing, downloading, and
# deleting CSV files with specific validations and database operations.

class FileAdminView(BaseView):
    ALLOWED_EXTENSIONS = {'csv'}  # Allowed file extensions
    ALLOWED_MIME_TYPES = {'text/csv', 'application/vnd.ms-excel'}

    def is_allowed_file(self, filename, mimetype):
        """Check if the file has an allowed extension and MIME type."""
        extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        return extension in self.ALLOWED_EXTENSIONS and (mimetype in self.ALLOWED_MIME_TYPES or mimetype == '')

    @expose('/', methods=['GET', 'POST'])
    def index_view(self):
        if request.method == 'POST' and 'file' in request.files:
            file = request.files['file']
            if file.filename:
                filename = secure_filename(file.filename)
                mimetype = file.mimetype

                if not self.is_allowed_file(filename, mimetype):
                    flash("Invalid file format! Please upload a CSV file only.", "danger")
                    return redirect(url_for('.index_view'))

                file_data = file.read()

                try:
                    existing_file = FileUpload.query.filter_by(filename=filename).first()
                    if existing_file:
                        AnalyticsData.query.filter_by(file_id=existing_file.id).delete()
                        db.session.delete(existing_file)
                        db.session.commit()

                    new_file = FileUpload(filename=filename, file_data=file_data)
                    db.session.add(new_file)
                    db.session.commit()

                    file.seek(0)
                    file_content = StringIO(file.read().decode('utf-8'))
                    csv_reader = csv.DictReader(file_content)

                    for row in csv_reader:
                        try:
                            if all(not str(value).strip() for value in row.values()):
                                continue  # Skip empty rows

                            date_str = row.get('date', '').strip()
                            parsed_date = parse_date(date_str)  # Now returns None if parsing fails

                            new_entry = AnalyticsData(
                                version=row.get('version', ''),
                                user_id=str(row.get('user_id', '')),
                                college=row.get('college', ''),
                                location=row.get('location', ''),
                                module=row.get('module', ''),
                                submodule=row.get('submodule', ''),
                                time=row.get('time', datetime.now().strftime("%H:%M:%S")),
                                duration=row.get('duration', '0'),
                                date=parsed_date,  # Stores None if parsing failed
                                file_id=new_file.id
                            )
                            db.session.add(new_entry)
                        except Exception as e:
                            print(f"Error processing row {row}: {str(e)}")
                            continue  # Skip problematic row

                    db.session.commit()
                    flash(f"File '{filename}' uploaded successfully, and data extracted!", 'success')

                except Exception as e:
                    flash(f"An error occurred: {str(e)}", 'danger')
                    db.session.rollback()

                return redirect(url_for('.index_view'))

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
        AnalyticsData.query.filter_by(file_id=file_record.id).delete()
        db.session.commit()
        db.session.delete(file_record)
        db.session.commit()

        flash(f"File '{file_record.filename}' deleted successfully!", 'success')
        return redirect(url_for('.index_view'))
