# Написать приложение, которое собирает основные новости с сайтов
# news.mail.ru, lenta.ru, yandex-новости. Для парсинга использовать XPath.
# Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.
# Сложить собранные данные в БД

import requests
import datetime
from pprint import pprint
from pymongo import MongoClient
from lxml import html

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

client = MongoClient('127.0.0.1', 27017)

db = client['news']

# --------------------------------------------------
# mail-новости
url = 'https://news.mail.ru/'

response = requests.get(url, headers=header)
dom = html.fromstring(response.text)

links = dom.xpath("//div[@data-module='TrackBlocks' and @class='js-module']//a[not(contains(@class,'banner'))]/@href")
links = frozenset(links)

mail = []
for link in links:
    response = requests.get(link, headers=header)
    dom = html.fromstring(response.text)
    mail_dict = {}
    name = dom.xpath("//h1/text()")
    mail_link = link
    source = dom.xpath("//span[@class='note']/a/span/text()")
    date = dom.xpath("//span[@class='note']/span[@datetime]/@datetime")
    mail_dict['name'] = name[0]
    mail_dict['link'] = mail_link
    mail_dict['source'] = source[0]
    mail_dict['date'] = date[0]
    mail.append(mail_dict)

mail_news = db.mail_news
mail_news.insert_many(mail)

for news in mail_news.find({}):
    pprint(news)

# -------------------------------------------------
# lenta-новости
url = 'https://lenta.ru/'

response = requests.get(url, headers=header)
dom = html.fromstring(response.text)

items = dom.xpath("//section[contains(@class,'for-main')]//div[contains(@class,'item')]")

lenta = []
for item in items:
    lenta_dict = {}
    name = item.xpath(".//a[not(contains(@class,'topic-title-pic'))]/text()|.//h2/a/text()")
    link = item.xpath(".//a[not(contains(@class,'topic-title-pic'))]/@href|.//h2/a/@href")
    date = item.xpath(".//a[not(contains(@class,'topic-title-pic'))]/time/@datetime|.//h2/a/time/@datetime")
    lenta_dict['name'] = name[0]
    lenta_dict['link'] = url + link[0] if link[0].count('https:') == 0 else link[0]
    lenta_dict['source'] = "lenta.ru"
    lenta_dict['date'] = date[0]
    lenta.append(lenta_dict)

lenta_news = db.lenta_news
lenta_news.insert_many(lenta)

for news in lenta_news.find({}):
    pprint(news)

# ---------------------------------------------
# яндекс-новости
url = 'https://yandex.ru/news/'

response = requests.get(url, headers=header)
dom = html.fromstring(response.text)

items = dom.xpath("//div[contains(@class,'news-top-stories')]/div[contains(@class,'mg-grid__col')]")

yandex = []
for item in items:
    yandex_dict = {}
    name = item.xpath(".//a/h2/text()")
    link = item.xpath(".//span/a/@href")
    source = item.xpath(".//span/a/text()")
    time = item.xpath(".//span[@class='mg-card-source__time']/text()")
    yandex_dict['name'] = name[0]
    yandex_dict['link'] = link[0]
    yandex_dict['source'] = source[0]
    yandex_dict['date'] = f'{str(datetime.datetime.now().day)}.{str(datetime.datetime.now().month)}.{str(datetime.datetime.now().year)} {time[0]}'
    yandex.append(yandex_dict)

yandex_news = db.yandex_news
yandex_news.insert_many(yandex)

for news in yandex_news.find({}):
    pprint(news)
