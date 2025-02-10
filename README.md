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
git db init (This creates a migrations/ directory to track migrations.)
git db migrate -m "comment" (This command will generate a migration script based on the current state of your models.)
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
## Docker DB Uograde Command:
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
│   ├── routes/                 # GET api Defination
│   ├   ├── __init__.py
│   ├   ├── ai_routes.py
│   ├   ├── unity_routes.py
│   ├── templates/              # Contains HTML templates for flask admin
│   ├   ├── analytics_data.html           
│   ├   ├── file_admin.html            
│   ├   ├── master.html        
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
