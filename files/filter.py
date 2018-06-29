#!/bin/env python

import json
import requests
import yaml

vars = yaml.load(open('../defaults/main.yml'))
url = vars['lavoisier']['base_url'] + vars['lavoisier']['vo_id_card_endpoint']
try:
    data = requests.get(url).json()
except UserWarning as e:
    print e

cleaned_data = []
for vo in data['voVoms']:
    clean_vo = {}
    for vomses in vo['Vo']:
        try:
            dn = vo['Vo'][0]['VoVomsServer'][0]['VoVomsServer'][2]['X509Cert'][0]['DN'][0]
            clean_vo['name'] = vo['name']
        except IndexError:
            print vo['name'] + "is bad"
    cleaned_data.append(clean_vo)

# write it to a file
with open('data.json', 'w') as file:
    json.dump(cleaned_data, file)
