import time
import config
import random
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
def make_session(headers: dict=None) -> requests.Session:
    session = requests.Session()
    define_headers={
        "User-Agent":random.choice(config.USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    retry = Retry(
        total=config.RETRY_TOTAL,
        backoff_factor=config.RETRY_BACKOFF,
        status_forcelist=config.RETRY_STATUS,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update(define_headers)
    if headers:
        session.headers.update(headers)
    return session
def fetch(session:requests.Session , url: str) -> str:
    time.sleep(random.uniform(config.DELAY_MIN , config.DELAY_MAX))
    timeout=(config.TIMEOUT_CONNECT,config.TIMEOUT_READ)
    res=session.get(url,timeout=timeout)
    res.raise_for_status()
    res.encoding=res.apparent_encoding
    return res.text