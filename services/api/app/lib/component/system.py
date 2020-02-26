from sanic.response import json
from sanic import Blueprint

bp = Blueprint('system', url_prefix='/system', version="v1")


@bp.get('/healthcheck')
async def healthcheck(request) -> dict:
    """
        Healthcheck method, always return status: OK
    """
    return json({"status": "OK"})
