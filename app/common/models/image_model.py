from pydantic import Field
from fastapi_utils.api_model import APIModel

class ImageModel(APIModel):
    uid: str | None = Field(None)
    product_id: str = Field(..., max_length=25)
    url: str = Field(..., max_length=400)
    descritpion: str | None = Field(None, max_length=300)