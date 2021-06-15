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
    amount = float(request.query["amount"])
    key = f"{currency_from}-{currency_to}"
    value = await get_value(key)
    result = amount / value
    data = {"result": result}
    return web.json_response(data)


async def get_value_of_field(data: str, field: str, integer_type: bool = False):
    index = data.find(field)
    if integer_type:
        start = index + len(field) + 2
    else:
        start = index + len(field) + 3
    end = data.find("\"", start)
    result = data[start:end:]
    return result


@routes.post('/database')
async def post_exchange_rate(request):
    merge = int(request.query["merge"])
    data = await request.post()
    if merge == 0:
        await clean_db()
    elif merge != 1:
        raise web.HTTPException()
    result = []
    for data_item in data:
        currency_from = await get_value_of_field(data[data_item], "currency_from")
        currency_to = await get_value_of_field(data[data_item], "currency_to")
        value = float(await get_value_of_field(data[data_item], "value", True))
        exchange_rate = ExchangeRate(currency_from=currency_from, currency_to=currency_to, value=value)
        key = f"{exchange_rate.currency_from}-{exchange_rate.currency_to}"
        value = exchange_rate.value
        result.append({"key": key, "value": value})
        await set_value(key, value)
    return web.json_response({"result": result})


app.add_routes(routes)
