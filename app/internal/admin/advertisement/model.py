from typing import Optional

from fastapi_utils.api_model import APIModel

import datetime

class AdvertisementBase(APIModel):
    title: Optional[str]
    description: str

class AdvertisementCreate(AdvertisementBase):
    hyperlink: str

class AdvertisementModel(AdvertisementCreate):
    uid: Optional[str]
    time_ago: Optional[datetime.datetime]
    is_active: Optional[bool]