from sanic.response import json
from sanic import Blueprint

bp = Blueprint('system', url_prefix='/system', version="v1")


@bp.get('/healthcheck')
async def healthcheck(request):
    return json({"status": "OK"})
