# app.py
from flask import Flask

from bytoken.org.config import server_host, server_port

app = Flask(__name__)


@app.route('/hello')
def home():
    return "Hello, World"


if __name__ == '__main__':
    app.run(host=server_host, port=server_port)
