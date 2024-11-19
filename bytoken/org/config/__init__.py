import chardet
import yaml

# 自动检测文件编码
file_path = 'config.yml'
with open(file_path, 'rb') as f:  # 以二进制模式读取文件
    raw_data = f.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']

# 使用检测到的编码读取文件
with open(file_path, 'r', encoding=encoding) as f:
    config = yaml.safe_load(f)

# 获取数据库端口配置
db_host = config['database']['host']
db_user = config['database']['username']
db_password = config['database']['password']
db_name = config['database']['database']
db_port = config['database']['port']

# 获取服务器端口配置
server_host = config['server']['host']
server_port = config['server']['port']

# 服务端加密
secret_key = config["secret_key"]
algorithm = config["algorithm"]
access_token_expire_minutes = config["access_token_expire_minutes"]

# redis
redis_host = config['redis']['host']
redis_port = config['redis']['port']
redis_password = config['redis']['password']
redis_db = config['redis']['db']
