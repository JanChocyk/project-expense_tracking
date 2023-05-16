import os
import shelve

import mysql.connector
import sqlite3


FILENAME = os.environ.get('NAME_DB')
QUERY_SELECT = 'SELECT * FROM list_expenses'
QUERY_INSERT = 'INSERT INTO list_expenses (amount, description) VALUES (%s, %s)'
QUERY_DELETE = 'DELETE FROM list_expenses WHERE id = %s'
QUERY_CREATE_DB = 'CREATE DATABASE expenses'
QUERY_CREATE_TABLE_MYSQL = 'CREATE TABLE list_expenses (id INT AUTO_INCREMENT, amount DECIMAL(10,2), description VARCHAR(200), PRIMARY KEY (id))'
QUERY_CREATE_TABLE_SQLITE = 'CREATE TABLE IF NOT EXISTS list_expenses (id INTEGER PRIMARY KEY , amount REAL, description TEXT)'
QUERY_DROP_DATABASE_MYSQL = 'DROP DATABASE expenses'


class Connector:
    """
    A class representing all connectors.
    """
    def execute_on_cursor(self, query: str, val=None):
        '''
        Method execute SQL statment on database. First process SQL statment, next use method execute on cursor. 

        Arguments:
        - query - SQL sentence
        - val - special value used in SQL sentence. Type: list or tuple.
        '''
        if val is None: 
            val = []
        self.mycursor.execute(query, val)
        if val != []:
            self.connection.commit()
        return self.mycursor.fetchall()
    

    def drop_database(self):
        print('The database has been droped.')


class MySQLConnector(Connector):
    """
    A class represent connection with database in MySQL. Class is a descendant of a class Connector.
    
    Atributes:
    - connection (mysql.connector.connection.MySQLConnection): connection with database.
    - mycursor (mysql.connector.cursor.MySQLCursor): created cursor on self.connection
    
    Methods:
    - drop_database - method drop database
    - create_database
    """
    def __init__(self, host: str, user: str, password: str, database: str):
        self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
        self.mycursor = self.connection.cursor()


    def drop_database(self):
        query = QUERY_DROP_DATABASE_MYSQL
        self.mycursor.execute(query)
        return super().drop_database()    

    
    @classmethod
    def prepare_database(cls, host: str, user: str, password: str, database: str):
        connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password)
        mycursor = connection.cursor()
        mycursor.execute(QUERY_CREATE_DB)
        connection.close()
        db = cls(host, user, password, database)
        db.execute_on_cursor(QUERY_CREATE_TABLE_MYSQL)
        return db


class SQLiteConnector(Connector):
    """
    A class represent connection with database.
    ...
    Atributes
    -------------
    connection = sqlite3.Connection
        Create connection with database.
    mycursor = sqlite3.Cursor
        Create cursor object.
    """
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.mycursor = self.connection.cursor()

    
    def execute_on_cursor(self, query: str, val=None):
        if type(self.connection) == sqlite3.Connection:
            query = query.replace("%s", "?")
        return super().execute_on_cursor(query, val)
    

    def drop_database(self):
        self.connection.close()
        name_db = FILENAME
        os.remove(name_db)
        return super().drop_database()  


    @classmethod
    def prepare_database(cls, db_name):
        db = cls(db_name)
        db.execute_on_cursor(QUERY_CREATE_TABLE_SQLITE)
        return db
    

def check_db_config():
    try:
        shelf = shelve.open('config')
        choice_db = shelf['choice_db']
        shelf.close()
    except KeyError:
        choice_db = set_choice_db('unknown')
    return choice_db

def set_choice_db(current_db):
    shelf = shelve.open('config')
    shelf['choice_db'] = current_db
    choice_db = choice_db = shelf['choice_db']
    shelf.close()
    return choice_db
