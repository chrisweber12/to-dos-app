# To-Do's App

Multi-user Flask application that allows users to create accounts and save, prioritize, and schedule tasks in a to-do list

### Usage

The *bootstrap.sh* file will do all the work in running the API - it initializes the Flask app, creates a virtual environment venv, sources to the virtual environment, installs dependencies from requirements.txt, and runs the app. In the main directory, simply run the command `./bootstrap.sh`.

From here, you can navigate to http://localhost:3000 and you will see a welcome page. From here, users can register or login. After login, users will be brought to a to-do list page, from which they can add, edit, schedule, and prioritize tasks. To change priority, users can use the up and down arrows to move tasks around the list.

### Program Structure

The main *app.py* file contains the app initialization and the route functions. The *forms.py* file contains classes for the login & registration forms and the create & edit task forms. The *templates* folder contains HTML templates that are loaded by the route functions in *app.py* and help implement the structure of the pages and the forms from *forms.py*. The *models.py* file contains the initialization code for the application database, implemented through SQLAlchemy, and a class for both the User and ToDo models for the database. When the first user is created, a *book.sqlite* file will be created and database information will be saved locally on this file, so login information and user data will be available across sessions.
