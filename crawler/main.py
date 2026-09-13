import requests
import config
from crawler.fetcher import fetch
from crawler.parser import parse_list, parse_detail, next_page_url, BLOCKED
from crawler.storage import link_exists, save_yu, commit_db

def crawl_and_save(session, start_url: str, max_pages: int, conn) -> tuple[int,int]:
    url = start_url
    page_count=0
    seen=set()
    added_count=0
    malformed_count = 0
    while url and page_count<max_pages:
        print(f"[list {page_count + 1}/{max_pages}] {url}")
        html=fetch(session, url)
        items=parse_list(html,url)
        for item in items:
            link=item["complete_link"]
            if link in seen or link_exists(conn, link):
                continue
            seen.add(link)

            if not item["title"] or not item["day"]:
                access_status = "malformed"
                content = ""
                save_yu(
                    conn,
                    url=link,
                    day=item["day"],
                    title=item["title"],
                    content=content,
                    access_status=access_status
                )
                malformed_count += 1
                print(f"  [!] malformed 记录: {link}")
                continue

            try:
                detail_html=fetch(session, link)
            except requests.RequestException as e:
                print(f"  [!] detail fail: {link} ({e})")
                continue
            content=parse_detail(detail_html)
            if content==BLOCKED:
                access_status = "restricted"
                content = item["title"]
            elif not content or content == "":
                access_status = "no_content"
                content = item["title"]
            else:
                access_status = "normal"
            save_yu(
                conn,
                url=link,
                day=item["day"],
                title=item["title"],
                content=content,
                access_status=access_status
            )
            added_count += 1
        commit_db(conn)
        url = next_page_url(html, url)
        page_count += 1
    if malformed_count > 0:
        print(f"\n⚠️ 警告：今日发现 {malformed_count} 条解析异常（malformed），请检查解析器！")
    return added_count , malformed_count
