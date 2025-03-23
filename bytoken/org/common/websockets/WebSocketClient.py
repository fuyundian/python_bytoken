import abc

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
            print("✅ 已连接到  WebSocket")
            # asyncio.create_task(self.ping())  # 启动心跳任务
        except Exception as e:
            print(f"❌ WebSocket 连接失败: {e}")
            await self.reconnect()

    @abc.abstractmethod
    async def receive(self):
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
