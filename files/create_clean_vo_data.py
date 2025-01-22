#!/usr/bin/env python

from __future__ import print_function

import json
import os
import pathlib
import sys

import jsbeautifier
import requests
import ruamel.yaml


def get_data():
    """
    Download VO info data using Operations Portal API
    """
    yaml = ruamel.yaml.YAML(typ="safe", pure=True)
    vars = yaml.load(
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
        VOMS server hostname
        VOMS port
        VOMS Server cert DN
        CA DN of the issueing CA
        :param data=vo: the json object to parse
    """
    cleaned_data = {"data": []}
    for vo in data["results"]:
        vo_name = vo["name"]
        clean_vo_info = {"name": vo_name, "voms": []}
        for vo_info in vo["Vo"]:
            vo_registry = vo_info["Registries"][0]
            try:
                # Only look for VOMS admin server
                if vo_registry["is_vomsadmin_server"] == "1":
                    try:
                        port = vo_registry["vomses_port"]
                        voms_server = vo_registry["VoVomsServer"]
                        hostname = voms_server[1]["hostname"][0]
                        dn = voms_server[2]["X509Cert"][0]["DN"][0]
                        ca_dn = voms_server[2]["X509Cert"][1]["CA_DN"][0]
                        clean_vo_info["voms"].append(
                            {
                                "DN": dn,
                                "CA_DN": ca_dn,
                                "hostname": hostname,
                                "port": port,
                            }
                        )
                    except IndexError:
                        print("VOMS for VO %s is bad" % vo_name)
            except KeyError:
                # is_vomsadmin_server is not always present
                pass
        # Only add VOs having at least one VOMS server
        if len(clean_vo_info["voms"]) > 0:
            cleaned_data["data"].append(clean_vo_info)
        else:
            print("%s is not having any VOMS server" % vo_name)

    print("%d vos configured" % len(cleaned_data["data"]))

    # write it to a file
    with open("%s/data.yml" % pathlib.Path(__file__).parent.absolute(), "w") as file:
        yaml = ruamel.yaml.YAML(typ="rt", pure=True)
        yaml.dump(cleaned_data, file)
    return 0


if __name__ == "__main__":
    opts = jsbeautifier.default_options()
    opts.indent_size = 2
    opts.space_in_empty_paren = True
    data = get_data()
    filter_data(get_data())
