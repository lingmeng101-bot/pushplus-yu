import config
from config import KEY_PASS
from crawler.fetcher import make_session
from crawler.storage import init_db, get_unpushed, mark_pushed
from crawler.main import crawl_and_save
from pushplus.push import send_to_wechat


def main():
    session = make_session()
    conn = init_db()
    try:

        added, malformed = crawl_and_save(
            session, config.BASE_URL, config.MAX_PAGES, conn
        )
        print(f"\n爬虫完成：新增 {added} 条，收容 {malformed} 条\n")


        rows = get_unpushed(conn)
        if not rows:
            print("没有新通知，无需推送。")
            return

        print(f"准备推送 {len(rows)} 条...\n")


        content_list = []
        for notice_id, title, url, day in rows:
            content_list.append(f"**【{day}】{title}**\n\n👉 [点击查看详情]({url})\n")


        content = "\n---\n".join(content_list)
        title_msg = f"西石大新通知 ({len(rows)}条)"


        result = send_to_wechat(token=KEY_PASS, title=title_msg, content=content)


        if result and result.get("code") == 200:
            print("推送成功，标记已推送！")
            for notice_id, title, url, day in rows:
                mark_pushed(conn, notice_id)
        else:
            print(f"推送失败，错误信息: {result}")

    finally:
        conn.close()


if __name__ == "__main__":
    main()