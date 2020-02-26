from sanic_openapi import doc
from sanic.response import json
from sanic import Blueprint

import lib.model

bp = Blueprint('products.offers',
               url_prefix='/<productId:uuid>/offers',
               version="v1"
               )


class OfferOutput:
    id = doc.String("Offer ID.")
    product = doc.String("Product UUID.")
    price = doc.String("Offer price.")
    items_in_stock = doc.String("Product items in stock.")
    createdAt = doc.DateTime("Datetime of item creation.")
    updatedAt = doc.DateTime("Datetime of item last update.")


@bp.get('/')
@doc.produces([OfferOutput])
@doc.summary("Fetch all Product Offers")
async def fetch(request, productId) -> list:
    """Return list of product offers"""

    _product = await lib.model.Products.get(id=productId).first()

    _items = lib.model.Offers.filter(product=_product).order_by('id')

    return json([_item.output() for _item in (await _items.all())])
