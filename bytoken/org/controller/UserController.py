from typing import Optional, Annotated

from fastapi import APIRouter, Depends, Request

from bytoken.org.common.http import Anonymous
from bytoken.org.common.http.Anonymous import getAnonymous
from bytoken.org.common.http.Auth import getUserId
from bytoken.org.common.res.DataRes import DataRes
from bytoken.org.model.User import UserLoginParam
from bytoken.org.service import getUserService

router = APIRouter()


@router.get("/getCurrentUser")
async def getUserById(request: Request):
    user = getUserService().getUserById(getUserId(request))
    return DataRes.success(data=user)


@router.post("/login")
async def login(param: UserLoginParam, anon: Annotated[Anonymous, Depends(getAnonymous)]):
    token = getUserService().login(param)
    return DataRes.success(data=token)
