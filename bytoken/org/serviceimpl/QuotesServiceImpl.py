import asyncio
import decimal
import json
from datetime import datetime

import websockets

from bytoken.org.common.websockets.WebSocketClient import WebSocketClient
from bytoken.org.config import quote_websock_url
from bytoken.org.service.QuotesService import QuotesService

unsubscribe = {
    "method": "UNSUBSCRIBE",
    "params": [
        "btcusdt@aggTrade"
    ],
    "id": 1
}

subscribe = {
    "method": "SUBSCRIBE",
    "params": [
        "btcusdt@aggTrade"
    ],
    "id": 1
}


class QuotesServiceImpl(QuotesService, WebSocketClient):
    """行情管理类"""

    def __init__(self):
        super().__init__(quote_websock_url)
        self.prices = {"BTC": decimal.Decimal(0)}

    def getPrice(self, baseCoin=str):
        """获取最新价格"""
        return self.prices.get(baseCoin, decimal.Decimal('0'))  #

    async def receive(self):
        """接收实时数据"""
        try:
            async for message in self.websocket:
                data = json.loads(message)
                if 'pong' in data:
                    print("✅ 收到 Pong 响应:", data)
                    return
                self.prices['BTC'] = data.get("p", "N/A")
                print(
                    f"💹 最新价格更新: {self.prices['BTC']} | 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                from bytoken.org.service import getEventOrderService
                try:
                    getEventOrderService().close_orders(coin='BTC', price=self.prices.get("BTC"))
                except Exception as e:
                    print(e)
                # 等待 1 秒
                await asyncio.sleep(5)

        except Exception as e:
            print(f"❌ 接收错误: {e}")
            await super().reconnect()

    def init(self):
        asyncio.create_task(self.start())

    async def start(self):
        try:
            await self.connect()
            print("✅ WebSocket 连接成功")
            await self.send(json.dumps(subscribe))
            print("✅ 发送订阅成功")
            await self.receive()  # 开始接收数据
        except websockets.InvalidHandshake as e:
            print(f"❌ 握手失败: {e}")
            await self.reconnect()
            await self.send(json.dumps(subscribe))
            print("✅ 发送订阅成功")
        except websockets.WebSocketException as e:
            print(f"❌ WebSocket 异常: {e}")
            await self.reconnect()
            await self.send(json.dumps(subscribe))
            print("✅ 发送订阅成功")
        except Exception as e:
            print(f"❌ 连接失败: {e}")
            await self.reconnect()
            await self.send(json.dumps(subscribe))
            print("✅ 发送订阅成功")

    async def exit(self):
        """关闭 WebSocket 连接"""
        try:
            await self.send(json.dumps(unsubscribe))
            print("✅ 关闭订阅成功")
            await super().close()
            print("🔌 WebSocket 已关闭")
        except Exception as e:
            print(f"❌ 关闭连接失败: {e}")
