from bs4 import BeautifulSoup
from urllib.parse import urljoin

BLOCKED="blocked"

def parse_list(html:str,base_url:str) -> list[dict]:
    soup=BeautifulSoup(html,'lxml')
    items=soup.select("ul.ej_list li")
    data_list=[]
    for item in items:
        day_tag=item.select_one("p.date_list.fr")
        day=day_tag.get_text(strip=True) if day_tag else ""

        title_tag=item.select_one("p.date_list.fr+a")
        if not title_tag:
            title_tag=item.select_one("a[href*='/info/']")

        link_tag=item.select_one("a[href*='/info/']")
        if not link_tag:
            continue

        title = title_tag.get("title", "").strip() if title_tag else ""
        if not title and title_tag:
            title = title_tag.get_text(strip=True)
        link = link_tag.get("href", "")
        if not link:
            continue

        complete_link=urljoin(base_url,link)

        data_list.append({
            "day":day,
            "title":title,
            "complete_link":complete_link
        })
    return data_list
def parse_detail(html:str):
    soup=BeautifulSoup(html,'lxml')
    title_tag=soup.select_one("title")
    title=title_tag.get_text(strip=True) if title_tag else ""
    #无权限
    if len(html)<2000 and ("无权访问" in html or "系统提示" in html) or (title.strip()=="系统提示"):
        return BLOCKED

    content_div = soup.select_one(
        "div.v_news_content, div#vsb_content, div.content, article, "
        "div.article-content, div.news_content, div.text-content, "
        "div#content, div.main-content, div.article, div.detail-content"
    )
    #html结构问题
    if not content_div:
        return ""

    for tag in content_div.find_all(["script", "style", "img", "iframe"]):
        tag.decompose()

    content=content_div.get_text(strip=True) if content_div else ""
    return content

def next_page_url(html:str,path_url:str):
    soup = BeautifulSoup(html, 'lxml')
    next_tag = soup.select_one("span.p_next.p_fun a")
    if not next_tag:
        return None
    return urljoin(path_url, next_tag.get("href"))

