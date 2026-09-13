# pushplus-yu

西石大通知爬虫 + PushPlus 手机推送。

## 功能
- 抓取西安石油大学通知公告
- 三种状态：normal / restricted / no_content / malformed
- 增量推送，不重复

## 使用方法
1. 复制 `.env.example` 为 `.env`，填入 `PUSHPLUS_TOKEN`
2. `pip install -r requirements.txt`
3. `python run.py`