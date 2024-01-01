
from website import create_app, db
from flask_migrate import Migrate


app = create_app()
migrate = Migrate(app, db)

# Only if this file is ran, will the following line be executed:
if __name__ == '__main__':
    # Will run flask application and start up the web server; everytime a change is made to python code it will
    # automatically rerun the web server
    app.run(debug=True)  # Remove this code when you're done coding
