from fastapi import APIRouter, Request, Depends

from bytoken.org.common.http.Auth import getUserId
from bytoken.org.common.res.DataRes import DataRes
from bytoken.org.model.EventOrder import OrderParam
from bytoken.org.service import getEventOrderService

router = APIRouter()


@router.post(path="/postOrder")
async def postOrder(request: Request, param: OrderParam):
    getEventOrderService().post_order(getUserId(request), param)
    return DataRes.success()


@router.get(path="/orderPages")
async def orderPages(request: Request, param: OrderParam = Depends()):
    orderRecords = getEventOrderService().order_pages(getUserId(request), param)
    return DataRes.success(data=orderRecords)
