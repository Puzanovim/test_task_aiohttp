from typing import List

from aiohttp import web
from .app import app
from .db import set_value, get_value, clean_db
from .schemas import ExchangeRate

routes = web.RouteTableDef()


@routes.get('/')
async def get_handler(request):
    return web.Response(text=f"HELLO")


@routes.get('/convert')
async def get_handler(request):
    """
    ---
    description: This end-point allow to convert currency.
    tags:
    - Convert
    produces:
    - text/plain
    responses:
        "200":
            description: successful operation. Return result in JSON
        "405":
            description: invalid HTTP Method
    """
    currency_from = request.query["from"]
    currency_to = request.query["to"]
    amount = int(request.query["amount"])
    key = f"{currency_from}-{currency_to}"
    value = await get_value(key)
    result = amount / value
    data = {"result": result}
    print(f"{amount} convert from {currency_from} to {currency_to}")
    return web.json_response(data)


@routes.post('/database')
async def post_handler(request, data: List[ExchangeRate]):
    """
    ---
    description: This end-point allow to test that service is up.
    tags:
    - Health check
    produces:
    - text/plain
    responses:
        "200":
            description: successful operation. Return "pong" text
        "405":
            description: invalid HTTP Method
    """
    merge = request.query["merge"]
    if merge == 0:
        await clean_db()
    elif merge != 1:
        raise web.HTTPMethodNotAllowed()
    for data_item in data:
        key = f"{data_item.currency_from}-{data_item.currency_to}"
        value = data_item.value
        await set_value(key, value)


app.add_routes(routes)
