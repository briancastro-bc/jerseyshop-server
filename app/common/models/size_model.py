import datetime
from pydantic import Field
from fastapi_utils.api_model import APIModel

class SizeModel(APIModel):
    uid: str | None = Field(None)
    value: str = Field(..., max_length=50)
    created_at: datetime.datetime | None = Field(None)