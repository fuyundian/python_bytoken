from typing import Annotated

from fastapi import APIRouter, Depends, Request

from bytoken.org.common.http import Anonymous
from bytoken.org.common.http.Anonymous import getAnonymous
from bytoken.org.common.http.Auth import getUserId
from bytoken.org.common.res.DataRes import DataRes
from bytoken.org.model.User import UserLoginParam
from bytoken.org.service import getUserAssetService

router = APIRouter()


@router.get(path="/getCurrentUser", response_model=DataRes)
async def getUserById(request: Request) -> DataRes:
    user = getUserAssetService().getUserById(getUserId(request))
    return DataRes.success(data=user)


@router.post(path="/login", response_model=DataRes)
async def login(param: UserLoginParam, anon: Annotated[Anonymous, Depends(getAnonymous)]) -> DataRes:
    token = getUserAssetService().login(param)
    return DataRes.success(data=token)
