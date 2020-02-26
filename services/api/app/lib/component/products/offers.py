from sanic.response import json
from sanic import Blueprint

import lib.model

bp = Blueprint('products.offers',
               url_prefix='/<productId:uuid>/offers',
               version="v1"
               )


@bp.get('/')
async def fetch(request, productId) -> list:
    """Return list of product offers"""

    _product = await lib.model.Products.get(id=productId).first()

    _items = lib.model.Offers.filter(product=_product).order_by('id')

    return json([_item.output() for _item in (await _items.all())])
