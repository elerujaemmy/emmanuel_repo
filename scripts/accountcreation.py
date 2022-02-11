from __future__ import print_function
import boto3
import botocore
import time
import sys
import argparse
import os
import urllib
import json
from botocore.vendored import requests


def get_client(service):
  client = boto3.client(service)
  return client

def create_account(accountname,accountemail,accountrole,access_to_billing,scp,root_id):
    account_id = 'None'
    client = get_client('organizations')
    try:
        create_account_response = client.create_account(Email=accountemail, AccountName=accountname,
                                                        RoleName=accountrole)
        
 except botocore.exceptions.ClientError as e:
        print(e)
        sys.exit(1)
    #time.sleep(30)
    create_account_status_response = client.describe_create_account_status(CreateAccountRequestId=create_account_response.get('CreateAccountStatus').get('Id'))
    account_id = create_account_status_response.get('CreateAccountStatus').get('AccountId')
    while(account_id is None ):
        create_account_status_response = client.describe_create_account_status(CreateAccountRequestId=create_account_response.get('CreateAccountStatus').get('Id'))
        account_id = create_account_status_response.get('CreateAccountStatus').get('AccountId')
    #move_response = client.move_account(AccountId=account_id,SourceParentId=root_id,DestinationParentId=organization_unit_id)
    return(create_account_response,account_id)
