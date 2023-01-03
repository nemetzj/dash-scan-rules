# !/usr/bin/python

import os
import subprocess

#Validate all Cloudcustodian scan rules in the applicable repo directories (../scan-rules/custodian and down)
def custodian_validate_all():
    #myoutput = open('somefile.txt', 'w')

    for root, dirs, files in os.walk("../scan-rules/custodian/aws/ec2", topdown=True): #TODO Change Directory Back
       for name in files:
            if name.endswith(".yml"):
                command = 'custodian validate ' + os.path.join(root, name)
                print("------------------------------------------")
                print("Validating | " + os.path.join(root, name))
                process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
                output, error = process.communicate()


   #for name in dirs:
        # print(os.path.join(root, name))
        # print(name)
        # print(os.path.join(root, name))


#Validate a single Cloudcustodian scan-rule for a given name (with .yml)
def custodian_validate_one(rule_name):
    for root, dirs, files in os.walk("../scan-rules/custodian", topdown=False):
           for name in files:
                if name == rule_name:
                    command = 'custodian validate ' + os.path.join(root, name)
                    print("------------------------------------------")
                    print("Validating | " + command)
                    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
                    
                    output, error = process.communicate()





#Run functions --------------------------------

#custodian_validate_all()
#custodian_validate_one('ec2-ebs-unencrypted-volumes')
