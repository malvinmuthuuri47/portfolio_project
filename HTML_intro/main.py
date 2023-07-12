from website import create_app
from website import db
from website.models import User, Hotels

app = create_app()  # Instantiate the function that instantiates the flask app

if __name__ == '__main__':
    app.run()