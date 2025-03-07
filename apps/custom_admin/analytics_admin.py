#Python Import

#Flask Import
from flask_admin import BaseView, expose
from flask import render_template, flash, redirect,url_for,request
# App Import
from apps.models import AnalyticsData
from apps import db
from sqlalchemy import desc  # Import for sorting
"""
This Python class defines a custom analytics view that queries and displays analytics data using a
 custom template.
"""
class CustomAnalyticsView(BaseView):
    # You can set a name for this view
    def is_accessible(self):
        # Add your authentication or permission check logic here
        return True

    @expose('/')
    def index(self):
        page = request.args.get('page', 1, type=int)  # Get page number from request, default to 1
        per_page = 10  # Number of records per page

        # Query analytics data with pagination
        # pagination = AnalyticsData.query.paginate(page=page, per_page=per_page, error_out=False)
        pagination = AnalyticsData.query.order_by(desc(AnalyticsData.id)).paginate(
        page=page, per_page=per_page, error_out=False
        )
        data = pagination.items  # Get records for the current page

        return self.render('admin/analytics_data.html', data=data, pagination=pagination)