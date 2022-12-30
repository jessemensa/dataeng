from google.cloud import bigquery 

# -------------------------------------------------------------
# UNCOMMENT AND READ THE CODE BELOW TO UNDERSTAND HOW TO LOAD DATA FROM GCS TO BIGQUERY
# from google.cloud import bigquery

# # Construct a BigQuery client object.
# client = bigquery.Client()

# # TODO(developer): Set table_id to the ID of the table to create.
# # table_id = "your-project.your_dataset.your_table_name"

# job_config = bigquery.LoadJobConfig(
#     schema=[
#         bigquery.SchemaField("name", "STRING"),
#         bigquery.SchemaField("post_abbr", "STRING"),
#     ],
#     skip_leading_rows=1,
#     # The source format defaults to CSV, so the line below is optional.
#     source_format=bigquery.SourceFormat.CSV,
# )
# uri = "gs://cloud-samples-data/bigquery/us-states/us-states.csv"

# load_job = client.load_table_from_uri(
#     uri, table_id, job_config=job_config
# )  # Make an API request.

# load_job.result()  # Waits for the job to complete.

# destination_table = client.get_table(table_id)  # Make an API request.
# print("Loaded {} rows.".format(destination_table.num_rows))



# -------------------------------------------------------------


# CHANGE PROJECT ID 
# this be the project id 
PROJECT_ID = "engexamspreparation" 
# "gs://{}-data-bucket/from-git/chapter-3/dataset/trips/20180101/*.json".format(project_id)
# engexamspreparation-bucket/trips/20180101
# this be where the data be located for google cloud storage 
GCS_URI = "gs://{}-bucket/trips/20180101/*.json".format(PROJECT_ID)
# this be the table id, we dey tap into the project id dn connect to am plus the dataset name 
TABLE_ID = "{}.raw_bikesharing.trips".format(PROJECT_ID) 

# we dey create the client object 
client = bigquery.Client() 

# this method dey load the data from google cloud storage to bigquery 
# e dey take location of the data in gcs, the table id we dey load into then the table schema 
def loadgcstobigqueryeventdata(GCS_URI, TABLE_ID, table_schema): 
    # this be configuration options we dey take load the jobs 
    job_config = bigquery.LoadJobConfig(
        schema = table_schema, # this be table schema 
        source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON, # file format for the data be json 
        write_disposition = 'WRITE_APPEND' # if the table already exist, we dey append the data to the table
    )

    # go load the data to CLOUD STORAGE 
    load_job = client.load_table_from_uri(
        GCS_URI, TABLE_ID, job_config=job_config
    )
    # THIS DET THE QUERYJOB INSIDE 
    load_job.result() 
    # this go get the table based on table id, passes in the get the table 
    table = client.get_table(TABLE_ID) 

    print("Loaded {} rows into {}:{}.".format(table.num_rows, PROJECT_ID, TABLE_ID)) 

# this be the table schema of how we want make e be 
bigquery_table_schema = [
    bigquery.SchemaField("trip_id", "STRING"),
    bigquery.SchemaField("duration_sec", "INTEGER"),
    bigquery.SchemaField("start_date", "TIMESTAMP"),
    bigquery.SchemaField("start_station_name", "STRING"),
    bigquery.SchemaField("start_station_id", "STRING"),
    bigquery.SchemaField("end_date", "TIMESTAMP"),
    bigquery.SchemaField("end_station_name", "STRING"),
    bigquery.SchemaField("end_station_id", "STRING"),
    bigquery.SchemaField("member_gender", "STRING")
]

# this main method go run the function 
if __name__ == '__main__':
    loadgcstobigqueryeventdata(GCS_URI, TABLE_ID, bigquery_table_schema)
