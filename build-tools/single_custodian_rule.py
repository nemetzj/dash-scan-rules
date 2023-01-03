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

    # Get one yml rule from custodian directories
    def getOne(rule):
        for root, dirs, files in os.walk(CUSTODIAN_SCAN_RULES_DIR, topdown=True):
           for file in files:
                if file.endswith(rule):
    
                    path = os.path.join(root, file)
                    name = file.replace(".yml", "")
    
                    #Add all cloudcustodian rules to array
                    scan_rules.append(custodian_rules(root, path, file, name))




def convert_yaml_to_json(ruleObj):
    # Open YAML file
    with open(ruleObj.path, 'r') as yml_data:
        configuration = yaml.safe_load(yml_data)

    # Generate JSON file location
    json_file_name = ruleObj.name + '.json'

    with open(TEMP_DIR + json_file_name, 'w') as json_data:
        json.dump(configuration, json_data, indent=2) # Write as temporary JSON file
   
    f = open(TEMP_DIR + json_file_name)
    output_data = json.load(f) # Save JSON to variable

    os.remove(TEMP_DIR + json_file_name) # Remove temporary JSON file

    return output_data




## Remove the outer scan rule element not needed for JSON
def trim_policy_json(ruleJson):
    trimmed_json = ruleJson['policies'][0]
    return trimmed_json



## Create a combined JSON array with ALL custodian rules
def get_combined_policy_json():
    combined_json = []
    # iterate over files in that directory
    for filename in os.listdir(CUSTODIAN_INDIVIDUAL_RULES_DIR):
        f = os.path.join(CUSTODIAN_INDIVIDUAL_RULES_DIR, filename)
        # checking if it is a file
        if os.path.isfile(f):
            with open(f, 'r') as infile:
                combined_json.append(json.load(infile))
                #combined_json.extend(json.load(infile))
                #print(f)

    return combined_json



def create_metrics_json(combined_json):
    metrics_obj = {}

    #Timestamp
    current_GMT = time.gmtime()
    timestamp = calendar.timegm(current_GMT)

    #DateTime
    now = datetime.now() # current date and time
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")


    #Add to Results Array
    metrics_obj["Timestamp"] = timestamp;
    metrics_obj["ArtifactDate"] = date_time;
    metrics_obj["Total Custodian Rules"] = len(combined_json);

    return metrics_obj


def write_json_file(json_input, output_dir, output_file):
    with open(output_dir + output_file, 'w') as output_file:
        json.dump(json_input, output_file, indent=2)


## =================================================================================================
## Driver methods
## =================================================================================================

## Create artifacts for all custodian rules
def build_all_cloudcustodian_rules():
    custodian_rules.getAll()

    # Create JSON of all individual custodian rules
    for rule in scan_rules:
        rule_json = convert_yaml_to_json(rule)
        trimmed_json = trim_policy_json(rule)

    # Create combined JSON of custodian rules
    combined_json = get_combined_policy_json()

    metrics_json = create_metrics_json(combined_json)


def send_lambda_request(scan_rule_file):
    custodian_rules.getOne(scan_rule_file)

    # Create JSON of all individual custodian rules
    #for rule in scan_rules:
    rule = scan_rules[0]
    rule_json = convert_yaml_to_json(rule)
    trimmed_json = trim_policy_json(rule_json)

    #print('JSON Plain: ', rule_json)
    #print('JSON Trimmed JSON: ', trimmed_json)

    api_body = {
      "clientId": "client-id1",
      "cloudPlatform": "aws",
      "credentials": {     
        "accountId": "634658324862",
        "roleName": "Dash-Test-Scanning",
        "externalId": "K065T92"
      },
      "scanParameters": {
        "regions": [
          "us-east-1",
          "us-east-2"
        ],
        "tags": [
        ],
        "filters": [
        ],
        "policies": [
            trimmed_json
        ]
      }
    }

    print('API BODY: ', api_body)

    api_url = "https://rgbz2b87vj.execute-api.us-east-1.amazonaws.com/dash-poc-jake4/scan"
    headers =  {"Content-Type":"application/json"}
    response = requests.post(api_url, data=json.dumps(api_body), headers=headers)
    
    scanner_lambda_response = response.json()
    scan_id = scanner_lambda_response['scanId']

    print('===============================================')
    print('Status Code: ', response.status_code)
    print('Response: ', scanner_lambda_response)
    print('https://s3.console.aws.amazon.com/s3/buckets/c7n-aas-dash-poc-jake4-results?region=us-east-1&prefix=',scan_id,'/&showversions=false', sep='')
    print('===============================================')




#build_all_cloudcustodian_rules()
#send_lambda_request('ec2-ebs-unencrypted-volumes.yml')
