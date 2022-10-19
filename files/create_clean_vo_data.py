#!/usr/bin/env python

from __future__ import print_function

import json
import os
import pathlib
import sys

import jsbeautifier
import requests
from ruamel import yaml


def get_data():
    vars = yaml.safe_load(
        open("%s/../defaults/main.yml" % pathlib.Path(__file__).parent.absolute())
    )
    url = "".join(
        (vars["lavoisier"]["base_url"], vars["lavoisier"]["vo_id_card_endpoint"])
    )
    try:
        auth_token = os.environ["OPS_PORTAL_API_TOKEN"]
    except KeyError:
        print("OPS_PORTAL_API_TOKEN not found in the environment, exiting.")
        sys.exit(1)
    headers = {"X-API-Key": auth_token, "Accept": "application/json"}
    try:
        response = requests.get(url, headers=headers)
        status_code = response.status_code
        if status_code != requests.codes.ok:
            print("Graph API call result: ")
            print(status_code)
            print(json.dumps(response.json(), indent=2))
            sys.exit(1)
        data = response.json()
    except UserWarning as e:
        print(e)
        sys.exit(1)
    return data


def filter_data(data):
    """
    Filter the json from Lavoisier, by excluding VOs which do not have a VOMS
    server. This method takes the raw json from Lavoisier and loops over the
    entries in it, extracting the relevant information for the VO.
    The result is an object (data) with an array of dicts containing:
        VO name
        voms server hostname
        voms port
        VOMS Server cert DN
        CA DN of the issueing CA
        :param data=vo: the json object to parse
    """
    cleaned_data = {"data": []}
    for i, vo in enumerate(data['voVoms']):
        for k, vomses in enumerate(vo['Vo']):
            try:
                clean_vo = {
                    'name': None,
                    'voms': {},
                }
                voms_server = vo['Vo'][k]['VoVomsServer'][0]['VoVomsServer'][2]
                clean_vo['voms'].update({
                    'DN': voms_server['X509Cert'][0]['DN'][0],
                    'CA_DN': voms_server['X509Cert'][1]['CA_DN'][0],
                    'hostname': voms_server['host'],
                    'port': vo['Vo'][k]['VoVomsServer'][0]['vomses_port'],
                })
                clean_vo['name'] = vo['name']
                cleaned_data['data'].append(clean_vo)
            except IndexError:
                print("VO %s is bad" % vo['name'])
    print("%d vos configured" % i)

    # write it to a file
    with open('data.yml', 'w') as file:
        yaml.dump(cleaned_data, file, Dumper=yaml.RoundTripDumper)
    return 0


if __name__ == "__main__":
    opts = jsbeautifier.default_options()
    opts.indent_size = 2
    opts.space_in_empty_paren = True
    data = get_data()
    filter_data(get_data())
