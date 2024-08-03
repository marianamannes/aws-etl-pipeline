import mysql.connector

class MYSQLClient:
    def __init__(self, user, password, host, db,):
        print('--- Creating MYSQL connection ---')
        self.user = user
        self.password = password
        self.host = host
        self.database = db
        self.cnx = mysql.connector.connect(user=self.user, 
                                           password=self.password,
                                           host=self.host,
                                           database=self.database)
        self.cursor = self.cnx.cursor()
        if self.cnx.is_connected():
            print("MYSQL connection created")
        else:
            print("Error in MYSQL connection")

    def run_query(self, query):
        self.cursor.execute(query)
        self.cnx.commit()

    def run_batch_query(self, query, list):
        self.cursor.executemany(query, list)
        self.cnx.commit()

    def get_row_count(self):
        row_count = self.cursor.rowcount
        return row_count
    
    def fetch_query(self, query):
        self.cursor.execute(query)
        result = self.cursor.fetchone()[0]
        return result
    
    def close_cursor(self):
        self.cursor.close()