import json
import requests

url = '127.0.0.1:5000'

with open('backend/data.json', 'r') as f:
    datas = json.load(f)

datas['temp'] = [str(n) for n in datas['temp']]
datas['temp'] = ', '.join(datas['temp'])

datas['test'] = [str(n) for n in datas['test']]
datas['test'] = ', '.join(datas['test'])

for data in datas:
    r = requests.post(url, data = datas)