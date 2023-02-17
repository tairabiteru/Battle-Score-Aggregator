from functools import partial
from sanic.worker.loader import AppLoader
from sanic import Sanic
from dash.core import Dash, logger
from dash.conf import conf

if __name__ == "__main__":
    loader = AppLoader(factory=partial(Dash.create_app, "BSA"))
    app = loader.load()
    app.prepare(host=conf.host, port=conf.port)

    if conf.enable_admin_interface:
        logger.warning("!!! WARNING !!! ~~ ADMIN INTERFACE IS ENABLED! ~~ !!! WARNING !!!")
        logger.warning("The admin interface should NEVER be enabled during production!")
        logger.warning("If you are in production, shut down IMMEDIATELY and change the config.")

    try:
        Sanic.serve(primary=app, app_loader=loader)
    except OSError as e:
        if e.errno == 10057:
            logger.warning("Recieved call to shut down. Bye!")
