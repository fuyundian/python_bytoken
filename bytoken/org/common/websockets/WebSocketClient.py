import abc

import websockets


class WebSocketClient:
    def __init__(self, url: str):
        self.websocket = None
        self.ping_interval = 20
        self.url = url

    async def connect(self):
        """建立 WebSocket 连接"""
        try:
            self.websocket = await websockets.connect(uri=self.url, ping_interval=self.ping_interval, ping_timeout=100)
            print("✅ 已连接到  WebSocket")
            # await asyncio.create_task(self.ping_pong())  # 启动心跳任务
        except Exception as e:
            print(f"❌ WebSocket 连接失败: {e}")
            await self.reconnect()

    @abc.abstractmethod
    async def receive(self):
        pass

    @abc.abstractmethod
    async def send(self, data):
        pass

    async def reconnect(self):
        if self.websocket is None or self.websocket.open is False:
            await self.connect()
            await self.receive()

    async def close(self):
        """关闭 WebSocket 连接"""
        try:
            if self.websocket is None or not self.websocket.open:
                print("连接已经关闭或不存在.")
                return

            await self.websocket.close()
            print("WebSocket 连接已关闭.")
        except Exception as e:
            print(f"关闭连接失败: {e}")
