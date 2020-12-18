# 2. Написать функцию, которая производит поиск и выводит на экран
# вакансии с заработной платой больше введённой суммы. Поиск должен
# происходить по 2-ум полям (минимальной и максимальной зарплате)

from pprint import pprint
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['hh_db']
vacancies_hh = db.vacancies_hh

while True:
    salary = input('Введите желаемую зарплату: ')
    try:
        salary = int(salary)
        break
    except Exception as e:
        print(f"Введите целое число!\nОшибка: {e}")

for vacancy in vacancies_hh.find({'$or': [{'salary_min': {'$gte': str(salary)}}, {'salary_max': {'$gte': str(salary)}}]}):
     pprint(vacancy)
