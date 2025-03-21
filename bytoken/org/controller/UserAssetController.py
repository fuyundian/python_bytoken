from fastapi import APIRouter, Request, Depends

from bytoken.org.common.http.Auth import getUserId
from bytoken.org.common.res.DataRes import DataRes
from bytoken.org.model.UserAsset import UserAssetParam
from bytoken.org.service import getUserAssetService

router = APIRouter()


@router.get(path="/getUserAsset")
async def getUserAsset(request: Request, param: UserAssetParam = Depends()):
    asset = getUserAssetService().getUserAsset(getUserId(request), param.coin)
    return DataRes.success(asset)


@router.post(path="/deposition")
async def getUserAsset(request: Request, param: UserAssetParam):
    getUserAssetService().deposition(getUserId(request), param)
    return DataRes.success(data=None)
