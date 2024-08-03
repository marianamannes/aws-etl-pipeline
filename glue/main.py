import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from s3_client import S3Client
from s3_query_loader import QueryLoader
from mysql_client import MYSQLClient
from mysql_query_handler import QueryHandler
from s3_utils import *
from utils import *

# Job Parameters
args = getResolvedOptions(sys.argv,
                          ['JOB_NAME',
                           'CSV_BUCKET',
                           'OBJECT_KEY',
                           'QUERY_BUCKET',
                           'MYSQL_USER',
                           'MYSQL_PASSWORD',
                           'MYSQL_HOST',
                           'MYSQL_DB'])

# Set up Glue
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Connect to s3
s3_client = S3Client()

# Get s3 object content
dataset = get_s3_obj_df(s3_client, 'superstore-ingestion', 'dataset_3.csv')

# Ge s3 object lenght
dataset_len = len(dataset)

# Convert dataset to 3NF
df_dict = create_distinct_dataframes(dataset,
                                     {'categories': ['Category'],
                                      'subcategories': ['Sub-Category'],
                                      'priorities': ['Order Priority'],
                                      'shipping': ['Ship Mode'],
                                      'customers': ['Customer ID', 'Customer Name'],
                                      'products': ['Product ID', 'Product Name', 'Category', 'Sub-Category'],
                                      'orders': ['Order ID', 'Order Date', 'Ship Date', 'Ship Mode', 'Customer ID', 'Order Priority'],
                                       'order_items': ['Row ID', 'Product ID', 'Order ID', 'Sales', 'Quantity', 'Discount', 'Profit', 'Shipping Cost']
                                        })

# Connect to MYSQL
mysql_client = MYSQLClient(args['MYSQL_USER'], 
                           args['MYSQL_PASSWORD'], 
                           args['MYSQL_HOST'], 
                           args['MYSQL_DB'])

# Create temporary tables to ingest data from the csv
query_loader = QueryLoader(s3_client, args['QUERY_BUCKET'])
query_handler = QueryHandler(mysql_client, query_loader, df_dict)
query_handler.create_and_populate_temp_tables()

# Insert datasets into MYSQL DW
query_handler.insert_values_to_final_tables()

# Validate ingestion
query_handler.validate_ingestion(dataset_len, 'order_items')

job.commit()
