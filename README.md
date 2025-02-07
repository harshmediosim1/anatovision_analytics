Cadaviz Analytics Dashbaord

step1 - used Flask App python 3.10.10

Database Used - Postgresql 

Database Migrations- 
- git db init (This creates a migrations/ directory to track migrations.)
- git db migrate -m "comment" (This command will generate a migration script based on the current state of your models.)
- flask db upgrade (This command applies the migration to the database.)

Run Flask Application-
- flask run / python run.py


**Docker Setup:
create two docker files for one of cadaviz and one of Flask App
compose file containt services - Dash app, flask App and Postgresql DB
services Name- Flask App(cadaviz_web), Dash App(dash_app), Database(db)

Initial Commands:
docker-compose build(for build the image and container)
docker-compose up (for run the container)

Optional Commands:
docker-compose exec cadaviz_web flask db upgrade(cadaviz_web i.e our flask app service name)

**