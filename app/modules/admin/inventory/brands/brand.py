from fastapi import APIRouter, Depends, Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas import Brand
from app.core.dependency import get_session
from app.core.http_responses import HttpResponseBadRequest
from app.common.models import BrandModel

router = APIRouter()

@router.get('/')
async def read_brands():
    pass

@router.get('/{code}')
async def read_brand(
    code: str = Path(...)
):
    pass

@router.post('/', response_model=BrandModel, status_code=201)
async def add_brand(
    brand: BrandModel,
    session: AsyncSession = Depends(get_session)
):
    existented_brand: Brand = await session.execute(
        select(Brand).where(Brand.name == brand.name)
    )
    if not existented_brand:
        new_brand: Brand = Brand(
            **brand.dict(exclude_unset=True)
        )
        await session.add(new_brand)
        await session.commit()
        return new_brand
    return HttpResponseBadRequest({
        "status": "fail",
        "data": {
            "message": "La marca ya existe"
        }
    }).response()

@router.put('/{code}')
async def update_brand(
    code: str = Path(...)
):
    pass

@router.patch('/{code}')
async def edit_brand(
    code: str = Path(...)
):
    pass

@router.delete('/{code}')
async def delete_brand(
    code: str = Path(...)
):
    pass