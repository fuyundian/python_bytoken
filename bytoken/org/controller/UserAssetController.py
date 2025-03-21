from fastapi import APIRouter, Request

from bytoken.org.common.http.Auth import getUserId
from bytoken.org.common.res.DataRes import DataRes
from bytoken.org.model.UserAsset import UserAssetParam
from bytoken.org.service import getUserAssetService

router = APIRouter()


@router.get(path="/getUserAsset", response_model=DataRes)
async def getUserAsset(request: Request, param: UserAssetParam) -> DataRes:
    asset = getUserAssetService().getUserAsset(getUserId(request), param.coin)
    return DataRes.success(asset)


@router.post(path="/deposition", response_model=DataRes)
async def getUserAsset(request: Request, param: UserAssetParam) -> DataRes:
    asset = getUserAssetService().deposition(getUserId(request), param.coin)
    return DataRes.success(asset)
