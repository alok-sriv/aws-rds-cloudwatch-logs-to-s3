CREATE EXTERNAL TABLE `postgres_hourly_logs`(
  `logtime1` string COMMENT '', 
  `logtime` timestamp COMMENT 'Log timestamp', 
  `tz` string COMMENT 'Log timezone', 
  `client` string COMMENT 'Client IP or hostname', 
  `clientport` int COMMENT 'Client port', 
  `username` string COMMENT 'DB username making connection to database', 
  `dbname` string COMMENT ' database name', 
  `serverport` int COMMENT ' server port', 
  `log_level` string COMMENT ' Indicating log level i.e LOG,ERROR,FATAL,DETAILED', 
  `log_type1` string COMMENT ' Classification of event i.e connection, disconnection , audit', 
  `duration` decimal(38,6) COMMENT ' Applicable for timed queries (ms)', 
  `log_type2` string COMMENT '', 
  `message` varchar(40000) COMMENT ' Postgresql log message')
PARTITIONED BY ( 
  `log_year` int, 
  `log_month` varchar(20), 
  `log_day` int, 
  `log_hour` int)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.serde2.RegexSerDe' 
WITH SERDEPROPERTIES ( 
  'input.regex'='^(\\S+)\\s(\\d{4}-\\d{2}-\\d{2}\\s\\d{2}:\\d{2}:\\d{2})\\s(\\S+):\\[?(\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}|[\\w\\.-]+)?\\]?\\(?(\\d+)?\\)?:\\[?(\\w+)?\\]?@\\[?(\\w+)?\\]?:\\[?(\\d+)?\\]?:(\\w+)?:\\s*(\\w+):?\\s*(\\d+\\.\\d+)?(?:\\s\\w+)?\\s*(\\w+)?:?(.*)', 
  'timestamp.formats'='yyyy-MM-dd HH:mm:ss') 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://bucketname/cwlogs'
