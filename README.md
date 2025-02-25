# Cadaviz-Analytics Dashboard

This project is a web Api's application for managing data to shows in analytical format(Table, LineChart, pieChart), also shows active users.

## Features
- Post Api For Post the data in DB.
- GET Api For Get the data and shows on dashboard.

## Tech Stack
- **Backend**: Python, Flask
- **Frontend**: Dash
- **Database**: PostgreSQL

## Prerequisites
- Python 3.10 or above
- pip (Python package installer)

## Create and activate a virtual environment:
```
python -m venv venv
```
## Install dependencies:
```
pip install -r requirements.txt
```
## Apply migrations to set up the database:
```
flask db init (This creates a migrations/ directory to track migrations.)
flask db migrate -m "comment" (This command will generate a migration script based on the current state of your models.)
flask db upgrade (This command applies the migration to the database.)
```
## Run the development server:
```
flask run
```
## Open the application in your browser at:
```
http://127.0.0.1:5000/
```
## Docker Setup:
create two docker files for one one of flask app and one of cadaviz 
compose file containt services - Dash app, flask App and Postgresql DB
services Name- Flask App(cadaviz_web), Dash App(dash_app), Database(db)

## Docker Initial Commands:
```
docker-compose build (for build the image and container)
docker-compose up (for run the container)
```
## Docker DB Upgrade Command:
```
docker-compose exec cadaviz_web flask db upgrade(cadaviz_web i.e our flask app service name)
```
## Project Structure:
```bash
cadaviz-analytics/
├── apps/                       #flask apps
│   ├── custom_admin/           # POST api Defination
│   ├   ├── __init__.py
│   ├   ├── analytics_admin.py  
│   ├   ├── file_admin.py
│   ├   ├── user_admin.py
│   ├── routes/                 # GET api Defination
│   ├   ├── __init__.py
│   ├   ├── ai_routes.py
│   ├   ├── auth_routes.py
│   ├   ├── unity_routes.py
│   ├── templates/              # Contains HTML templates for flask admin
│   ├   ├── analytics_data.html           
│   ├   ├── file_admin.html            
│   ├   ├── master.html 
│   ├   ├── login.html
│   ├   ├── index.html
│   ├── static/              # Contains HTML templates for flask admin
│   ├   ├── images/  
│   ├       ├── cadaviz.png    
│   ├── tests/
│   ├── utils/                
│   ├── __init__.py
│   ├── models.py       # Defined model for analyticals data and file upload 
├── cadaviz/            # Dash App
│   ├── apps
│   ├   ├── __init__.py
│   ├   ├── callback.py
│   ├   ├── charts.py  
│   ├   ├── data_processing.py
│   ├   ├── layout.py         
│   ├── app.py          
│   ├── Dockerfile  
│   ├── requirements.txt       #dash app requirements    
│
├── migrations/         # flask app db migrations
├── .gitignore 
├── config.py           # project configuration
├── run.py              # main file for entry into app
├── docker-compose.yml  # file contains services for flask, dash, db 
├── Dockerfile          # flask app file
├── README.md
├── requirements.txt    # flask level dependancy

```

## Create Admin User Using Flask:
```
Open flask shell using flask shell
from apps import db
from apps.models import User
admin_user=User(username="admin", email="admin@immersivelabz.com", is_admin=True)
admin_user.set_password("admin")
db.session.add(admin_user)
db.session.commit()
```
## Create Admin User Using Flask for docker:
- if we used docker container then we have to create admin user in container isloation using following steps. 
1.  Create Admin User Inside the Dockerized Flask App(Access the Flask App Container)
    cmd -
     ```
     docker exec -it cadaviz_web sh  (cadaviz_web is our flask service name)
     ```

    Then followed the next cmd using flask shell    
```

    Open flask shell - flask shell
    extecutes following cmd
    from apps import db
    from apps.models import User
    admin_user=User(username="admin", email="admin@immersivelabz.com", is_admin=True)
    admin_user.set_password("admin")
    db.session.add(admin_user)
    db.session.commit()
```