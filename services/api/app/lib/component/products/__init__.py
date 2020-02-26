import aiohttp

from tortoise.exceptions import OperationalError
from tortoise.transactions import atomic, in_transaction

from sanic_validation import validate_json
from sanic_openapi import doc
from sanic.exceptions import abort
from sanic.response import json
from sanic import Blueprint

import lib.model

from . import offers

bp_index = Blueprint('products', version="v1")

bp = Blueprint.group(
    bp_index,
    offers.bp,
    url_prefix='/products'
)

ProductForm = {
    'name': {'type': 'string', 'required': True},
    'description': {'type': 'string', 'required': True},
}


class ProductOutput:
    id = doc.String("Product UUID.")
    name = doc.String("Product name.")
    description = doc.String("Product description.")


@bp_index.post('/')
@doc.consumes(
    doc.JsonBody(
        {
            "name": doc.String("Product name."),
            "description": doc.String("Product description."),
        }
    ),
    location="body", content_type="application/json"
)
@doc.produces(ProductOutput)
@doc.response(201, ProductOutput, description="Product created")
@doc.summary("Create new product")
@validate_json(ProductForm, clean=True)
async def create(request, valid_json) -> dict:
    """Create product method"""

    @atomic()
    async def createProduct(data):

        async with aiohttp.ClientSession(conn_timeout=1) as client:

            _product = await lib.model.Products.create(
                **data
            )

            _headers = {
                "Bearer": lib.config.API_KEY
            }

            async with client.post(
                lib.config.API_URL + 'products/register',
                json=_product.output(),
                headers=_headers
            ) as resp:

                if resp.status != 201:
                    raise OperationalError()

        return _product

    try:
        # Create product, in database transaction, if fails, nothing stored
        _item = await createProduct(valid_json)
    except:
        raise OperationalError()

    return json(_item.output(), status=201)


@bp_index.get('/')
@doc.produces([ProductOutput])
@doc.summary("Fetch all products")
async def fetch(request) -> list:
    """Return list of products"""

    _items = lib.model.Products.filter().order_by('id')

    return json([_item.output() for _item in (await _items.all())])


@bp_index.get('/<productId:uuid>')
@doc.produces(ProductOutput)
@doc.summary("Get product detail")
async def get(request, productId) -> dict:
    """Return specified product"""

    _item = await lib.model.Products.get(id=productId).first()

    return json(_item.output())


@bp_index.patch('/<productId:uuid>')
@doc.consumes(
    doc.JsonBody(
        {
            "name": doc.String("Product name."),
            "description": doc.String("Product description."),
        }
    ),
    location="body", content_type="application/json"
)
@doc.produces(ProductOutput)
@doc.summary("Update product values")
@validate_json(ProductForm, clean=True)
async def patch(request, productId, valid_json) -> dict:
    """Patch and return updated specified product"""

    _item = await lib.model.Products.get(id=productId).first()
    if _item:
        for key, value in valid_json.items():
            setattr(_item, key, value)
        await _item.save()

    return json(_item.output())


@bp_index.delete('/<productId:uuid>')
@doc.summary("Delete product")
async def delete(request, productId) -> dict:
    """Delete specified product and return blank dict if success"""

    _item = await lib.model.Products.get(id=productId).first()
    await _item.delete()

    return json({})
