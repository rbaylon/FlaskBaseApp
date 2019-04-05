# FlaskBaseApp
A base flask application with user management already in place. Features wtforms/ web front end and rest API. The purpose of this app is to get you started with flask and save time building a user login/management. You can easily extend this app by creating a new model view and controller.

# Installation

1. Install postgresql server on your machine.
2. Install pipenv
3. cd FlaskBaseApp
4. pipenv install
5. create the database and database user(refer to postgresql documentation)
6. Initialize the database and create the tables.
	6.a. pipenv run python migrate db init
	6.b. pipenv run python migrate db migrate
	6.c. pipenv run python migrate db upgrade
7. Create the application admin user
	7.a. pipenv run python3 createadmin.py
8. Run the app
	8.a. pipenv run python3 run.py
