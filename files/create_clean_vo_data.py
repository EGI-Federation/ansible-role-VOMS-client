#!/bin/env python

import json
import requests
import yaml

vars = yaml.safe_load(open('../defaults/main.yml'))
url = vars['lavoisier']['base_url'] + vars['lavoisier']['vo_id_card_endpoint']
try:
    data = requests.get(url).json()
except UserWarning as e:
    print e

cleaned_data = {"data": []}
for i, vo in enumerate(data['voVoms']):
    print vo['name']
    # Open LSC file
    # Open vomses file
    for k, vomses in enumerate(vo['Vo']):
        print k
        try:
            clean_vo = {
                'name': None,
                'voms': {
                    'DN': None,
                    'CA_DN': None,
                    'hostname': None,
                }
            }
            clean_vo['name'] =  vo['name']
            clean_vo['voms']['DN'] = vo['Vo'][k]['VoVomsServer'][0]['VoVomsServer'][2]['X509Cert'][0]['DN'][0]
            clean_vo['voms']['CA_DN'] = vo['Vo'][k]['VoVomsServer'][0]['VoVomsServer'][2]['X509Cert'][1]['CA_DN'][0]
            clean_vo['voms']['hostname'] = vo['Vo'][k]['VoVomsServer'][0]['VoVomsServer'][2]['host']
            clean_vo['voms']['port'] = vo['Vo'][k]['VoVomsServer'][0]['vomses_port']
            cleaned_data['data'].append(clean_vo)
        except IndexError:
            print vo['name'] + "is bad"
        
# write it to a file
with open('data.json', 'w') as file:
    json.dump(cleaned_data, file)
