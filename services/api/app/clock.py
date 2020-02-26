import os
import asyncio
import aiohttp

from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import lib.config
import lib.model
import lib.utils

from tortoise import Tortoise, run_async
from tortoise.exceptions import OperationalError


async def update():
    """
        Product update job.
        Add or update Product Offers from remote API.
    """

    # Iterate over all products stored in database
    _items = lib.model.Products.filter().order_by('id')
    for _item in await (_items.all()):

        # Create async aiohttp client session
        async with aiohttp.ClientSession(conn_timeout=1) as client:

            # Request header dictionary
            _headers = {
                "Bearer": lib.config.API_KEY
            }

            # Get all offers from remote API for actual product
            async with client.get(
                lib.config.API_URL + f'products/{_item.id}/offers',
                headers=_headers
            ) as resp:

                # Raise exception if wrong response
                if resp.status != 200:
                    raise OperationalError()

                # Iterate over Offers from API response
                for i in await resp.json():

                    # If Offer not in database, create
                    _offer, _created = await lib.model.Offers.get_or_create(
                        id=str(i["id"]),
                        product=_item
                    )

                    # Update offer data
                    _offer.price = i["price"]
                    _offer.items_in_stock = i["items_in_stock"]

                    # Save to database
                    await _offer.save()


async def init():

    # Database connection
    await Tortoise.init(db_url=lib.config.DATABASE_URL, modules={"model": ["lib.model"]})
    await Tortoise.generate_schemas()

    if not lib.config.API_KEY:
        # Obtain API_KEY if not specified
        lib.config.API_KEY = await lib.utils.getKey()


if __name__ == "__main__":

    # Init scheduler with one periodic job
    scheduler = AsyncIOScheduler()
    scheduler.add_job(update, "interval", minutes=1)
    scheduler.start()

    try:
        # Init async loop
        loop = asyncio.get_event_loop()
        loop.run_until_complete(init())
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
