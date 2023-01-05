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

scan_meta = []


class artifact_set:
    def __init__(self):
        self.timestamp = self.create_timestamp()
        self.artifact_dir = ''
        self.rules_dir = ''
        self.meta_dir = ''
        
    #Create timestamp
    def create_timestamp(self):
        current_GMT = time.gmtime()
        current_timestamp = calendar.timegm(current_GMT)
        return current_timestamp

    #Create directories for artifacts
    def create_directories(self):
        ARTIFACT_DIR = CUSTODIAN_ARTIFACTS_DIR + str(self.timestamp) + '/'
        os.mkdir(ARTIFACT_DIR, 0o777)

        ARTIFACT_RULES_DIR = ARTIFACT_DIR + 'rules/'
        os.mkdir(ARTIFACT_RULES_DIR, 0o777)

        ARTIFACT_META_DIR = ARTIFACT_DIR + 'meta/'
        os.mkdir(ARTIFACT_META_DIR, 0o777)

        self.artifact_dir = ARTIFACT_DIR 
        self.rules_dir = ARTIFACT_RULES_DIR
        self.meta_dir = ARTIFACT_META_DIR
        


class custodian_meta:
    def __init__(self, filename):
        #TODO Validate JSON SCHEMA of meta file 
        fileInfo = self.getOne(filename)

        self.root = fileInfo["root"] # ../scan-rules/custodian/aws/ec2/negative/ebs
        self.path = fileInfo["path"] # ../scan-rules/custodian/aws/ec2/negative/ebs/ec2-ebs-unoptimized-meta.json
        self.file = fileInfo["file"] # ec2-ebs-unoptimized-meta.json
        self.name = fileInfo["name"] # ec2-ebs-unoptimized-meta
        self.json = self.getJson()


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


    def createMetaFile(self):
        meta_json = self.json

        formatted_meta_output = {
            "rule": meta_json["rule"],
            "name": meta_json["name"],
            "description": meta_json["description"],
            "recommendation": meta_json["recommendation"],
            "resource_type": meta_json["resource_type"],
            "urls": meta_json["urls"],
            "key_fields": meta_json["key_fields"]
        }
        #print("==============================================")
        #print("New Meta JSON: ", formatted_meta_output)

        return formatted_meta_output


    def createMetaControl(self):
        meta_json = self.json

        formatted_meta_output = {
            "scan": meta_json["rule"],
            "type": "custodian",
            "categories": meta_json["security_categories"],
            "sub_categories": meta_json["security_sub_categories"]
        }
        return formatted_meta_output



#Get all metadata files for a given directory and sub-directories    
def get_all_meta_filenames(directory):
    files_list = []
    for root, dirs, files in os.walk(directory, topdown=True):
       for file in files:
            if file.endswith("meta.json"):
                files_list.append(file)
    return files_list


#Write JSON file basaed on JSON input and output directory, file-name
def write_json_file(json_input, output_dir, output_file):
    with open(output_dir + output_file, 'w') as output_file:
        json.dump(json_input, output_file, indent=2)


## =================================================================================================
## Driver methods
## =================================================================================================


def build_all_custodian_meta():
    artifacts = artifact_set()
    artifacts.create_directories()
    #print("Artifact2: ", artifacts.artifact_dir)
    #print("Artifact2: ", artifacts.meta_dir)
    #print("Artifact2: ", artifacts.rules_dir)

    meta_combined_json = []
    
    # Write all meta files   
    file_list = get_all_meta_filenames(CUSTODIAN_SCAN_RULES_DIR)
    for file in file_list:
        #print("file:", file)
        meta = custodian_meta(file)
        metaArtifact = meta.createMetaFile()
        meta_combined_json.append(metaArtifact) # Add to combined JSON
        #print("metaArtifact:", metaArtifact)
        write_json_file(metaArtifact, artifacts.meta_dir , meta.file)

    #Write meta combined json
    write_json_file(meta_combined_json, artifacts.artifact_dir , 'scan-meta.json')
    


"""
def build_single_custodian_meta(meta_file):
    meta = custodian_meta(meta_file)
    metaArtifact = meta.createMetaFile()
    write_json_file(metaArtifact, CUSTODIAN_ARTIFACTS_DIR , meta.file)


    metaControlArtifact = meta.createMetaControl()
    write_json_file(metaControlArtifact, CUSTODIAN_ARTIFACTS_DIR , "control.json")
"""



build_all_custodian_meta()

#build_single_custodian_meta("ec2-ebs-unencrypted-volumes-meta.json")