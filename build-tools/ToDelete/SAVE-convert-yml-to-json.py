#!/usr/bin/python3

## Reference: https://www.houseninetytwo.com/how-to-convert-a-yaml-file-to-json-to-csv-using-python-pandas-dataframes/

import os
import yaml
import json
import pandas as pd

all_scan_rules = []


def convert_all():
    scan_rules = get_all_custodian_scan_rules()
    convert_yaml_to_json(scan_rules)



def get_all_custodian_scan_rules():
    for root, dirs, files in os.walk("../scan-rules/custodian/", topdown=True):
           for name in files:
                if name.endswith(".yml"):
                    all_scan_rules.append(os.path.join(root, name))
    return all_scan_rules




def convert_yaml_to_json(scan_rules):
    # Open YAML file
    with open('../scan-rules/custodian/aws/account/password-policy-all-checks.yml', 'r') as yml_data:
        configuration = yaml.safe_load(yml_data)

    # Convert to JSON
    with open('../scan-rules/custodian/aws/account/password-policy-all-checks.json', 'w') as json_data:
        json.dump(configuration, json_data, indent=2) #Write to JSON file


def trim_policy_json():
    #Remove outer JSON of policy not needed for API
    f = open('../scan-rules/custodian/aws/account/password-policy-all-checks.json')
    data = json.load(f)
    trimmed_json = data['policies'][0]

    print(trimmed_json)

    f.close()



convert_all()
