

from airflow import DAG
# what is this operator doing ?? 
# from airflow.contrib.operators.gcp_sql_operator import CloudSqlInstanceExportOperator
from airflow.providers.google.cloud.operators.sql import CloudSqlInstanceExportOperator
# from airflow.providers.google.cloud.operators.cloud_sql import (
#     CloudSQLCreateInstanceDatabaseOperator,
#     CloudSQLCreateInstanceOperator,
#     CloudSQLDeleteInstanceDatabaseOperator,
#     CloudSQLDeleteInstanceOperator,
#     CloudSQLExportInstanceOperator,
#     CloudSQLImportInstanceOperator,
#     CloudSQLInstancePatchOperator,
#     CloudSQLPatchInstanceDatabaseOperator,
# )
# Using GCS storage for a BigQuery operator
# from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
# from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
# BIGQUERY OPERATOR FOR DATA TRANSFORMATION 
from airflow.providers.google.cloud.operators.bigquery import BigQueryOperator
# from airflow.contrib.operators.bigquery_operator import BigQueryOperator

from airflow.utils.dates import days_ago

args = {
    'owner': 'jesse-mensah',
}

GCP_PROJECT_ID = 'engexamspreparation'
INSTANCE_NAME = 'mysql-instance'
EXPORT_URI = 'gs://engexamspreparation-bucket/stations/stations.csv'
SQL_QUERY = "SELECT * FROM apps_db.stations"

export_body = {
    "exportContext": {
        "fileType": "csv",
        "uri": EXPORT_URI,
        "csvExportOptions":{
            "selectQuery": SQL_QUERY
        }
    }
}

with DAG(
    dag_id='level_2_dag_load_bigquery',
    default_args=args,
    schedule_interval='0 5 * * *',
    start_date=days_ago(1),
) as dag:
    # The body will contain information about how you want to extract your data.
    sql_export_task = CloudSqlInstanceExportOperator(
        project_id=GCP_PROJECT_ID, 
        body=export_body, 
        instance=INSTANCE_NAME, 
        task_id='sql_export_task'
    )
    # load stations table to bigquery 
    gcs_to_bq_example = GCSToBigQueryOperator(
    task_id                             = "gcs_to_bq_example",
    bucket                              = 'engexamspreparation-bucket',
    source_objects                      = ['stations/stations.csv'],
    destination_project_dataset_table   ='raw_bikesharing.stations',
    schema_fields=[
        {'name': 'station_id', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'name', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'region_id', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'capacity', 'type': 'INTEGER', 'mode': 'NULLABLE'}
    ],
    write_disposition='WRITE_TRUNCATE'
    )
    # DATATRANSFORMATION BIGQUERY TO BIGQUERY 
    bq_to_bq  = BigQueryOperator(
        task_id                     = "bq_to_bq",
        sql                         = "SELECT count(*) as count FROM `raw_bikesharing.stations`",
        destination_dataset_table   = 'dwh_bikesharing.temporary_stations_count',
        write_disposition           = 'WRITE_TRUNCATE',
        create_disposition          = 'CREATE_IF_NEEDED',
        use_legacy_sql              = False,
        priority                    = 'BATCH'
    )

    sql_export_task >> gcs_to_bq_example >> bq_to_bq

if __name__ == "__main__":
    dag.cli()