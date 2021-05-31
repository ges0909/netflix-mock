import fastapi
from fastapi import Depends

from netflix_mock.schemas.location import Location
from netflix_mock.schemas.weather_status import WeatherStatus
from netflix_mock.services.weather_service import get_weather

router = fastapi.APIRouter()


@router.get(path="", response_model=WeatherStatus)
async def do_i_need_an_umbrella(
    location: Location = Depends(),  # Location requires a POST body normally. To get its value as query use Depends().
):
    data = await get_weather(location=location)

    weather = data.get("weather", {})
    category = weather.get("category", "UNKNOWN")

    forecast = data.get("forecast", {})
    temp = forecast.get("temp", 0)

    bring = category.lower().strip() == "rain"

    return WeatherStatus(city=location.city, bring_umbrella=bring, temp=temp)
