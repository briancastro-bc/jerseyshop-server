import datetime
from pydantic import Field
from fastapi_utils.api_model import APIModel

class ColorModel(APIModel):
    uid: str | None = Field(None)
    name: str = Field(..., max_length=30)
    value: str = Field(..., max_length=10)
    created_at: datetime.datetime | None = Field(None)