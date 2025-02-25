#Python Import
#Flask Import
from flask import Flask,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin,AdminIndexView
from flask_login import LoginManager,current_user



db = SQLAlchemy()
migrate = Migrate()

    
#Admin Register
login_manager = LoginManager()
login_manager.login_view = "auth.login"
admin = Admin(name='Cadaviz Analytics', template_mode='bootstrap4')
admin.template_mode = 'bootstrap4'

# Custom Admin Index View for Access Control
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login"))
    
    
""" The 'create_app' function initializes a Flask application with SQLAlchemy database, migration
    support, and an admin interface, along with registering various views and blueprints for different
    functionalities.
    :return: The 'create_app()' function is returning a Flask application instance that has been
    configured with SQLAlchemy for database operations, Flask-Migrate for database migrations, and
    Flask-Admin for administrative interface. It also registers various views and blueprints for
    different parts of the application such as analytics data, file upload, Unity routes, and AI routes.
    """
def create_app():
    app = Flask(__name__, template_folder="templates",  static_folder='static')
    app.config.from_object('config.Config')
    db.init_app(app)
    migrate.init_app(app,db)
    login_manager.init_app(app)
    admin.init_app(app, index_view=MyAdminIndexView())
    
    from apps.custom_admin.file_admin import FileAdminView
    from apps.custom_admin.analytics_admin import CustomAnalyticsView
    from apps.models import User
    from apps.custom_admin.user_admin import UserAdminView
    
    # Register models and views
    admin.add_view(UserAdminView(User, db.session, name='Users', category='Users'))
    admin.add_view(CustomAnalyticsView(name='Analytics Data',endpoint='analytics_data'))
    admin.add_view(FileAdminView(name='File Upload', endpoint='file_admin'))
    
    # Register blueprints
    from apps.routes.unity_routes import unity_bp
    from apps.routes.ai_routes import ai_bp
    from apps.routes.auth_routes import auth_bp

    app.register_blueprint(unity_bp, url_prefix='/unity')
    app.register_blueprint(ai_bp, url_prefix='/ai')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app


from apps.models import User

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))