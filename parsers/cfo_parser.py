import requests
from bs4 import BeautifulSoup
import re
import time
import datetime
import json
import os

headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    }
)

CLEANR = re.compile('<.*?>')


def cleanhtml(raw_html):
    return re.sub(CLEANR, '', raw_html)


def get_cfo_article(url):
    text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(text, 'html.parser')
    html = str(soup.find("div", "news-detail").find("span", itemprop="description"))
    return cleanhtml(html).replace("\t", " ").replace("\xa0", " ")


def get_cfo_page(url):
    text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(text, 'html.parser')

    res = []
    content = soup.body.find(id="content")
    if not content:
        return res
    item_list = content.find("ul", "item-list")
    if not item_list:
        return res

    for i in item_list.find_all("li"):
        try:
            title_a = i.find("div", "title").a
            article_url = "https://www.cfo-russia.ru" + str(title_a.get("href"))
            title = str(title_a.string).strip()
            description = str(i.find("div", "description").string).strip()
            date = str(i.find("div", "date-box").string).strip()
            timestamp = time.mktime(datetime.datetime.strptime(date, "%d.%m.%Y").timetuple())
            article_text = get_cfo_article(article_url)
            res.append({
                "url": article_url,
                "title": title,
                "description": description,
                "text": article_text,
                "timestamp": timestamp,
                "site": "cfo"
            })
        except Exception as e:
            print(e, url)
    return res


def get_cfo_days(days, max_pages=50):
    res = []
    time_begin = time.time() - datetime.timedelta(days=days).total_seconds()
    offset = 0
    while offset < max_pages:
        url = "https://www.cfo-russia.ru/novosti/?PAGEN_1=" + str(offset + 1)
        offset += 1
        page = get_cfo_page(url)
        if not page:
            break
        res += page
        if res and res[-1]["timestamp"] < time_begin:
            break
    return list(filter(lambda i: time_begin <= i["timestamp"], res))


if __name__ == "__main__":
    print('Start parsing cfo-russia.ru.')
    res = get_cfo_days(2)
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    file_name = os.path.join(file_dir, '../data/cfo_news.json')
    with open(file_name, 'w+') as outfile:
        json.dump(res, outfile)
    print(f'Parsing cfo-russia.ru finished. {len(res)} articles saved to cfo_news.json.')
