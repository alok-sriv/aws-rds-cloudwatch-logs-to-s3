import boto3
import collections
from datetime import datetime, timedelta, date, time

region = 'us-east-2'
def lambda_handler(event, context):
    log_file = boto3.client('logs')
    startOfDay = datetime.combine(date.today()-timedelta(1),time())
    endOfDay = datetime.combine(date.today(),time())
    unix_start = datetime(1970,1,1)
    group_name = ['/aws/rds/instance/dbinstancename/postgresql']
    for x in group_name:
        response = log_file.create_export_task(
         taskName='eip_rds_pgsql_export_task',
         logGroupName=x,
         fromTime=int((startOfDay-unix_start).total_seconds() * 1000),
         to=int((endOfDay-unix_start).total_seconds() * 1000),
         destination='S3bucketname',
         destinationPrefix='cwlogs/log_year={}/log_month={}/log_day={}/log_hour={}/exported_logs-{}'.format(startOfDay.strftime("%Y"),startOfDay.strftime("%b"),startOfDay.strftime("%d"),startOfDay.strftime("%H"),startOfDay.strftime("%Y-%m-%d"))
         )
        return 'Response from export task at {} :\n{}'.format(datetime.now().isoformat(),response)
