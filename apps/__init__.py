#Python Import
#Flask Import
from flask import Flask, redirect, url_for, request
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

# Custom Admin Index View for Access Control
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login"))

def init_dashboard(server):
    from dash import Dash
    from apps.dashboard.layout import serve_layout
    from apps.dashboard.callbacks import register_callbacks

    dash_app = Dash(
        __name__,
        server=server,
        url_base_pathname='/dashboard/',
        suppress_callback_exceptions=True
    )
    
    dash_app.layout = serve_layout
    register_callbacks(dash_app)

    # Protect Dashboard routes using Flask-Login
    @server.before_request
    def protect_dashboard():
        if request.path.startswith('/dashboard'):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))

    return dash_app

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

    @app.route('/')
    def root():
        return redirect('/dashboard/')

    # Initialize Dashboard
    app = init_dashboard(app).server

    return app

from apps.models import User

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))