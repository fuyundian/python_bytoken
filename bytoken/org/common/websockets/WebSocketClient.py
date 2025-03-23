import abc
import asyncio

import websockets


class WebSocketClient:
    def __init__(self, url: str):
        self.websocket = None
        self.ping_interval = 10  # 心跳间隔
        self.url = url  # 心跳间隔

    async def connect(self):
        """建立 WebSocket 连接"""
        try:
            self.websocket = await websockets.connect(self.url)
            print("✅ 已连接到 Binance WebSocket")
            asyncio.create_task(self.ping())  # 启动心跳任务
        except Exception as e:
            print(f"❌ WebSocket 连接失败: {e}")

    async def ping(self):
        """发送心跳包"""
        try:
            while True:
                if self.websocket and self.websocket.open:
                    await self.websocket.ping()
                    print("📡 发送 Ping 保持连接")
                await asyncio.sleep(self.ping_interval)
        except Exception as e:
            print(f"⚠️ Ping 发送失败: {e}")


    @abc.abstractmethod
    async def receive(self):
        pass

    async def reconnect(self):
        if self.websocket is None or self.websocket.open is False:
            await self.connect()
            await self.receive()

    async def close(self):
        if self.websocket is None or self.websocket.open is False:
            return
        await self.websocket.exit()
