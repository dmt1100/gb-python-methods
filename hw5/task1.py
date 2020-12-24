# Написать программу, которая собирает входящие письма из своего
# или тестового почтового ящика и сложить данные о письмах
# в базу данных (от кого, дата отправки, тема письма, текст письма полный)
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
from pprint import pprint
from pymongo import MongoClient


driver = webdriver.Chrome()

driver.get('https://mail.ru/')

elem = driver.find_element_by_name('login')
elem.send_keys('study.ai_172')

elem.send_keys(Keys.ENTER)

elem = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'password'))
        )
elem.send_keys('NextPassword172')

elem.send_keys(Keys.ENTER)

elem = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'llc__container'))
        )

elem.click()
mails_list = []

while True:
    time.sleep(2)
    mail = {}
    contact = driver.find_element_by_class_name('letter-contact').text
    date = driver.find_element_by_class_name('letter__date').text
    header = driver.find_element_by_tag_name('h2').text
    body = driver.find_element_by_class_name('letter-body__body-content').text

    mail['contact'] = contact
    mail['date'] = date
    mail['header'] = header
    mail['body'] = body

    mails_list.append(mail)

    try:
        driver.find_element_by_xpath("//span[contains(@class,'button2_arrow-down')]").click()
    except Exception as ex:
        pprint(ex)
        break

client = MongoClient('127.0.0.1', 27017)
db = client['mails']
mail_ru = db.mail_ru
mail_ru.insert_many(mails_list)

# pprint(mails_list)

driver.close()
