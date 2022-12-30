cloudstoragebucketname = engexamspreparation-bucket

bucket_name=[your gcs bucket name]
gcloud sql export csv mysql-instance-source \
gs://engexamspreparation-bucket/mysql_export/stations/20180101/stations.csv \
--database=apps_db \
--offload \
--query='SELECT * FROM stations WHERE station_id <= 200;'
gcloud sql export csv mysql-instance-source \
gs://engexamspreparation-bucket/mysql_export/stations/20180102/stations.csv \
--database=apps_db \
--offload \
--query='SELECT * FROM stations WHERE station_id <=400;'

SUCCESSFUL 

NOW DELETE MYSQL INSTANCE FROM RUNNING 
gcloud sql instances delete mysql-instance-source
