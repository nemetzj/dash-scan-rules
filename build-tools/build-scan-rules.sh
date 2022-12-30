#!/bin/bash

TIMESTAMP=$(date +%s)

### Create output directory based on timestamp
cd ..
mkdir ./output-artifacts/${TIMESTAMP}



### Create JSON from /scan-rules directory

### Find all YML files
#find ./scan-rules/custodian/ -name *.yml -exec echo "Hello, '{}'" \;

find ./scan-rules/custodian/ -name *.yml -exec ./build-tools/test-scan-rules.sh {} \;



#for file in ./scan-rules/custodian/*
#do
#  cd file
#  echo "$file" >> results.out
#done
