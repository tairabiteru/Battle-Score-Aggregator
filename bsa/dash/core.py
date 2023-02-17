"""
This module defines the dashboard.

The dashboard is effectively the web interface that the user interacts with.
This module defines the configuration of the dashboard from conf.py, then
sets the routes from routes.py.
"""

from .conf import conf
from .filters import jinjafilters
from .routes import routes
from orm.judge import Judge

import coloredlogs
import jinja2
import logging
import sanic
import sanic_session
import sanic_jinja2


logger = logging.getLogger("main")
coloredlogs.install(
    level='DEBUG',
    logger=logger,
    fmt="[%(asctime)s][%(levelname)s] %(message)s"
)


class Dash:
    @staticmethod
    def create_app(name):
        app = sanic.Sanic("BSA")
        app.static("/static", conf.static_directory)

        loader = jinja2.FileSystemLoader(conf.template_directory)
        sanic_session.Session(
            app,
            interface=sanic_session.InMemorySessionInterface()
        )
        app.ctx.jinja = sanic_jinja2.SanicJinja2(app, loader=loader)

        for jinjafilter in jinjafilters:
            app.ctx.jinja.add_end(jinjafilter.__name__, jinjafilter, scope="filters")
        
        app.blueprint(routes)

        judges = Judge.obtainall()
        for judge in judges:
            judge.helpFlag = False
            judge.save()

        return app

    # @classmethod
    # def run(cls):
    #     if conf.enable_admin_interface:
    #         logger.warning("!!! WARNING !!! ~~ ADMIN INTERFACE IS ENABLED! ~~ !!! WARNING !!!")
    #         logger.warning("The admin interface should NEVER be enabled during production!")
    #         logger.warning("If you are in production, shut down IMMEDIATELY and change the config.")

    #     dash = cls()
    #     dash.app.run(
    #         host=conf.host,
    #         port=conf.port,
    #         access_log=False,
    #         debug=False
    #     )
