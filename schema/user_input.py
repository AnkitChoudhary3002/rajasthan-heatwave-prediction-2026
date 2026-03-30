from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class CityInput(BaseModel):
        city: str = Field(..., description="Name of the city to fetch weather data for", example="Jaipur")
        @field_validator("city")
        def validate_city(cls, v):
            if not v.replace(' ', '').isalpha():
                raise ValueError("City name must contain only letters")
            return v.lower().title()

class WeatherInput(BaseModel):
    date: str = Field(..., example="15/06/2026")
    temperature: float = Field(None, description="Temperature in degrees Celsius", example=25.0)
    humidity: float = Field(None, description="Relative humidity in percentage", example=30.0)
    windspeed: float = Field(None, description="Wind speed in km/h", example=15.0)
    precip: float = Field(None, description="Precipitation in mm", example=0.0)
    cloudcover: float = Field(None, description="Cloud cover in percentage", example=10.0)

    @field_validator("date")
    def validate_date(cls, v):
        try:
            datetime.strptime(v, "%d/%m/%Y")
        except ValueError:
            raise ValueError("Date must be in dd/mm/yyyy format")
        return v
    
class HeatIndexInput(BaseModel):
    temperature: float = Field(..., description="Temperature in degrees Celsius", example=25.0)
    humidity: float = Field(..., description="Relative humidity in percentage", example=30.0)