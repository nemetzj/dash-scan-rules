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



class artifact_set():
    def __init__(self, timestamp="", organization_id="", description="", related_security_framework=[]):
        self.timestamp = timestamp
        self.artifact_dir = artifact_dir
        self.artifact_rules_dir = artifact_rules_dir
        self.artifact_ruleset_dir = artifact_ruleset_dir


    def create_timestamp(self):
        #Create timestamp
        current_GMT = time.gmtime()
        current_timestamp = calendar.timegm(current_GMT)

    def create_all_artifact_dirs(self):
        #Make artifact directories
        ARTIFACT_DIR = CUSTODIAN_ARTIFACTS_DIR + str(current_timestamp) + '/'
        os.mkdir(ARTIFACT_DIR, 0o777)
        ARTIFACT_RULES_DIR = ARTIFACT_DIR + 'rules/'
        os.mkdir(ARTIFACT_RULES_DIR, 0o777)




