from fastapi import APIRouter, Request

from bytoken.org.common.http.Auth import getUserId
from bytoken.org.common.res.DataRes import DataRes
from bytoken.org.model.EventOrder import OrderParam
from bytoken.org.service import getEventOrderService

router = APIRouter()


@router.post(path="/postOrder")
async def postOrder(request: Request, param: OrderParam):
    getEventOrderService().postOrder(getUserId(request), param)
    return DataRes.success()
