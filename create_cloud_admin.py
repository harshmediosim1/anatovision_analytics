import os
from apps import create_app, db
from apps.models import User

# --- PASTE YOUR RENDER EXTERNAL DATABASE URL HERE ---
# It should look like: postgres://anatovision...
CLOUD_DB_URL = "postgres://..."

if __name__ == "__main__":
    if CLOUD_DB_URL == "postgres://...":
        print("Please paste your External Database URL into CLOUD_DB_URL on line 6!")
        exit()

    print(f"Connecting to Cloud Database...")
    
    # Temporarily override the app config to point to the cloud DB
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = CLOUD_DB_URL
    app.config['SECRET_KEY'] = 'temp-secret-key'
    
    with app.app_context():
        # Ensure tables exist just in case
        db.create_all()
        
        # Check if admin already exists
        existing_admin = User.query.filter_by(username='admin').first()
        if existing_admin:
            print("Admin user already exists in the cloud database!")
        else:
            print("Creating admin user...")
            admin = User(username='admin', email='admin@example.com', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("SUCCESS! Admin user created. You can now log into your live dashboard.")
