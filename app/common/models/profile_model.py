from fastapi_utils.api_model import APIModel

from app.core.schemas import Gender

class ProfileBase(APIModel):
    pass

class ProfileCreate(ProfileBase):
    phone_number: str
    gender: Gender|None

class ProfileModel(ProfileCreate):
    uid: str
    photo: str|None