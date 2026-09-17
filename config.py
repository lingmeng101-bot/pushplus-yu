import os
import logging
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
#logger配置
LOG_NAME='ling-file'
LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s - [%(filename)s:%(lineno)d] - %(name)s - %(levelname)s - %(message)s"
LOG_DATEFMT = "%Y-%m-%d %H:%M:%S"
LOG_FILE = "app.log"
#随机UA
USER_AGENTS = [

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",

    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",

    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0"
]