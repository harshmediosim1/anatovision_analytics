#Python Import

#Flask Import
from flask_admin import BaseView, expose
from flask import render_template, flash, redirect,url_for
# App Import
from apps.models import AnalyticsData
from apps import db

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
        # Query all the analytics data
        data = AnalyticsData.query.all()

        # Render a custom template to display the data
        return self.render('admin/analytics_data.html', data=data)