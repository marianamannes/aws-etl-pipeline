import boto3
import pandas as pd

class S3Connector:
    def __init__(self, df_bucket, query_bucket):
        print('--- Creating S3 connection ---')
        self.s3_resource = boto3.client("s3")
        self.df_bucket = df_bucket
        self.query_bucket = query_bucket
        print('S3 connection created')

    def get_object(self, bucket, objectkey):
        obj = self.s3_resource.get_object(Bucket=bucket, Key=objectkey)
        return obj

    def get_df(self, objectkey):
        obj = self.get_object(self.df_bucket, objectkey)
        df = pd.read_csv(obj['Body'], index_col=None)
        return df, len(df)
    
    def get_query(self, objectkey):
        obj = self.get_object(self.query_bucket, objectkey)
        obj_string = obj['Body'].read().decode('utf-8')
        return obj_string
    
    def get_create_temp_table_query(self):
        query = self.get_query('glue/queries/create_temp_table.sql')
        return query
    
    def get_add_column_temp_table_query(self):
        query = self.get_query('glue/queries/add_column_temp_table.sql')
        return query
    
    def get_add_created_at_column_temp_table_query(self):
        query = self.get_query('glue/queries/add_created_at_column_temp_table.sql')
        return query
    
    def get_insert_temp_table_query(self):
        query = self.get_query('glue/queries/insert_temp_table.sql')
        return query
    
    def get_general_insert_query(self):
        query = self.get_query('glue/queries/general_insert.sql')
        return query
    
    def get_specific_table_insert_query(self, table):
        query = self.get_query(f'glue/queries/{table}_table_insert.sql')
        return query
    
    def get_validate_query(self):
        query = self.get_query('glue/queries/validate.sql')
        return query