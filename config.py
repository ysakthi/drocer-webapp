# Adapted from https://www.digitalocean.com/community/tutorials/how-to-structure-large-flask-applications

# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Define the database - we are working with
# SQLite for this example
#SQLALCHEMY_ENGINE = 'mysql+mysqldb://'
SQLALCHEMY_ENGINE = 'mysql+mysqlconnector://'
SQLALCHEMY_ECHO = False  # do not write SQLAlchemy to logs

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# generated with: hashlib.sha1(os.urandom(128)).hexdigest()

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "093dfce55b9259d2521e67cdbeb3ad907f6d4d3c"

# Secret key for signing cookies
SECRET_KEY = "7a75e6cc32171cbe5fa68c4eee8cf36a6d4ce82b"

# Path to page images
PAGE_IMAGES_PATH = os.path.join(BASE_DIR,"data/png")
