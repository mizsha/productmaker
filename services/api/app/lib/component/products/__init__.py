import aiohttp

from tortoise.exceptions import OperationalError
from tortoise.transactions import atomic, in_transaction

from sanic_validation import validate_json
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


@bp_index.post('/')
@validate_json(ProductForm, clean=True)
async def create(request, valid_json) -> dict:

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


@bp_index.get('/')
async def fetch(request) -> list:

    _items = lib.model.Products.filter().order_by('id')

    return json([_item.output() for _item in (await _items.all())])


@bp_index.get('/<productId:uuid>')
async def get(request, productId) -> dict:

    _item = await lib.model.Products.get(id=productId).first()

    return json(_item.output())
