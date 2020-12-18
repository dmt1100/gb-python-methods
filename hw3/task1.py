# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге
# MongoDB и реализовать функцию, записывающую собранные вакансии в созданную БД.

from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
from pymongo import MongoClient
import re

vacancy_input = input('Ввведите название вакансии : ')
main_link = 'https://hh.ru'
add_link = f"/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&search_field=description&text={vacancy_input}"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
vacancies = []

while True:
    response = requests.get(main_link+add_link, params={}, headers=headers)
    soup = bs(response.text, 'html.parser')
    if response.ok:
        vacancy_list = soup.findAll('div', {'class': 'vacancy-serp-item__row_header'})
        for vacancy in vacancy_list:
            data = {}
            vacancy_header = vacancy.find('a')
            data['site'] = 'https://hh.ru'
            data['vacancy'] = vacancy_header.text
            data['link'] = vacancy_header['href']
            vacancy_salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            if vacancy_salary is not None:
                salary_text = ''.join(vacancy_salary.text.split()[:-1])
            else:
                data['salary_min'] = None
                data['salary_max'] = None
                data['currency'] = None
                vacancies.append(data)
                continue
            if salary_text.find('-') > -1:
                data['salary_min'] = re.sub('\D', '', salary_text.split('-')[0])
                data['salary_max'] = re.sub('\D', '', salary_text.split('-')[-1])
            elif salary_text.find('от') > -1:
                data['salary_min'] = re.sub('\D', '', salary_text)
            elif salary_text.find('до') > -1:
                data['salary_max'] = re.sub('\D', '', salary_text)
            else:
                data['salary_min'] = re.sub('\D', '', salary_text)
                data['salary_max'] = re.sub('\D', '', salary_text)
            data['currency'] = vacancy_salary.text.split()[-1]
            vacancies.append(data)
            next_link = soup.find('a', {'data-qa': 'pager-next'})
        if next_link is None:
            break
        add_link = next_link['href']

print(len(vacancies))
client = MongoClient('127.0.0.1', 27017)
db = client['hh_db']
vacancies_hh = db.vacancies_hh
vacancies_hh.insert_many(vacancies)

# for vacancy in vacancies_hh.find({}).limit(3):
#     pprint(vacancy)
