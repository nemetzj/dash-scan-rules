#!/bin/bash


### Find all YML files
cd ..
#find ./scan-rules/custodian/ -name *.yml -exec echo "'{}'" \;

find ./scan-rules/custodian/ -name *.yml -exec ./build-tools/test-scan-rules.sh {} \;

