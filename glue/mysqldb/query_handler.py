
from mysqldb.utils import *

class QueryHandler:
    def __init__(self, mysql_client, query_loader, df_dict):
        self.mysql = mysql_client
        self.query_loader = query_loader
        self.df_dict = df_dict
        self.timestamp_now = get_timestamp_now()

    def _create_temp_table(self, tmp_table_name):
        create_table_query = self.query_loader.get_create_temp_table_query().format(tmp_table_name)
        self.mysql.run_query(create_table_query)

    def _add_columns_to_temp_table(self, tmp_table_name, df):
        for col in df.columns:
            column_name = col.lower().replace(' ', '_').replace('-', '')
            df.rename(columns={col: column_name}, inplace=True)
            add_column_query = self.query_loader.get_add_column_temp_table_query().format(table=tmp_table_name, column=column_name)
            self.mysql.run_query(add_column_query)

    def _add_created_at_column(self, tmp_table_name):
        add_created_at_column_query = self.query_loader.get_add_created_at_column_temp_table_query().format(table=tmp_table_name)
        self.mysql.run_query(add_created_at_column_query)

    def _insert_data_into_temp_table(self, tmp_table_name, df):
            columns = list(df.columns)
            columns.append('created_at')
            insert_query = self.query_loader.get_insert_temp_table_query() + ('(' + len(columns) * '%s, ' + ')').replace(', )', ')')
            insert_query = insert_query.format(table=tmp_table_name, columns=', '.join(columns))
            df['created_at'] = self.timestamp_now
            self.mysql.run_batch_query(insert_query, df.values.tolist())

    def create_and_populate_temp_tables(self):
        print('--- Creating and ingesting data to temporary tables ---')
        for key, df in self.df_dict.items():
            tmp_table_name = key + '_tmp'
            self._create_temp_table(tmp_table_name)
            self._add_columns_to_temp_table(tmp_table_name, df)
            self._add_created_at_column(tmp_table_name)
            self._insert_data_into_temp_table(tmp_table_name, df)
            print('Temporary table ' + str(tmp_table_name) + ' created and populated')

    def _insert_general_data(self, table_name, df):
        general_insert_query = self.query_loader.get_general_insert_query().format(table=table_name, table_tmp=table_name + '_tmp', column=list(df)[0].lower().replace(' ', '_'))
        self.mysql.run_query(general_insert_query)

    def _insert_custom_data(self, table_name):
        custom_insert_query = self.query_loader.get_specific_table_insert_query(table_name)
        self.mysql.run_query(custom_insert_query)

    def insert_values_to_final_tables(self):
        print('--- Inserting data to final tables ---')
        for key, df in self.df_dict.items():
            if key not in ('products', 'orders', 'customers', 'order_items'):
                self._insert_general_data(key, df)
            else:
                self._insert_custom_data(key)
            print(f'{key} table: {self.mysql.get_row_count()} rows inserted')

    def validate_ingestion(self, dataset_len, table):
        print('--- Validating ingestion ---')
        validate_query = self.query_loader.get_validate_query().format(table = table, timestamp = self.timestamp_now)
        table_len = self.mysql.fetch_query(validate_query)
        print('Dataset length: ' + str(dataset_len))
        print('Inserted to ' + table + ' : ' + str(table_len))
        if dataset_len == table_len:
            print('Successful ingestion')
        else:   
            print('ERROR')
        self.mysql.close_cursor()
        