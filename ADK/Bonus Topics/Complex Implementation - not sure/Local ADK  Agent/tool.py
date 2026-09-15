from dotenv import load_dotenv
load_dotenv()
import os
import httpx
import asyncio

BASE_URL = "https://v6.exchangerate-api.com/v6"

async def convert_currency(base_currency: str, target_currency: str, amount: float = 1.0) -> dict:
    """Convert an amount from one currency to another using live exchange rates.

    Args:
        base_currency: ISO 4217 code to convert from, e.g. "USD".
        target_currency: ISO 4217 code to convert to, e.g. "INR".
        amount: Amount in base_currency to convert. Defaults to 1.0.

    Returns:
        dict with conversion_rate, converted_amount, and last update time,
        or an "error" key if the request failed.
    """
    api_key = os.environ.get("EXCHANGE_RATE_API_KEY")
    if not api_key:
        return {"error": "EXCHANGE_RATE_API_KEY is not set."}

    base_currency = base_currency.upper().strip()
    target_currency = target_currency.upper().strip()
    url = f"{BASE_URL}/{api_key}/pair/{base_currency}/{target_currency}/{amount}"

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
    except httpx.HTTPError as e:
        return {"error": f"Request failed: {e}"}

    if data.get("result") != "success":
        return {"error": data.get("error-type", "unknown error")}

    return {
        "base_currency": data["base_code"],
        "target_currency": data["target_code"],
        "conversion_rate": data["conversion_rate"],
        "amount": amount,
        "converted_amount": data.get("conversion_result", data["conversion_rate"] * amount),
        "last_updated_utc": data["time_last_update_utc"],
    }