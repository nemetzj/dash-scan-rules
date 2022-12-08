### Running Scan Rules
1. Install CloudCustodian - https://cloudcustodian.io/docs/quickstart/index.html#install-cc
2. Clone this repository ```git clone https://github.com/nemetzj/dash-scan-rules.git```
3. Navigate to the directory where you want to run a rule
    1. ```cd /scans/aws/ec2```
    2. Run commands using "custodian"
    3. Run custodian checks using the following
       - ```AWS_ACCESS_KEY_ID="XXX" AWS_SECRET_ACCESS_KEY="XXX custodian run --dryrun --region all --output-dir=./my-report ec2-unencrypted-volumes.yml```
       - ```AWS_ACCESS_KEY_ID="XXX" AWS_SECRET_ACCESS_KEY="XXX" custodian run --dry-run --region all --output-dir=./output-report ./scans/account_checks/example-check.yml```


<hr>

### Directory Structure
```
/scans - Contains all CloudCustodian rules
    /aws - Contains all AWS related rules
        
        /account
        /cloudtrail
        /cloudwatch
        /ec2
        /elb
        /..other-aws-services
            -Directories should be named after the "resource" type from cloudcustodian

    /azure
    /..other cloud service
```

<hr>

### Writing CloudCustodian Rules
1. Create new rule file under the appropriate directory, example **"cloudservice-backup-disabled.yml"** 
    1. This filename include the cloud service name (IE. "rds-instance", "rds-cluster) as well as describe the finding as best as possible
2. Each rule should be structured as a single CloudCustodian policy (If you have 10 things to check for a resource, then there will be 10 .yml files) 
   ```
      policies:
         - name: cloudservice-backup-disabled >>> This should be the same as the yml filename
           description: This is a description of what this scan does
           resource: security-group >>> The cloud service you are running the rule against
           filters:
   ```
3. Rules can be written in the based on the following references
    1. Full AWS Reference information  from CloudCustodian can be found here - https://cloudcustodian.io/docs/aws/resources/index.html    
    2. Filter information can be found here - https://cloudcustodian.io/docs/aws/resources/aws-common-filters.html    
    3. "actions" **SHOULD NOT be included in cloudcustodian .yml policies**
4. You can try out your rule by running the command structured as: ```AWS_ACCESS_KEY_ID="XXX" AWS_SECRET_ACCESS_KEY="XXX custodian run --dryrun --region all --output-dir=./output-report cloudservice-backup-disabled.yml```
    1. Result logs will be shown in the console logs
    2. Output .json files will be available under the ./output-report directory
    3. You can specify a specific region if you only want to scan/run the rule for one region: 
        1. **--region us-east-1** vs **--region all** 


<hr>


### Different Outputs/Formats
Different reports and output types can be defined via the console commands and other configuration found in documentation. 

Reports and output types - https://cloudcustodian.io/docs/quickstart/usage.html#reports

#### GRID TEXT FORMAT
```AWS_ACCESS_KEY_ID="XXX" AWS_SECRET_ACCESS_KEY="XXX" custodian report --region all --output-dir=./my-report ec2-unencrypted-volumes.yml --format grid```

####CSV (in CLI)
```AWS_ACCESS_KEY_ID="XXX" AWS_SECRET_ACCESS_KEY="XXX" custodian report --region all --output-dir=./my-report ec2-unencrypted-volumes.yml --format csv```


<hr>
