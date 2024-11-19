from bytoken.org.common.http import app
from bytoken.org.config import server_host, server_port

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=server_host, port=server_port)
