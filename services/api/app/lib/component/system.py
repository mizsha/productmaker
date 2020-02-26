from sanic.response import json
from sanic import Blueprint

from sanic_openapi import doc

bp = Blueprint('system', url_prefix='/system', version="v1")


@bp.get('/healthcheck')
@doc.summary("Healthcheck method")
@doc.description('Always return status: OK.')
async def healthcheck(request) -> dict:

    return json({"status": "OK"})
