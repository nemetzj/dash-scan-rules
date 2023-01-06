#!/usr/bin/python3

import os
import yaml
import json
import requests

import calendar
import time
from datetime import datetime


#Class used for file information and getting other functionality
class input_file:
    def __init__(self, directory, filename):
        #TODO Validate JSON SCHEMA of ruleset file 
        self.directory = directory
        fileInfo = self.get_file_info(filename)

        self.root = fileInfo["root"] # ../scan-rules/custodian/aws/ec2/negative/ebs
        self.path = fileInfo["path"] # ../scan-rules/custodian/aws/ec2/negative/ebs/ec2-ebs-unoptimized-meta.json
        self.file = fileInfo["file"] # ec2-ebs-unoptimized-meta.json
        self.name = fileInfo["name"] # ec2-ebs-unoptimized-meta
        self.json = self.get_json()


    def get_file_info(self, filename):
        for root, dirs, files in os.walk(self.directory, topdown=True):
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
          

    def get_json(self):
        file = open(self.path)
        json_data = json.load(file)
        return json_data



#Get all rules files for a given directory and sub-directories
def get_all_filenames(directory, ending):
    files_list = []
    for root, dirs, files in os.walk(directory, topdown=True):
       for file in files:
            if file.endswith(ending):
                files_list.append(file)
    return files_list



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




def write_json_file(json_input, output_dir, output_file):
    with open(output_dir + output_file, 'w') as output_file:
        json.dump(json_input, output_file, indent=2)




## ===================================================
## Metrics and other processing
## ===================================================

def create_artifact_dirs(ruleObj):
    #Create timestamp
    current_GMT = time.gmtime()
    current_timestamp = calendar.timegm(current_GMT)
    
    #Make artifact directories
    ARTIFACT_DIR = CUSTODIAN_ARTIFACTS_DIR + str(current_timestamp) + '/'
    os.mkdir(ARTIFACT_DIR, 0o777)
    ARTIFACT_RULES_DIR = ARTIFACT_DIR + 'rules/'
    os.mkdir(ARTIFACT_RULES_DIR, 0o777)



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




""" #Move to scan-rules schema functions
def trim_policy_json(ruleJson):
    trimmed_json = ruleJson['policies'][0]
    return trimmed_json
"""