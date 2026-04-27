import requests as rq
import datetime as dt
import json
import re
import os
from email.utils import parsedate_to_datetime
import xml.etree.ElementTree as ET

# RBC blocks direct API/HTML scraping; RSS feed provides full-text via custom namespace
RBC_RSS_URL = 'https://rssexport.rbc.ru/rbcnews/news/30/full.rss'
RBC_NS = 'https://www.rbc.ru'


def parse_rbc_news(days=1):
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; RSS reader)'}
    response = rq.get(RBC_RSS_URL, headers=headers, timeout=10)
    if response.status_code != 200:
        print(f'RBC RSS error: {response.status_code}')
        return []

    root = ET.fromstring(response.content)
    ns = {'rbc': 'https://www.rbc.ru'}
    ress = []
    cutoff = dt.datetime.now().timestamp() - days * 86400

    for item in root.iter('item'):
        url = item.findtext('link', '').strip()
        if '/finances/' not in url:
            continue
        try:
            res = {}
            res['url'] = url
            res['site'] = 'rbc_finances'
            res['title'] = (item.findtext('title') or '').replace('\xa0', ' ').replace('\t', ' ').strip()
            res['description'] = (item.findtext('description') or '').replace('\xa0', ' ').replace('\t', ' ').strip()

            full_text_el = item.find('{https://www.rbc.ru}full-text')
            if full_text_el is not None and full_text_el.text:
                clean = re.sub(r'<[^>]+>', '', full_text_el.text)
                res['text'] = clean.replace('\xa0', ' ').replace('\t', ' ').strip()
            else:
                res['text'] = res['description']

            pub_date = item.findtext('pubDate', '')
            ts = parsedate_to_datetime(pub_date).timestamp()
            res['timestamp'] = ts

            if ts < cutoff:
                continue
            ress.append(res)
        except Exception as e:
            print(e, url)

    return ress


if __name__ == "__main__":
    print('Start parsing rbc finances.')
    res = parse_rbc_news(365)
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    file_name = os.path.join(file_dir, '../data/rbc_finances_news.json')
    with open(file_name, 'w+') as outfile:
        json.dump(res, outfile)
    print(f'Parsing rbc finances finished. {len(res)} articles saved to rbc_finances_news.json.')
