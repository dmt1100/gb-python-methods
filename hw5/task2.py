# Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo
# и складывает данные в БД. Магазины можно выбрать свои.
# Главный критерий выбора: динамически загружаемые товары

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pprint import pprint
from pymongo import MongoClient
import time
import json


chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)

driver.get('https://www.mvideo.ru/')
hits_list = []

try:
    hits = driver.find_element_by_xpath('//div[contains(text(),"Хиты продаж")]/ancestor::div[@class="section"]')
except Exception as ex:
    print('Хиты продаж отсутствуют\n', ex)

while True:
    count = 0
    try:
        hit_goods = hits.find_elements_by_xpath(".//a[@class='fl-product-tile-picture fl-product-tile-picture__link']")
        for elem in hit_goods:
            good = elem.get_attribute('data-product-info')
            good = good.replace('\t', '')
            good = good.replace('\n', '')
            good = json.loads(good)
            good.pop('Location')
            good.pop('eventPosition')
            if good not in hits_list:
                hits_list.append(good)
            else:
                count += 1
    except Exception as ex:
        print('Ошибка: ', ex)

    if count == len(hits_list):
        break
    else:
        try:
            next_button = WebDriverWait(hits, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, './/a[contains(@class,"next-btn")]')
                )
            )
            next_button.click()
            time.sleep(2)
        except Exception as ex:
            print('Ошибка: ', ex)

pprint(hits_list)
print(f'Количество хитов продаж: {len(hits_list)}')

client = MongoClient('127.0.0.1', 27017)
db = client['m_video_db']
m_video_hits = db.m_video_hits
m_video_hits.insert_many(hits_list)

driver.close()
