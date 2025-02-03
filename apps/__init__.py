#Python Import
#Flask Import
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin

db = SQLAlchemy()
migrate = Migrate()

#Admin Register
admin = Admin(name='Cadaviz Analytics', template_mode='bootstrap4')


""" The 'create_app' function initializes a Flask application with SQLAlchemy database, migration
    support, and an admin interface, along with registering various views and blueprints for different
    functionalities.
    :return: The 'create_app()' function is returning a Flask application instance that has been
    configured with SQLAlchemy for database operations, Flask-Migrate for database migrations, and
    Flask-Admin for administrative interface. It also registers various views and blueprints for
    different parts of the application such as analytics data, file upload, Unity routes, and AI routes.
    """
def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object('config.Config')
    db.init_app(app)
    migrate.init_app(app,db)
    admin.init_app(app)

    from apps.custom_admin.file_admin import FileAdminView
    from apps.custom_admin.analytics_admin import CustomAnalyticsView

    # Register models and views
    admin.add_view(CustomAnalyticsView(name='Analytics Data',endpoint='analytics_data'))
    admin.add_view(FileAdminView(name='File Upload', endpoint='file_admin'))
    
    # Register blueprints
    from apps.routes.unity_routes import unity_bp
    from apps.routes.ai_routes import ai_bp

    app.register_blueprint(unity_bp, url_prefix='/unity')
    app.register_blueprint(ai_bp, url_prefix='/ai')

    return app
