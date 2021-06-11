import pytest
from src.db import get_value


@pytest.mark.asyncio
@pytest.mark.parametrize(("currency_from", "currency_to", "result"), [
    ("RUB", "USD", 60),
    ("RUB", "EUR", 80),
])
async def test_get_currency(currency_from, currency_to, result):
    key = f"{currency_from}-{currency_to}"
    value = await get_value(key)
    assert value == result
