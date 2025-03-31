## FastAPI 项目环境搭建

本项目基于 FastAPI 构建，并使用多个依赖库进行增强功能。以下是安装和运行环境的说明。

### 安装依赖

请确保您的 Python 版本为 3.7 及以上。

### 1. 安装 FastAPI 和 Uvicorn
```
pip install fastapi uvicorn
```

FastAPI 是用于构建 Web API 的高性能框架，而 Uvicorn 是一个 ASGI 服务器。

### 2. 安装 YAML 解析和密码加密库
```
pip install pyyaml bcrypt
```
PyYAML 用于处理 YAML 文件，bcrypt 用于加密和验证密码。

### 3. 安装字符编码检测库

```
pip install chardet
```

Chardet 可用于检测文本文件的字符编码。

### 4. 安装项目依赖
```
pip install -r requirements.txt
```
requirements.txt 文件包含了所有必要的依赖包，可使用此命令一键安装。

### 5. 安装数据库支持库
```
pip install sqlalchemy pymysql
```
SQLAlchemy 是一个 SQL ORM，PyMySQL 用于与 MySQL 数据库交互。

### 6. 安装生产环境 WSGI 服务器
```
pip install gunicorn
```
Gunicorn 是一个 WSGI HTTP 服务器，用于在生产环境中运行应用。

### 7. 安装依赖注入工具
```
pip install dependency-injector
```
Dependency Injector 用于管理应用中的依赖关系，提升代码的可维护性。

### 8. 安装 JWT 认证库
```
pip install pyjwt
```
PyJWT 用于创建和验证 JSON Web Tokens（JWT），用于身份验证。

### 9. 安装 WebSockets 支持库
```
pip install websockets
```
WebSockets 用于实现双向实时通信，如在线聊天、通知推送等。

启动 FastAPI 服务器

使用 Uvicorn 启动 FastAPI 应用：
```
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
其中：

- main:app 指的是 main.py 文件中的 app 实例。

- --reload 选项在开发模式下启用热重载。

运行生产环境服务器

使用 Gunicorn 运行 FastAPI 应用：
```
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```
其中：

- -w 4 指定使用 4 个工作进程。

- -k uvicorn.workers.UvicornWorker 使 Gunicorn 兼容 Uvicorn。

结语

至此，FastAPI 项目的环境已经搭建完毕，您可以根据需要进一步扩展和优化应用。