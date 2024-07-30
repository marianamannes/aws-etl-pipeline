import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from s3_client import S3Connector
from normalize import Normalizer
from mysql_client import MYSQLConnector

# Job Parameters
args = getResolvedOptions(sys.argv,
                          ['JOB_NAME',
                           'BUCKET_NAME',
                           'OBJECT_KEY',
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
s3_client = S3Connector()

# Get s3 object content
dataset, dataset_len = s3_client.get_object('superstore-ingestion', 'dataset_1.csv')

# Convert dataset to 3NF
df_dict = Normalizer(dataset).create_distinct_dataframes({'categories': ['Category'],
                                                         'subcategories': ['Sub-Category'],
                                                         'priorities': ['Order Priority'],
                                                         'shipping': ['Ship Mode'],
                                                         'customers': ['Customer ID', 'Customer Name'],
                                                         'products': ['Product ID', 'Product Name', 'Category', 'Sub-Category'],
                                                         'orders': ['Order ID', 'Order Date', 'Ship Date', 'Ship Mode', 'Customer ID', 'Order Priority'],
                                                         'order_items': ['Row ID', 'Product ID', 'Order ID', 'Sales', 'Quantity', 'Discount', 'Profit', 'Shipping Cost']
                                                         })

# Connect to MYSQL
mysql_conn = MYSQLConnector(args['MYSQL_USER'], 
                            args['MYSQL_PASSWORD'], 
                            args['MYSQL_HOST'], 
                            args['MYSQL_DB'],
                            df_dict)

# Create temporary tables to ingest data from the csv
mysql_conn.create_temp_tables()

# Insert datasets into MYSQL DW
mysql_conn.insert_values()

# Validate ingestion
mysql_conn.validate_ingestion(dataset_len, 'order_items')

job.commit()
