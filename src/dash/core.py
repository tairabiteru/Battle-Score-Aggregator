"""Module that defines the dashboard."""

from dash.conf import conf
from dash.routes import routes

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
        """Initialize dashboard."""
        self.host = conf.host
        self.port = conf.port
        self.templateDirectory = conf.templateDirectory
        self.staticDirectory = conf.staticDirectory

    def setup(self):
        """Perform setup."""
        self.app = web.Application()

        aiohttp_jinja2.setup(self.app, loader=jinja2.FileSystemLoader(self.templateDirectory))

        fernet_key = fernet.Fernet.generate_key()
        secret_key = base64.urlsafe_b64decode(fernet_key)
        aiohttp_session.setup(self.app, EncryptedCookieStorage(secret_key))

        self.app.router.add_static('/static/', path=self.staticDirectory, name='static')
        self.app.add_routes(routes)

    def run(self):
        if conf.adminEnabled:
            print("!!! WARNING !!!   ADMIN INTERFACE IS ENABLED!")
            print("This should NEVER be enabled during production!")
            print("If you are in production, SHUT IT DOWN IMMEDIATELY and change the config.")
        self.setup()
        web.run_app(self.app, host=self.host, port=self.port)
