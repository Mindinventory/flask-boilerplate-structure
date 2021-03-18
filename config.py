import os

# Statement for enabling the development environment
DEBUG = True

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'sqlite3.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
DATABASE_CONNECT_OPTIONS = {}

# Enable protection against *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = os.urandom(24)

# Secret key for signing cookies
SECRET_KEY = os.urandom(24)

# Configuration of a mail account for sending mails
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'Your Email'
MAIL_PASSWORD = 'Your Password'
ADMINS = ['Your Email']

# Admin credentials
ADMIN_CREDENTIALS = ('admin', 'admin')
FLASK_ADMIN_SWATCH = 'cerulean'
WTF_CSRF_ENABLED = False
