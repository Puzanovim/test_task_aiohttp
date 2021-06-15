from typing import List
from aiohttp import web
from src.app import app
from src.db import set_value, get_value, clean_db
from src.schemas import ExchangeRate

routes = web.RouteTableDef()


@routes.get('/')
async def get_handler(request):
    return web.Response(text=f"HELLO")


@routes.get('/convert')
async def get_convert_currency(request):
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
async def post_exchange_rate(request):
    data = request.post()
    print(data)
    merge = int(request.query["merge"])
    if merge == 0:
        await clean_db()
    elif merge != 1:
        raise web.HTTPException()
    result = []
    for data_item in data:
        key = f"{data_item.currency_from}-{data_item.currency_to}"
        value = data_item.value
        result.append({"key": key, "value": value})
        await set_value(key, value)
    return web.json_response({"result": result})


app.add_routes(routes)
