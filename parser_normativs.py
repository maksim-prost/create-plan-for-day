from bs4 import BeautifulSoup
import requests
import sys
import json
url = 'https://fireguys.ru/apps/sbornik-normativov-po-psp-2022.html'

r = requests.get(url)

soup = BeautifulSoup(r.text, 'lxml')

table = soup.select('table.tablenorm-psp2022 tbody tr')
raw_list = [row for row in table 
            if row.td.get('class') and row.td.get('class')[0] not in ['stolbhead', 'podrazdel-psp2022', 'vstolb'] ]
list_normativ = []
cur_normativ = []
dict_normativs = dict()
get_data = lambda tag, key: tag.select(key)[0].text.strip()

for row in raw_list:
    if row.td.get('class')[0]=="stolb1":
        if not row.select('td.stolb6'):
            process = dict_normativs[key]['process']
        else:
            process =  get_data(row, 'td.stolb6')
        key = get_data(row, 'td.stolb1')
        score = []
        
        if stolb345 := row.select('td.stolb345'):
            score = [ {
                'specificity': None,
                'score': [td.text.strip() for td in stolb345 ]
            }, ]
        dict_normativs[key] = {
                'title': get_data(row, 'td.stolb2'),
                'process': process,
                'score': score
        }
        continue
    dict_normativs[key]['score'].append( {
        'specificity': get_data(row, 'td.stolb2'),
        'score': [td.text.strip() for td in row.select('td.stolb345')]
    })

print(len(dict_normativs))
# sys.stdout = open('temp2', 'w')
# print(list_normativ)
sys.stdout = open('prof_normativ.json', 'w')
print(json.dumps(dict_normativs))