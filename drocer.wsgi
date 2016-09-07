# WSGI application configuration

## activate virtual environment
import os
import sys
application_path = os.path.dirname(os.path.abspath(__file__))

activate_this = '%s/%s' % (application_path, 'venv/bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

# import application
sys.path.insert(0, application_path)
from app import wsgi_app as application # note the entry-point name 'application' is required by mod_uwsgi
application.config.from_object('config')
