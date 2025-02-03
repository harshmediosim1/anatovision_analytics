Cadaviz Analytics Dashbaord

step1 - used Flask App python 3.10.10

Database Used - Postgresql 

Database Migrations- 
- git db init (This creates a migrations/ directory to track migrations.)
- git db migrate -m "comment" (This command will generate a migration script based on the current state of your models.)
- flask db upgrade (This command applies the migration to the database.)

Run Flask Application-
- flask run / python run.py
