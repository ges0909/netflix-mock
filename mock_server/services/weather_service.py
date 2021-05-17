import httpx

from mock_server.schemas.location import Location


async def get_weather(location: Location):
    url = f"https://weather.talkpython.fm/api/weather?city={location.city}&country={location.country}&units=metric"

    if location.state:
        url += f"&state={location.state}"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url=url)
        resp.raise_for_status()
        return resp.json()
