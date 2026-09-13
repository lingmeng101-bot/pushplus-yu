import os
from dotenv import load_dotenv
load_dotenv()
KEY_PASS=os.getenv("PUSHPLUS_TOKEN")
BASE_URL=os.getenv("BASE_URL")

#数据库
DB_NAME="xsyu.db"
MAX_PAGES = 1
#时间参数
DELAY_MIN = 1.0
DELAY_MAX = 2.0
TIMEOUT_CONNECT = 5
TIMEOUT_READ = 15
#请求参数
RETRY_TOTAL = 3
RETRY_BACKOFF = 1
RETRY_STATUS = (429, 500, 502, 503, 504)
