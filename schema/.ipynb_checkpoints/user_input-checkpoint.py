from datetime import datetime

from pydantic import BaseModel, Field

try:
    # Pydantic v2
    from pydantic import field_validator as _date_validator
except ImportError:  # pragma: no cover - compatibility fallback
    # Pydantic v1
    from pydantic import validator as _date_validator


class WeatherInput(BaseModel):
    date: str = Field(..., examples=["15/06/2026"])
    humidity: float = Field(..., examples=[30.0])
    windspeed: float = Field(..., examples=[15.0])
    precip: float = Field(..., examples=[0.0])
    cloudcover: float = Field(..., examples=[10.0])

    @_date_validator("date")
    def validate_date(cls, value: str) -> str:
        try:
            datetime.strptime(value, "%d/%m/%Y")
        except ValueError as exc:
            raise ValueError("Date must be in dd/mm/yyyy format") from exc
        return value
from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class WeatherInput(BaseModel):
    date: str = Field(..., example="15/06/2026")
    humidity: float = Field(..., example=30.0)
    windspeed: float = Field(..., example=15.0)
    precip: float = Field(..., example=0.0)
    cloudcover: float = Field(..., example=10.0)

    @field_validator("date")
    def validate_date(cls, v):
        try:
            datetime.strptime(v, "%d/%m/%Y")
        except ValueError:
            raise ValueError("Date must be in dd/mm/yyyy format")
        return v