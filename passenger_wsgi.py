"""
Post request dont work on Djano apps on A2 hosted servers. This replacement 'passenger_wsgi.py'
has fixed the issue for me. Works with Python 3.5 with Django 1.11, 2.0, 2.1, 2.2 and Python 3.7 with Django 3.0.
"""

# Keep this empty
SCRIPT_NAME = ''

class PassengerPathInfoFix(object):
    """
    Sets PATH_INFO from REQUEST_URI since Passenger doesn't provide it.
    """
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        from urllib.parse import unquote
        environ['SCRIPT_NAME'] = SCRIPT_NAME

        request_uri = unquote(environ['REQUEST_URI'])
        script_name = unquote(environ.get('SCRIPT_NAME', ''))
        offset = request_uri.startswith(script_name) and len(environ['SCRIPT_NAME']) or 0
        environ['PATH_INFO'] = request_uri[offset:].split('?', 1)[0]
        return self.app(environ, start_response)

# Replace projectname with the name of the main folder containing wsgi.py and setting.py
import brasileiraoapi.wsgi
application = brasileiraoapi.wsgi.application
application = PassengerPathInfoFix(application)