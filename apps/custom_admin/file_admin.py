#Python Import

#Flask Import
from flask import request, redirect, url_for, flash, send_file
from flask_admin import expose, BaseView
#App Import
from apps.models import FileUpload, AnalyticsData  # Import AnalyticsData
from apps import db
#Third-party Import
from werkzeug.utils import secure_filename
import io
import csv
from io import StringIO
from datetime import datetime

'''The `FileAdminView` class in Python defines methods for uploading, extracting data from file,
downloading, and deleting files in a web application.'''

class FileAdminView(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def index_view(self):
        if request.method == 'POST' and 'file' in request.files:
            file = request.files['file']
            if file.filename:
                filename = secure_filename(file.filename)

                try:
                    # Save file in the database as binary
                    file_data = file.read()
                    new_file = FileUpload(filename=filename, file_data=file_data)
                    db.session.add(new_file)
                    db.session.commit()

                    # Reset file pointer to the beginning after reading
                    file.seek(0)
                    
                    # Extract data from the file (assuming CSV)
                    file_content = StringIO(file.read().decode('utf-8'))
                    csv_reader = csv.DictReader(file_content)

                    for row in csv_reader:
                        # Assuming the CSV contains the necessary columns for AnalyticsData
                        # new_entry = AnalyticsData(
                        #     version=row.get('version', 'N/A'),
                        #     user_id=row.get('user_id', 'N/A'),
                        #     college=row.get('college', 'N/A'),
                        #     location=row.get('location', 'N/A'),
                        #     module=row.get('module', 'N/A'),
                        #     submodule=row.get('submodule', ''),  # Handle optional field
                        #     time=row.get('time', datetime.now().strftime("%H:%M:%S")),
                        #     duration=row.get('duration', '0'),
                        #     date=datetime.strptime(row.get('date', datetime.now().strftime("%Y-%m-%d")),'%Y-%m-%d').date()
                        # )
                        # db.session.add(new_entry)
                        try:
                            date_str = row.get('date', '').strip()
                            parsed_date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else datetime.now().date()

                            new_entry = AnalyticsData(
                                version=row.get('version', 'N/A'),
                                user_id=row.get('user_id', 'N/A'),
                                college=row.get('college', 'N/A'),
                                location=row.get('location', 'N/A'),
                                module=row.get('module', 'N/A'),
                                submodule=row.get('submodule', ''),
                                time=row.get('time', datetime.now().strftime("%H:%M:%S")),
                                duration=row.get('duration', '0'),
                                date=parsed_date
                            )
                            db.session.add(new_entry)
                        except Exception as e:
                            flash(f"Error processing row {row}: {str(e)}", 'danger')

                    # Commit to the database
                    db.session.commit()

                    flash(f"File '{filename}' uploaded and data extracted successfully!", 'success')

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