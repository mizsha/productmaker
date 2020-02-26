# pylint: disable=E0401,E0611
import logging
import hashlib
import aiohttp

import aiohttp.client_exceptions

from sanic import Sanic, response
from sanic.response import json
from sanic.exceptions import abort, NotFound, Unauthorized, MethodNotSupported, InvalidUsage

from sanic_cors import CORS
from sanic_openapi import swagger_blueprint

from tortoise.transactions import atomic, in_transaction
from tortoise.contrib.sanic import register_tortoise
import tortoise.exceptions

# Import app config and models
import lib.config
import lib.model

# Import app endpoints
import lib.component.system
import lib.component.products

# Init Sanic app
app = Sanic(__name__)

app.config.API_VERSION = lib.config.VERSION
app.config.API_TITLE = lib.config.TITLE
app.config.API_BASEPATH = "/"
app.config.API_CONTACT_EMAIL = 'info@{0}'.format(lib.config.DOMAIN)


# CORS module automagic
CORS(app)

# Expose Sanic Swagger endpoints (/swagger/)
app.blueprint(swagger_blueprint)

# Expose app endpoints
app.blueprint(lib.component.system.bp)
app.blueprint(lib.component.products.bp)

# Connect to database
register_tortoise(
    app, db_url=lib.config.DATABASE_URL, modules={"model": ["lib.model"]}, generate_schemas=True
)


@app.listener('before_server_start')
async def before_server_start(app, loop) -> None:
    """
        If not API key specified in config default or 
        environment variable, get new one and store to database for next run.
    """
    if not lib.config.API_KEY:

        @atomic()
        async def getKey():

            _hash = hashlib.md5(lib.config.API_URL.encode('utf-8')).hexdigest()
            _key, _created = await lib.model.Keys.get_or_create(hash=_hash)
            if _created:
                async with aiohttp.ClientSession(conn_timeout=1) as client:
                    async with client.post(lib.config.API_URL + '/auth') as resp:
                        if resp.status != 201:
                            raise tortoise.exceptions.OperationalError()

                        _key.key = (await resp.json())["access_token"]
                        await _key.save()

            return _key.key

        lib.config.API_KEY = await getKey()


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
@app.exception(tortoise.exceptions.DoesNotExist)
async def error404(request, exception):
    """
        Catch all 404 errors and transform response to json.
    """
    return json({
        'status': 404,
        'statusMessage': str(exception)
    }, status=404)


@app.exception(tortoise.exceptions.OperationalError)
@app.exception(aiohttp.client_exceptions.ServerTimeoutError)
async def error504(request, exception):
    """
        Catch all 504 errors and transform response to json.
    """
    return json({
        'status': 504,
        'statusMessage': str(exception)
    }, status=504)


@app.exception(MethodNotSupported)
@app.exception(InvalidUsage)
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
        app.run(
            host=lib.config.HOST,
            port=lib.config.PORT,
            debug=True,
            access_log=True,
            workers=1
        )
    else:
        app.run(
            host=lib.config.HOST,
            port=lib.config.PORT,
            debug=False,
            access_log=False
        )
