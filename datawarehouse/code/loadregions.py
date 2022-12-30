from google.cloud import bigquery 

# THIS BE THE PROJECT ID
PROJECT_ID = "engexamspreparation" 
# THIS BE THE PUBLIC TABLE ID WE DEY EXTRACT FROM 
PUBLIC_TABLE_ID = "bigquery-public-data.san_francisco_bikeshare.bikeshare_regions"
# THIS BE THE TARGET TABLE ID WE DEY LOAD PUT INSIDE 
TARGET_TABLE_ID = "{}.raw_bikesharing.regions".format(PROJECT_ID) 

# THIS METHOD DEY LOAD THE DATA FROM PUBLIC TABLE TO TARGET TABLE 
def loaddatafrombigquery(PUBLIC_TABLE_ID, TARGET_TABLE_ID): 
    # client object 
    client = bigquery.Client() 
    # JOB CONFIURATION => THE DESTINATION TABLE THEN WRITE TRUNCATE 
    job_config = bigquery.QueryJobConfig(
        destination = TARGET_TABLE_ID, 
        write_disposition = 'WRITE_TRUNCATE' # IF TABLE EXISTS, WE DEY OVERWRITE AM 
        ) 
    
    # WE DEY USE THIS SQL QUERY EXTRACT SOME OF THE DATA 
    sql = "SELECT * FROM `{}`;".format(PUBLIC_TABLE_ID) 
    # THIS METHOD DEY RUN SQL QUERY 
    query_job = client.query(sql, job_config=job_config) 
    
    # WE DEY TRY 
    # 
    try: 
        # GET THE RESUT OF THE JOB 
        query_job.result() 
        # PRINT THE RESULT 
        print("Query success")
    # IF ERROR DEY THEN PRINT THE ERROR 
    except Exception as exception:
        print(exception) 

# RUN THE METHOD WE CREATE THEN PASS THE IDS WE GET 
if __name__ == "__main__":
    loaddatafrombigquery(PUBLIC_TABLE_ID, TARGET_TABLE_ID)
    