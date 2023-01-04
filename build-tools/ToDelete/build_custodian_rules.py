#!/usr/bin/python3
## Reference: https://www.houseninetytwo.com/how-to-convert-a-yaml-file-to-json-to-csv-using-python-pandas-dataframes/

import os
import yaml
import json

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




def convert_yaml_to_json(rule, artifact):
    # Open YAML file
    with open(rule.path, 'r') as yml_data:
        configuration = yaml.safe_load(yml_data)

    # Generate JSON file location
    json_file_name = rule.name + '.json'
    #print("JSON File: " + json_file_name)

    if(artifact):
        # Convert to JSON
        with open(CUSTODIAN_INDIVIDUAL_RULES_DIR + json_file_name, 'w') as json_data:
            json.dump(configuration, json_data, indent=2) #Write to JSON file

        f = open(CUSTODIAN_INDIVIDUAL_RULES_DIR + json_file_name)
        output_data = json.load(f)
        return output_data

    else:
        with open(TEMP_DIR + json_file_name, 'w') as json_data:
            json.dump(configuration, json_data, indent=2) #Write as temporary JSON file
       
        f = open(TEMP_DIR + json_file_name)
        output_data = json.load(f)
        print('JSON Data From Convert: ', output_data) #Remove temporary JSON file

        return output_data




## Remove the outer scan rule element not needed for JSON
def trim_policy_json(rule, artifact):
    json_file_name = rule.name + '.json'

    # Remove outer JSON of policy not needed for API
    f = open(CUSTODIAN_INDIVIDUAL_RULES_DIR + json_file_name)
    data = json.load(f)
    trimmed_json = data['policies'][0]

    if(artifact):
        write_json_file(trimmed_json, CUSTODIAN_INDIVIDUAL_RULES_DIR, json_file_name)


    return trimmed_json



## Create a combined JSON array with ALL custodian rules
def get_combined_policy_json(artifact):
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

    if(artifact):
        write_json_file(combined_json, CUSTODIAN_ARTIFACTS_DIR, 'all-custodian-rules.json')

    return combined_json


def write_json_file(json_input, output_dir, output_file):
    with open(output_dir + output_file, 'w') as output_file:
        json.dump(json_input, output_file, indent=2)



def create_metrics_json(combined_json, artifact):
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

    if(artifact):
        write_json_file(metrics_obj, CUSTODIAN_ARTIFACTS_DIR, 'output-results.json')

    return metrics_obj




## Create artifacts for all custodian rules
def build_all_cloudcustodian_rules():
    custodian_rules.getAll()

    # Create JSON of all individual custodian rules
    for rule in scan_rules:
        convert_yaml_to_json(rule, True)
        trim_policy_json(rule, True)

    # Create combined JSON of custodian rules
    combined_json = get_combined_policy_json(True)

    create_metrics_json(combined_json, True)


# Create artifacts for all custodian rules
#def create_request():
#    custodian_rules.getOne('ec2-ebs-unencrypted-volumes')
#
#    # Create JSON of all individual custodian rules
#    for rule in scan_rules:
#        rule_json = convert_yaml_to_json(rule, False)
#        trimmed_rule = trim_policy_json(rule_json, False)
#                   print('Single Rule:')




#build_all_cloudcustodian_rules()
#create_request()
