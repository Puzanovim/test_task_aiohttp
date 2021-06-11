import pytest
from src.db import set_value, get_value


@pytest.mark.asyncio
@pytest.mark.parametrize(("currency_from", "currency_to", "value"), [
    ("RUB", "USD", 61),
    ("RUB", "EUR", 85),
])
async def test_add_exchange_rate(currency_from, currency_to, value):
    key = f"{currency_from}-{currency_to}"
    await set_value(key, value)
    result = await get_value(key)
    assert result == value
