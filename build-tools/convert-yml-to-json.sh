#!/bin/bash

echo Scan Rule Processed: $1
RULE_PATH=$1

#Get the filename without path or extension (IE. my-scan-rule)
FILE=$(basename -- "$RULE_PATH")
EXTENSION="${RULE_PATH##*.}"
FILE_NAME="${FILE%.*}"

echo $FILE_NAME

#Convert YML rules to JSON and put in output directory
#yq r --prettyPrint -j $1
yq r --prettyPrint -j $1 > ./output-artifacts/$FILE_NAME.json

echo -------------------------------------------------------


