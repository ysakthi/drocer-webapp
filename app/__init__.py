# Import flask and template operators.
from flask import Flask, render_template, request, session, redirect, url_for

# Define the WSGI application object.
wsgi_app = Flask(__name__, static_url_path='/static', static_folder='static')

# Import application classes.

# Setup logging.
import logging
#logging.Formatter(fmt='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)s: %(module)s.%(funcName)s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)
logger.info('WSGI application initialized.')


# Add error handlers.
@wsgi_app.errorhandler(404)
def error_handler_404(error):
    logger.error(error)
    return "File note found.", 404

@wsgi_app.errorhandler(Exception)
def error_handler_500(error):
    logger.error(error)
    import sys, os
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    logger.debug(str(exc_type) + " " + str(fname) + " " + str(exc_tb.tb_lineno))

    return "Server error.", 500

# Add application routes
@wsgi_app.route('/', methods=['GET'])
def route_landing():
    return render_template('landing.html')

@wsgi_app.route('/about', methods=['GET'])
def route_about():
    return render_template('about.html')


