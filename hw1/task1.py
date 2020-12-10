# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев
# для конкретного пользователя, сохранить JSON-вывод в файле *.json.

import requests
import json

user_name = 'dmt1100'
main_link = f'https://api.github.com/users/{user_name}/repos'
response = requests.get(main_link)

file_name = 'result.json'
try:
    if response.ok:
        if 'json' in response.headers['content-type']:
            data = response.json()
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                print(f'Файл {file_name} записан!')
        else:
            raise Exception('Неожиданный тип содержимого')
except Exception as e:
    print(e)
