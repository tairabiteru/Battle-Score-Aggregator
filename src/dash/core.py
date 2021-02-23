"""
This module defines the dashboard.

The dashboard is effectively the web interface that the user interacts with.
This module defines the configuration of the dashboard from conf.py, then
sets the routes from routes.py.
"""

from dash.conf import conf
from dash.routes import routes
from orm.judge import Judge

from aiohttp import web
import aiohttp_jinja2
import aiohttp_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import base64
from cryptography import fernet
import jinja2


class Dash:
    """Class defines the dashboard."""

    def __init__(self):
        self.host = conf.host
        self.port = conf.port
        self.templateDirectory = conf.templateDirectory
        self.staticDirectory = conf.staticDirectory

    def setup(self):
        """Perform setup."""
        self.app = web.Application()

        # Load Jinja2
        aiohttp_jinja2.setup(self.app, loader=jinja2.FileSystemLoader(self.templateDirectory))

        # Set keys for session encryption
        fernet_key = fernet.Fernet.generate_key()
        secret_key = base64.urlsafe_b64decode(fernet_key)
        aiohttp_session.setup(self.app, EncryptedCookieStorage(secret_key))

        # Add /static and routes
        self.app.router.add_static('/static/', path=self.staticDirectory, name='static')
        self.app.add_routes(routes)

        # Clear all help flags
        judges = Judge.obtainall()
        for judge in judges:
            judge.helpFlag = False
            judge.save()

    def run(self):
        if conf.adminEnabled:
            print("!!! WARNING !!!   ADMIN INTERFACE IS ENABLED!")
            print("This should NEVER be enabled during production!")
            print("If you are in production, SHUT IT DOWN IMMEDIATELY and change the config.")
        self.setup()
        web.run_app(self.app, host=self.host, port=self.port)
