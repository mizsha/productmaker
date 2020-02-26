import aiohttp

from sanic import Blueprint
from sanic.response import json
from sanic.exceptions import abort
from sanic_validation import validate_json

from tortoise.transactions import atomic, in_transaction
from tortoise.exceptions import OperationalError

import lib.model

bp = Blueprint('products', url_prefix='/products', version="v1")

ProductForm = {
    'name': {'type': 'string', 'required': True},
    'description': {'type': 'string', 'required': True},
}


@bp.post('/')
@validate_json(ProductForm, clean=True)
async def create(request, valid_json):

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
        _item = await createProduct(valid_json)
    except:
        raise OperationalError()

    return json(_item.output(), status=201)


@bp.get('/')
async def fetch(request):

    _items = lib.model.Products.filter().order_by('id')

    return json([_item.output() for _item in (await _items.all())])


@bp.get('/<productId:uuid>')
async def get(request, productId):

    _item = await lib.model.Products.get(id=productId).first()

    return json(_item.output())
