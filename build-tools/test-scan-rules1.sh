#!/bin/bash

echo Scan Rule Processed: $1
RULE_PATH=$1

#Get the filename without path or extension (IE. my-scan-rule)
#FILE=$(basename -- "$RULE_PATH")
#EXTENSION="${RULE_PATH##*.}"
#FILE_NAME="${FILE%.*}"

#echo $FILE_NAME



custodian validate $1

#if custodian validate $1 | grep 'WARNING'; then
#  echo "matched"
#fi

echo -------------------------------------------------------
