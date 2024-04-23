import time
from mysql.connector import (connection)


class DbConnection:

    def __init__(self, username, password, host, db_name):
        self.cnx = connection.MySQLConnection(user=username, password=password,
                                              host=host,
                                              database=db_name)
        self.cursor = self.cnx.cursor(buffered=True)
        self.record_counter = 0

    def close_connection(self):
        self.cnx.close()

    def increase_counter(self):
        self.record_counter = self.record_counter + 1

    def commit_transaction_if_more_than_100(self):
        if self.record_counter > 100:
            self.cnx.commit()
            self.record_counter = 0

    def commit_transaction(self):
            self.cnx.commit()
            self.record_counter = 0