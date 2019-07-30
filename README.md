# rds-cloudwatch-logs-to-s3
cw_to_s3_daily.py : Lambda function will move previous day's RDS cloudwatch logs to S3 bucket.

cw_to_s3_hourly.py : Lambda function will move previous hour RDS cloudwatch logs to S3 bucket. Should be scheduled through Cloudwatch events.

athena_table.sql : To create table in Athena.
