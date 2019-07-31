# This lambda function will  copy CloudWatch logs of all the available instances into S3  after every 2 hours
# Multiple Log groups can be handles with this Lambda
import boto3
import collections
from datetime import datetime, timedelta, date, time
import time

region = 'us-east-2'

def lambda_handler(event, context):
    log_file = boto3.client('logs')
    now=datetime.now()
    startOfhour = now.replace(minute=0,second=0, microsecond=0)-timedelta(hours=2)
    endOfhour = now.replace(minute=0,second=0, microsecond=0)
    unix_start = datetime(1970,1,1)
    #group_name = ['/aws/rds/instance/rdsins1/postgresql']
    group_name = group_names()

    for x in group_name:
        str1=''.join(x)
        insname= str1.split('/')[4]
        response = log_file.create_export_task(
         taskName='rds_pgsql_export_task',
         logGroupName=x,
         fromTime=int((startOfhour-unix_start).total_seconds() * 1000),
         to=int((endOfhour-unix_start).total_seconds() * 1000),
         destination='aws-bucket',
         destinationPrefix='logs/log_year={}/log_month={}/log_day={}/log_hour={}/instance_name={}/exported_logs-{}'.format(startOfhour.strftime("%Y"),startOfhour.strftime("%b"),startOfhour.strftime("%d"),startOfhour.strftime("%H"),insname,startOfhour.strftime("%Y-%m-%d"))
        )
        time.sleep(10)
    return 'Response from export task at {} :\n{}'.format(datetime.now().isoformat(),response)


def group_names():
    log_file = boto3.client('logs')
    groupnames = []
    paginator = log_file.get_paginator('describe_log_groups')
    response_iterator = paginator.paginate(logGroupNamePrefix='/aws/rds/instance')
    for response in response _iterator:
        listOfResponse=response["logGroups"]
        for result in listOfResponse:
            groupnames.append(result["logGroupName"])
    return groupnames
