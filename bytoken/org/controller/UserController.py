from typing import Optional

from fastapi import APIRouter, Depends

from bytoken.org.common.http import Anonymous
from bytoken.org.common.res.DataRes import DataRes
from bytoken.org.model.User import UserLoginParam
from bytoken.org.service import getUserService

router = APIRouter()


@router.get("/getCurrentUser")
async def getUserById(id: int):
    user = getUserService().getUserById(id)
    return DataRes.success(data=user)


@router.post("/login")
async def login(param: UserLoginParam, no_auth: Optional[Anonymous] = Depends(lambda: Anonymous)):
    token = getUserService().login(param)
    return DataRes.success(data=token)
