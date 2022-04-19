from pydantic import Field
from fastapi_utils.api_model import APIModel

class BrandModel(APIModel):
    code: str | None = Field(None)
    name: str = Field(..., max_length=50)
    logo: str = Field(..., max_length=400)