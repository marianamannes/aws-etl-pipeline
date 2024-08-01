import mysql.connector
import datetime
import time

class MYSQLConnector:
    def __init__(self, user, password, host, db, df_dict):
        print('--- Creating MYSQL connection ---')
        self.user = user
        self.password = password
        self.host = host
        self.database = db
        self.cnx = mysql.connector.connect(user=self.user, 
                                           password=self.password,
                                           host=self.host,
                                           database=self.database)
        try:
            if self.cnx.is_connected():
                print("MYSQL connection created")
            else:
                print("Error in MYSQL connection")
        except Error as e:
            print(f"Error in MYSQL connection: {e}")

        self.cursor = self.cnx.cursor()
        self.df_dict = df_dict
        self.timestamp_now = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    def create_temp_tables(self):
        print('--- Creating and ingesting data to temporary tables ---')
        for key, value in self.df_dict.items():
            tmp_table_name = key + '_tmp'
            create_table_query = open('glue/queries/create_temp_table.sql', 'r').read().format(tmp_table_name)
            self.cursor.execute(create_table_query)
            for i in value:
                column_name = i.lower().replace(' ', '_').replace('-', '')
                value.rename(columns={i:column_name}, inplace=True)
                add_column_query = open('glue/queries/add_column_temp_table.sql', 'r').read().format(table = tmp_table_name, column = column_name)
                self.cursor.execute(add_column_query)
            add_created_at_column_query = open('glue/queries/add_created_at_column_temp_table.sql', 'r').read().format(table = tmp_table_name)
            self.cursor.execute(add_created_at_column_query)
            columns = list(value)
            columns.append('created_at')
            insert_query = open('glue/queries/insert_temp_table.sql', 'r').read() + ('(' + len(columns) * '%s, ' + ')').replace(', )', ')')
            insert_query = insert_query.format(table = tmp_table_name, columns = str(columns).replace("'", "").replace('[', '')).replace(']', '')
            value['created_at'] = self.timestamp_now
            self.cursor.executemany(insert_query, value.values.tolist())
            self.cnx.commit()
            print('Temporary table ' + str(tmp_table_name) + ' created and populated')

    def insert_values(self):
        print('--- Inserting data to final tables ---')
        for key, value in self.df_dict.items():
           if key not in ('products', 'orders', 'customers', 'order_items'):
              general_insert_query = open('glue/queries/general_insert.sql', 'r').read().format(table = key, table_tmp = key + '_tmp', column = list(value)[0].lower().replace(' ', '_'))
              self.cursor.execute(general_insert_query)
              print(key + ' table: ' + str(self.cursor.rowcount) + ' rows inserted')
              self.cnx.commit()
           else:
              custom_insert_query = open('glue/queries/{}_table_insert.sql'.format(key), 'r').read()
              self.cursor.execute(custom_insert_query)
              print(key + ' table: ' + str(self.cursor.rowcount) + ' rows inserted')
              self.cnx.commit()

    def validate_ingestion(self, dataset_len, table):
        print('--- Validating ingestion ---')
        validate_query = open('glue/queries/validate.sql', 'r').read().format(table = table, timestamp = self.timestamp_now)
        self.cursor.execute(validate_query)
        table_len = self.cursor.fetchone()[0]
        print('Dataset length: ' + str(dataset_len))
        print('Inserted to ' + table + ' : ' + str(table_len))
        if dataset_len == table_len:
            print('Successful ingestion')
        else:   
            print('ERROR')
        self.cursor.close()
        