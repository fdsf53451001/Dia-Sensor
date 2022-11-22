import requests

url = 'http://120.126.17.188:8090/_data'

def post(datas, /, url = url):
    ''' function to post the test result to database

    datas: a list contain multiple test result, each as a dict.
           with structure like follow
           'memberid': int,
           'temp': int list with len == 10,
           'test': int list with len == 10
    '''

    for data in datas:
        temp = ', '.join([str(n) for n in data['temp']])
        test = ', '.join([str(n) for n in data['test']])
        r = requests.post(url, data = {'memberid': data['memberid'], 'temp': temp, 'test': test}, verify = False)
        print(r.status_code)
