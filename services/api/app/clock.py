import os
import asyncio
import aiohttp

from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import lib.config
import lib.model

from tortoise import Tortoise, run_async
from tortoise.exceptions import OperationalError


async def update():

    _items = lib.model.Products.filter().order_by('id')
    for _item in await (_items.all()):

        async with aiohttp.ClientSession(conn_timeout=1) as client:

            _headers = {
                "Bearer": lib.config.API_KEY
            }

            async with client.get(
                lib.config.API_URL + f'products/{_item.id}/offers',
                headers=_headers
            ) as resp:

                if resp.status != 200:
                    raise OperationalError()

                for i in await resp.json():
                    _offer, _status = await lib.model.Offers.get_or_create(
                        id=str(i["id"]),
                        product=_item
                    )
                    _offer.price = i["price"]
                    _offer.items_in_stock = i["items_in_stock"]
                    await _offer.save()


async def init():
    await Tortoise.init(db_url=lib.config.DATABASE_URL, modules={"model": ["lib.model"]})


if __name__ == "__main__":

    scheduler = AsyncIOScheduler()
    scheduler.add_job(update, "interval", minutes=1)
    scheduler.start()

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(init())
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
