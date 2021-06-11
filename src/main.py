from .routers import app
from aiohttp_swagger import *


def init_func(argv):
    setup_swagger(app, swagger_url="/docs", ui_version=3, swagger_from_file="src/swagger.yaml")
    return app
