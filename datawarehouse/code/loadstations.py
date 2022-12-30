from google.cloud import bigquery


PROJECT_ID = "engexamspreparation" 
TABLE_ID = "{}.raw_bikesharing.trips".format(PROJECT_ID)
GCS_URI = "gs://{}-bucket/mysql_export/stations/20180102/stations.csv".format(PROJECT_ID) 

def loadgcstobigquerysnapshotdata(GCS_URI, TABLE_ID, table_schema):
    client = bigquery.Client() 
    job_config = bigquery.LoadJobConfig(
        schema = table_schema,
        source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON, 
        write_disposition = 'WRITE_TRUNCATE'
    )

    load_job = client.load_table_from_uri(
        GCS_URI, TABLE_ID, job_config=job_config 
    )
    load_job = client.load_table_from_uri(
        GCS_URI, TABLE_ID, job_config=job_config
    )
    load_job.result() 
    table = client.get_table(TABLE_ID) 

    print("Loaded {} rows to table {}".format(table.num_rows,TABLE_ID))

bigquery_table_schema = [
    bigquery.SchemaField("station_id", "STRING"),
    bigquery.SchemaField("name", "STRING"),
    bigquery.SchemaField("region_id", "STRING"),
    bigquery.SchemaField("capacity", "INTEGER")
]

if __name__ == '__main__':
    loadgcstobigquerysnapshotdata(GCS_URI, TABLE_ID, bigquery_table_schema)