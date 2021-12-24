import os
import mysql.connector
from mysql.connector import errorcode


class Database:
    def __init__(self) -> None:
        self.config = {
            'user': os.getenv('DB_USERNAME'),
            'password': os.getenv('DB_PASS'),
            'host': os.getenv('DB_HOST'),
            'database': os.getenv('DB_NAME'),
            'raise_on_warnings': True
        }

    def connection(self):
        try:
            cnx = mysql.connector.connect(**self.config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                exit("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                exit("Database does not exist")
            else:
                exit(err)
        else:
            if cnx.is_connected():
                print("Berhasil terhubung ke database")
            return cnx
