# pylint: disable=E0401,E0611
import os
import logging

from sanic import Sanic, response
from sanic.response import json
from sanic.exceptions import abort, NotFound, Unauthorized, MethodNotSupported

import lib.config

import lib.component.system

logging.basicConfig(level=logging.DEBUG)

app = Sanic(__name__)

app.blueprint(lib.component.system.bp)


@app.listener('before_server_start')
async def before_server_start(app, loop) -> None:
    print("START")


@app.listener('after_server_stop')
async def after_server_stop(app, loop) -> None:
    print("END")


@app.exception(Unauthorized)
async def error401(request, exception):
    """
        Catch all 401 errors and transform response to json.
    """
    return json({
        'status': 401,
        'statusMessage': "Unauthorized"
    }, status=401)


@app.exception(NotFound)
async def error404(request, exception):
    """
        Catch all 404 errors and transform response to json.
    """
    return json({
        'status': 404,
        'statusMessage': str(exception)
    }, status=404)


@app.exception(MethodNotSupported)
async def error405(request, exception):
    """
        Catch all 405 errors and transform response to json.
    """
    return json({
        'status': 405,
        'statusMessage': str(exception)
    }, status=405)

if __name__ == "__main__":

    if lib.config.DEBUG:
        _workers = 1
    else:
        _workers = os.cpu_count()

    app.run(
        host=lib.config.HOST,
        port=lib.config.PORT,
        debug=lib.config.DEBUG,
        access_log=lib.config.DEBUG,
        workers=_workers
    )
