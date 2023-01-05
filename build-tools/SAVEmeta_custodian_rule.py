#!/usr/bin/python3

import os
import yaml
import json
import requests

import calendar
import time
from datetime import datetime


#Source for building all scans
CUSTODIAN_SCAN_RULES_DIR = '../scan-rules/custodian/'

#Artifact directories used for output
TEMP_DIR = '../artifacts/temp/'
CUSTODIAN_ARTIFACTS_DIR = '../artifacts/'
CUSTODIAN_INDIVIDUAL_RULES_DIR = '../artifacts/custodian/rules/'

scan_meta = []


class custodian_meta:
    def __init__(self, filename):
        fileInfo = self.getOne(filename)

        self.root = fileInfo["root"] # ../scan-rules/custodian/aws/ec2/negative/ebs
        self.path = fileInfo["path"] # ../scan-rules/custodian/aws/ec2/negative/ebs/ec2-ebs-unoptimized.yml
        self.file = fileInfo["file"] # ec2-ebs-unoptimized.yml
        self.name = fileInfo["name"] # ec2-ebs-unoptimized
        self.json = self.getJson()


    # Get all yml rules from custodian directories
    def getAll():
        for root, dirs, files in os.walk(CUSTODIAN_SCAN_RULES_DIR, topdown=True):
           for file in files:
                if file.endswith("meta.json"):

                    path = os.path.join(root, file)
                    name = file.replace(".yml", "")

                    #Add all cloudcustodian rules to array
                    scan_meta.append(custodian_meta(root, path, file, name))

    # Get single metadata json file
    def getOne(self, filename):
        for root, dirs, files in os.walk(CUSTODIAN_SCAN_RULES_DIR, topdown=True):
           for file in files:
                if file.endswith(filename):
                    
                    path = os.path.join(root, file)
                    name = file.replace(".json", "")
                    
                    output = {
                        "root": root,
                        "path": path,
                        "file": file,
                        "name": name
                    }
                    return output
          

    def getJson(self):
        file = open(self.path)
        json_data = json.load(file)
        return json_data
                                                 



## Remove the outer scan rule element not needed for JSON
def trim_policy_json(ruleJson):
    trimmed_json = ruleJson['policies'][0]
    return trimmed_json

def write_json_file(json_input, output_dir, output_file):
    with open(output_dir + output_file, 'w') as output_file:
        json.dump(json_input, output_file, indent=2)


## =================================================================================================
## Driver methods
## =================================================================================================


def build_custodian_meta():
    meta = custodian_meta("ec2-ebs-unencrypted-volumes-meta.json")
    meta_json = meta.json


    print("Meta 1 JSON: ", meta_json)

    #print("Meta 1: " + meta.root)
    #print("Meta 1: " + meta.path)
    #print("Meta 1: " + meta.file)
    #print("Meta 1: " + meta.name)
    #print("Meta 1 JSON: ", meta.json)
    #meta = custodian_controls("file-meta.json")


## Create artifacts for all custodian rules
def build_all_cloudcustodian_rules():
    #Create timestamp
    current_GMT = time.gmtime()
    current_timestamp = calendar.timegm(current_GMT)
    
    #Make artifact directories
    ARTIFACT_DIR = CUSTODIAN_ARTIFACTS_DIR + str(current_timestamp) + '/'
    os.mkdir(ARTIFACT_DIR, 0o777)
    ARTIFACT_RULES_DIR = ARTIFACT_DIR + 'rules/'
    os.mkdir(ARTIFACT_RULES_DIR, 0o777)

    custodian_rules.getAll()

    combined_json = []

    # Process all individual custodian rules
    for rule in scan_rules:
        rule_json = convert_yaml_to_json(rule)
        trimmed_json = trim_policy_json(rule_json)
        
        # Create JSON of all individual custodian rules
        individual_file_name = rule.name + '.json'
        write_json_file(trimmed_json, ARTIFACT_RULES_DIR, individual_file_name)

        combined_json.append(trimmed_json)


    # Create combined JSON of custodian rules
    write_json_file(combined_json, ARTIFACT_DIR, "scan-rules.json")

    # Create JSON of metrics
    metrics_json = create_metrics_json(combined_json)
    write_json_file(metrics_json, ARTIFACT_DIR, "output-info.json")





build_custodian_meta()