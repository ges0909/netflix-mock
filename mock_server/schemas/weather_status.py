from pydantic import BaseModel


class WeatherStatus(BaseModel):
    city: str
    bring_umbrella: bool
    temp: float
