import mysql.connector
from mysql.connector import Error

from .readConfigFile import *

# Definierung der Verbindungsfunktion
def connect():
    try:
        params = read_db_params()

        # Verbinde mit der Datenbank
        # Liest die Datenbank Parameter von dem Config Objekt
        conn = mysql.connector.connect(
            host=params.get('DB', 'host'),
            database=params.get('DB', 'database'),
            user=params.get('DB', 'user'),
            password=params.get('DB', 'password'),
            port=params.get('DB', 'port')
            )
        return conn
    except(Exception, Error) as error:
        print(error)