from s3.utils import *

class QueryLoader:
    def __init__(self, s3_client, bucket):
        self.s3 = s3_client
        self.bucket = bucket

    def get_create_temp_table_query(self):
        query = get_s3_obj_string(self.s3, self.bucket, 'glue/queries/create_temp_table.sql')
        return query
    
    def get_add_column_temp_table_query(self):
        query = get_s3_obj_string(self.s3, self.bucket, 'glue/queries/add_column_temp_table.sql')
        return query
    
    def get_add_created_at_column_temp_table_query(self):
        query = get_s3_obj_string(self.s3, self.bucket, 'glue/queries/add_created_at_column_temp_table.sql')
        return query
    
    def get_insert_temp_table_query(self):
        query = get_s3_obj_string(self.s3, self.bucket, 'glue/queries/insert_temp_table.sql')
        return query
    
    def get_general_insert_query(self):
        query = get_s3_obj_string(self.s3, self.bucket, 'glue/queries/general_insert.sql')
        return query
    
    def get_specific_table_insert_query(self, table):
        query = get_s3_obj_string(self.s3, self.bucket, f'glue/queries/{table}_table_insert.sql')
        return query
    
    def get_validate_query(self):
        query = get_s3_obj_string(self.s3, self.bucket, 'glue/queries/validate.sql')
        return query