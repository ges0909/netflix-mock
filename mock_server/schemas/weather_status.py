from pydantic import BaseModel


class WeatherStatus(BaseModel):
    city: str
    bring_umbrealla: bool
    temp: float
