# 2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
# Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

import requests
import json

# API точных обменных курсов, которые
# предоставляются Европейским центральным резервным банком.

api_key = '342ca0163149da25c1bd1345'

file_name = 'result2.json'

main_link = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/RUB'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

response = requests.get(main_link, headers=headers)

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
