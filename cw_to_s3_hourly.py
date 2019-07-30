import boto3
import collections
from datetime import datetime, timedelta, date, time

region = 'us-east-2'
def lambda_handler(event, context):
    log_file = boto3.client('logs')
    now=datetime.now()
    startOfhour = now.replace(minute=0,second=0, microsecond=0)-timedelta(hours=1)
    endOfhour = now.replace(minute=0,second=0, microsecond=0)
    unix_start = datetime(1970,1,1)
    group_name = ['/aws/rds/instance/dbinstancename/postgresql']
    for x in group_name:
        response = log_file.create_export_task(
         taskName='rds_pgsql_export_task',
         logGroupName=x,
         fromTime=int((startOfhour-unix_start).total_seconds() * 1000),
         to=int((endOfhour-unix_start).total_seconds() * 1000),
         destination='S3bucketname',
         destinationPrefix='cwlogs/log_year={}/log_month={}/log_day={}/log_hour={}/exported_logs-{}'.format(startOfhour.strftime("%Y"),startOfhour.strftime("%b"),startOfhour.strftime("%d"),startOfhour.strftime("%H"),startOfhour.strftime("%Y-%m-%d"))
         )
        return 'Response from export task at {} :\n{}'.format(datetime.now().isoformat(),response)
