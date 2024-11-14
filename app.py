from bytoken.org.common.http import app
from bytoken.org.common.res.DataRes import DataRes
from bytoken.org.config import server_host, server_port
from bytoken.org.service import getUserService


@app.get("/getUserById")
async def getUserById(id: int):
    user = getUserService().getUserById(id)
    return DataRes.success(data=user)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=server_host, port=server_port)
