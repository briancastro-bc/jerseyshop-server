from typing import Optional

from fastapi_utils.api_model import APIModel

from app.core.schemas.profile_schema import Gender

class ProfileBase(APIModel):
    pass

class ProfileCreate(ProfileBase):
    phone_number: str
    gender: Optional[Gender]

class ProfileModel(ProfileCreate):
    uid: str
    photo: Optional[str]