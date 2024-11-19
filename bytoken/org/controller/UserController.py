from fastapi import APIRouter

from bytoken.org.common.res.DataRes import DataRes
from bytoken.org.service import getUserService

router = APIRouter()


@router.get("/getUserById")
async def getUserById(id: int):
    user = getUserService().getUserById(id)
    return DataRes.success(data=user)
