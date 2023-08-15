# Getting started:

Install Python
Install poetry
Use the OCI python sdk
Config file is picked from default location (eg config file path:  windows: C:\Users\annatara\.oci\config), format example:
https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm

Run the script using: 
> poetry run python .\oci_python\oci-interaction.py '10.0.0.0/16' 'vcn_test' 'subnet_test' 'instance-20230815-0235' 'VM.Standard.E2.1.Micro' 'Oracle Linux' 'wxDv:US-SANJOSE-1-AD-1' 1.0 2

# About the code:
ociclientwrapper file has helper methods to interact with oci.
oci-interaction file is the entry point that covers the assignment given.
Unit test: Since this script was more about interactive with a oci client and does not have business logic, 
did not give priority to the test. Tested using script execution.

# Deployment Plan using OCI:
## This script can be deployed as a OCI function and invoked as needed. 
https://docs.oracle.com/en-us/iaas/Content/Functions/Concepts/functionsoverview.htm

## Terraform can be used to set up the OCI function
https://blogs.oracle.com/developers/post/creating-building-and-invoking-a-function-on-oci-with-terraform

## DevOps pipeline can be set to invoke terraform and tests 
https://docs.oracle.com/en/solutions/ci-cd-pipe-oci-devops/index.html#GUID-A70082F0-DFB8-43F2-8189-60B11BA258E1

## Before deploying the code to production need to add observability around it
Add enough logging, events, metrics to the code and alert on issues.
https://docs.oracle.com/en-us/iaas/Content/Monitoring/Concepts/monitoringoverview.htm

