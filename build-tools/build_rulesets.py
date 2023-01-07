#!/usr/bin/python3

import os
import yaml
import json
import requests

import calendar
import time
from datetime import datetime

from dash_utils import *


#Source for building all rulsets
RULESET_DIR = '../rulesets/'
CUSTODIAN_ARTIFACTS_DIR = '../artifacts/'


class schema:
    def __init__(self, schemaType):
        self.type = schemaType
        self.json = []

    def push(self, schema_object):
        json = schema_object.to_json()
        self.json.append(json)

    def create_file(self, directory, file_name):
        write_json_file(self.json, directory, file_name)



class ruleset(schema):
    def __init__(self, name="", organization_id="", description="", related_security_framework=[]):
        self.name = name
        self.organization_id = organization_id
        self.description = description
        self.related_security_framework = related_security_framework

    def to_json(self):
        json_object = {
            "name": self.name,
            "organization_id": self.organization_id,
            "description": self.description,
            "related_security_framework": self.related_security_framework,
        }
        return json_object 


    
class ruleset_to_security_framework(schema):
    def __init__(self):
        self.ruleset_id = ''
        self.security_framework_id = ''
        self.action = ''

    def to_json(self):
        json_object = {
            "ruleset_id": self.ruleset_id,
            "security_framework_id": self.security_framework_id,
            "action": self.action
        }
        return json_object 


class ruleset_to_security_categories(schema):
    def __init__(self):
        self.ruleset_id = ''
        self.security_category_id = ''
        self.action = ''

    def to_json(self):
        json_object = {
            "ruleset_id": self.ruleset_id,
            "security_category_id": self.security_category_id,
            "action": self.action
        }
        return json_object 


class ruleset_to_custodian_rules(schema):
    def __init__(self):
        self.ruleset_id = ''
        self.rule_id = ''
        self.action = ''

    def to_json(self):
        json_object = {
            "ruleset_id": self.ruleset_id,
            "rule_id": self.rule_id,
            "action": self.action
        }
        return json_object





## =================================================================================================
## Driver methods
## =================================================================================================

# Create rulesets.json
def build_all_rulesets():
    ruleset_schema = schema("ruleset");

    file_list = get_all_filenames(RULESET_DIR, ".json")

    for file in file_list:
        f = input_file(RULESET_DIR, file)
        file_json = f.get_json()
       
        ruleset_obj = ruleset()
        ruleset_obj.name = file_json["name"]
        ruleset_obj.organization_id = file_json["organization_id"]
        ruleset_obj.description = file_json["description"]
        ruleset_obj.related_security_framework = file_json["related_security_framework"]
        ruleset_schema.push(ruleset_obj)

    ruleset_schema.create_file(CUSTODIAN_ARTIFACTS_DIR, "rulesets.json")



# Create ruleset mappings
# ruleset_to_security_framework.json
# ruleset_to_security_categories.json
# ruleset_to_custodian_rules.json
def build_ruleset_mappings():
    ruleset_schema = schema("ruleset_to_security_framework");
    file_list = get_all_filenames(RULESET_DIR, ".json")

    for file in file_list:
        f = input_file(RULESET_DIR, file)
        file_json = f.get_json()

        ruleset_submap = file_json["include"]
        for i in ruleset_submap:
            print (i)
 


build_all_rulesets()
#build_ruleset_to_security_framework()