from flask import Flask
from flask_admin import Admin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.toolbox.admin import AdminView

# Define the WSGI application object
app = Flask(__name__)


# Configurations
app.config.from_object('config')


# Setup the mail server
from flask_mail import Mail
mail = Mail(app)

# Define the database object
db = SQLAlchemy(app)
# Migrate database
migrate = Migrate(app, db)
# Faker for seeding task
from faker import Faker
fake = Faker()


from app.auth.models import User
ad = Admin(app)
ad.add_view(AdminView(User, db.session))


# Import a module / component using its blueprint handler variable
from app.api.v1.routes import api as api_blueprint
from app.auth.routes import auth

# Register blueprint(s)
app.register_blueprint(api_blueprint)
app.register_blueprint(auth)


# If True it generates fake data
# First argument is for how many fake data generated
from app.seeding import add_users

app.cli.add_command(add_users)



