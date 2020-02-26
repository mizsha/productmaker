import hashlib
import aiohttp

import tortoise.exceptions
from tortoise.transactions import atomic, in_transaction

import lib.config
import lib.model


@atomic()
async def getKey():

    """
        If not API key specified in config or 
        environment variable, get new one and store to database for next run.
    """

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
