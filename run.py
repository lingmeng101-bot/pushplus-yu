import logging

import config
from config import KEY_PASS
from crawler.fetcher import make_session
from crawler.storage import init_db, get_unpushed, mark_pushed
from crawler.main import crawl_and_save
from pushplus.push import send_to_wechat
from logger import setup_logger

log = logging.getLogger(config.LOG_GET)


def main():
    setup_logger()
    log.info("开始运行")

    session = make_session()
    conn = init_db()
    try:

        added, malformed = crawl_and_save(
            session, config.BASE_URL, config.MAX_PAGES, conn
        )
        log.info("爬虫完成：新增 %d 条，收容 %d 条", added, malformed)


        rows = get_unpushed(conn)
        if not rows:
            log.info("没有新通知，无需推送。")
            return

        log.info("准备推送 %d 条...", len(rows))


        content_list = []
        for notice_id, title, url, day in rows:
            content_list.append(f"**【{day}】{title}**\n\n👉 [点击查看详情]({url})\n")


        content = "\n---\n".join(content_list)
        title_msg = f"西石大新通知 ({len(rows)}条)"


        result = send_to_wechat(token=KEY_PASS, title=title_msg, content=content)


        if result and result.get("code") == 200:
            log.info("推送成功，标记已推送！")
            for notice_id, title, url, day in rows:
                mark_pushed(conn, notice_id)
        else:
            log.error("推送失败，错误信息: %s", result)

    except Exception:

        log.exception("运行失败")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()