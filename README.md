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

## 日志
- 运行日志写进项目目录下的 `app.log`（UTF-8），同时在控制台输出一份
- 计划任务用 `pythonw.exe` 跑、没有控制台，回来直接看 `app.log` 就行
- 出错会记 `WARNING` / `ERROR`；日志文件被别的进程占用时只警告一次，不影响爬取和推送