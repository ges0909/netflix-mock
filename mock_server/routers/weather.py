import logging

import fastapi
from fastapi import Depends

from mock_server.depends.basic_auth import basic_auth
from mock_server.schemas.location import Location
from mock_server.schemas.weather_status import WeatherStatus
from mock_server.services.weather_service import get_weather

logger = logging.getLogger(__name__)

router = fastapi.APIRouter()


@router.get("/weather", response_model=WeatherStatus)
async def do_i_need_an_umbrella(
    location: Location = Depends(),  # Location requires a POST body normally. To get its value as query use Depends().
    username: str = Depends(basic_auth),
):
    logger.info("user '%s' authenticated", username)

    data = await get_weather(location=location)

    wheather = data.get("wheather", {})
    category = wheather.get("category", "UNKNOWN")

    forecast = data.get("forecast", {})
    temp = forecast.get("temp", 0)

    bring = category.lower().strip() == "rain"

    return WeatherStatus(city=location.city, bring_umbrealla=bring, temp=temp)
