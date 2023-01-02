#!/usr/bin/python3
## Reference: https://www.houseninetytwo.com/how-to-convert-a-yaml-file-to-json-to-csv-using-python-pandas-dataframes/

import os
import yaml
import json
import pandas as pd

import calendar
import time
from datetime import datetime  


#Source for building all scans
CUSTODIAN_SCAN_RULES_DIR = '../scan-rules/custodian/'

#Artifact directories used for output
CUSTODIAN_ARTIFACTS_DIR = '../artifacts/custodian/'
CUSTODIAN_INDIVIDUAL_RULES_DIR = '../artifacts/custodian/rules/'


scan_rules = []


class custodian_rules:
    def __init__(self, root, path, file, name):
        self.root = root    # ../scan-rules/custodian/aws/ec2/negative/ebs
        self.path = path    # ../scan-rules/custodian/aws/ec2/negative/ebs/ec2-ebs-unoptimized.yml
        self.file = file    # ec2-ebs-unoptimized.yml
        self.name = name    # ec2-ebs-unoptimized

    # Get all yml rules from custodian directories
    def getAll():
        for root, dirs, files in os.walk(CUSTODIAN_SCAN_RULES_DIR, topdown=True):
           for file in files:
                if file.endswith(".yml"):

                    path = os.path.join(root, file)
                    name = file.replace(".yml", "")

                    #Add all cloudcustodian rules to array
                    scan_rules.append(custodian_rules(root, path, file, name))


class artifact_metrics:
    def __init__(self, timestamp, artifact_date, number_rules):
        self.timestamp = timestamp    
        self.artifact_date = date_time    
        self.number_custodian_rules = number_custodian_rules





def convert_yaml_to_json(rule):
    # Open YAML file
    with open(rule.path, 'r') as yml_data:
        configuration = yaml.safe_load(yml_data)

    # Generate JSON file location
    json_file_name = rule.name + '.json'
    #print("JSON File: " + json_file_name)

    # Convert to JSON
    with open(CUSTODIAN_INDIVIDUAL_RULES_DIR + json_file_name, 'w') as json_data:
        json.dump(configuration, json_data, indent=2) #Write to JSON file



## Remove the outer scan rule element not needed for JSON
def trim_policy_json(rule, artifact):
    json_file_name = rule.name + '.json'

    # Remove outer JSON of policy not needed for API
    f = open(CUSTODIAN_INDIVIDUAL_RULES_DIR + json_file_name)
    data = json.load(f)
    trimmed_json = data['policies'][0]

    if(artifact):
        # Write trimmed JSON to existing JSON file output
        f = open(CUSTODIAN_INDIVIDUAL_RULES_DIR + json_file_name, 'w')
        json.dump(trimmed_json, f, indent=2)

        f.close()

    return trimmed_json



## Create a combined JSON file with ALL custodian rules in artifacts
def create_combined_policy_json():
    combined_json = []
    # iterate over files in
    # that directory
    for filename in os.listdir(CUSTODIAN_INDIVIDUAL_RULES_DIR):
        f = os.path.join(CUSTODIAN_INDIVIDUAL_RULES_DIR, filename)
        # checking if it is a file
        if os.path.isfile(f):
            with open(f, 'r') as infile:
                combined_json.append(json.load(infile))
                #combined_json.extend(json.load(infile))
                #print(f)

    with open(CUSTODIAN_ARTIFACTS_DIR + 'all-custodian-rules.json', 'w') as output_file:
        json.dump(combined_json, output_file, indent=2)
    return combined_json



def create_metrics_json(combined_json):
    metrics_array = []

    #Timestamp
    current_GMT = time.gmtime()
    timestamp = calendar.timegm(current_GMT)

    #DateTime
    now = datetime.now() # current date and time
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")


    #Add to Results Array
    metrics_array.append({"Timestamp": timestamp})
    metrics_array.append({"ArtifactDate": date_time})
    metrics_array.append({"Total Custodian Rules": len(combined_json)})
    print(metrics_array)

    with open(CUSTODIAN_ARTIFACTS_DIR + 'output-results.json', 'w') as output_file:
        json.dump(metrics_array, output_file, indent=2)




## Create artifacts for all custodian rules
def build_all_cloudcustodian_rules():
    custodian_rules.getAll()

    # Create JSON of all individual custodian rules
    for rule in scan_rules:
        convert_yaml_to_json(rule)
        trim_policy_json(rule, "true")

    # Create combined JSON of custodian rules
    combined_json = create_combined_policy_json()
    create_metrics_json(combined_json)
    #print(len(combined_json))





build_all_cloudcustodian_rules()
