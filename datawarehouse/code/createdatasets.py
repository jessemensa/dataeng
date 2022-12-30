
from google.cloud import bigquery
from google.cloud.exceptions import NotFound 

# Construct a BigQuery client object.
client = bigquery.Client()

# -------------------------------------------------------------
# -------------------------------------------------------------

# CREATE A LIST OF DATASETS WE WILL CREATE 
datasetsname = ['raw_bikesharing', 'dwh_bikesharing', 'dm_bikesharing']
location = 'US' 

# CREATE A FUNCTION 
def createbigquerydataset(datasetname):
    # CREATE A BIGQUERY DATASET 
    # CHECK IF DATASET EXISTS 
    # ARGS: DATASET_NAME: STRING  
    dataset_id = "{}.{}".format(client.project, datasetname) # client.project param dey get the project id dn dot am plus dataset name for the list inside 
    # exceptions 
    # we dey try get 
    try: 
        # client object dey tap into get_Dataset method dn pass the dataset id for inside 
        client.get_dataset(dataset_id) 
        # we go print the dataset_id if e already dey exist 
        print("Dataset {} already exists".format(dataset_id)) 
    # if we no get ah then 
    except NotFound: 
        # we go call bigQuery dn tap into Dataset class dn put dataset id as in dataset refrence, this go point we to the dataset_id variable we create 
        dataset = bigquery.Dataset(dataset_id) 
        # then get the dataset in location 
        dataset.location = location 
        # client object go tap into create_dataset method dn pass the dataset variable for inside dn create the dataset 
        dataset = client.create_dataset(dataset, timeout=30) # create the dataset 
        # we go print the project id dot tap into dataset dn get the dataset id 
        print("Created dataset {}.{}".format(client.project, dataset.dataset_id))

# for run through whatever dey the datasetsname list inside 
for name in datasetsname:
    # put am for the createbigquerydataset function inside 
    createbigquerydataset(name)
