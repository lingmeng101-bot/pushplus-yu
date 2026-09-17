import logging

import requests
import config
from crawler.fetcher import fetch
from crawler.parser import parse_list, parse_detail, next_page_url, BLOCKED
from crawler.storage import link_exists, save_yu, commit_db

log = logging.getLogger(config.LOG_NAME)

def crawl_and_save(session, start_url: str, max_pages: int, conn) -> tuple[int,int]:
    url = start_url
    page_count=0
    seen=set()
    added_count=0
    malformed_count = 0
    while url and page_count<max_pages:
        log.info("[list %d/%d] %s", page_count + 1, max_pages, url)
        try:
            html=fetch(session, url)
        except requests.RequestException as e:
            log.error("列表页请求失败，本轮结束: %s (%s)", url, e)
            break
        items=parse_list(html,url)
        if not items:
            log.warning("列表页没解析出任何条目，页面结构可能变了: %s", url)
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
                log.warning("[!] malformed 记录: %s", link)
                continue

            try:
                detail_html=fetch(session, link)
            except requests.RequestException as e:
                log.warning("[!] 详情页请求失败: %s (%s)", link, e)
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
            log.info("  [+] %s 【%s】%s", access_status, item["day"], item["title"])
        commit_db(conn)
        url = next_page_url(html, url)
        page_count += 1
    if malformed_count > 0:
        log.warning("今日发现 %d 条解析异常（malformed），请检查解析器！", malformed_count)
    return added_count , malformed_count