"""
The expense_tracking.py program is used to manage your expenses. The program connects to the database where the data is stored.
Functionalities:
- adding expense
- removal of the expense
- displaying the report
- python list display
- delete the database
- importing data from a csv file

Exemplary program launches:
# MySQL
# python expense_tracking.py add mysql 1001 "test"
# python expense_tracking.py raport mysql
# python expense_tracking.py import-csv mysql "expenses.csv" 
# python expense_tracking.py python-export mysql
# python expense_tracking.py delete mysql 1
# python expense_tracking.py drop-database mysql

# SQLite
# python expense_tracking.py add sqlite 1001 "test"
# python expense_tracking.py raport sqlite
# python expense_tracking.py import-csv sqlite "expenses.csv" 
# python expense_tracking.py python-export sqlite
# python expense_tracking.py delete sqlite 1
# python expense_tracking.py drop-database sqlite
"""

import csv
from dataclasses import dataclass
import os
import sys

import click
import mysql.connector
import sqlite3

HOST = os.environ.get('host')
USER = os.environ.get('user')
PASSWORD = os.environ.get('password_to_db')
DATABASE = os.environ.get('database')
FILENAME = 'expenses.db'
TABLE_NAME = 'list_expenses'
QUERY_SELECT = 'SELECT * FROM list_expenses'
QUERY_INSERT = 'INSERT INTO list_expenses (amount, description) VALUES (%s, %s)'
QUERY_DELETE = 'DELETE FROM list_expenses WHERE id = %s'
QUERY_CREATE_DB = 'CREATE DATABASE expenses'
QUERY_CREATE_TABLE_MYSQL = 'CREATE TABLE table_name (id INT AUTO_INCREMENT, amount DECIMAL(10,2), description VARCHAR(200), PRIMARY KEY (id))'
QUERY_CREATE_TABLE_SQLITE = 'CREATE TABLE IF NOT EXISTS table_name (id INTEGER PRIMARY KEY , amount REAL, description TEXT)'
QUERY_DROP_DATABASE_MYSQL = 'DROP DATABASE '


class Connector:
    """
    Database related class

    Method:
    - execute_on_cursor(self, query, val=None, table_name='')
    """
    def execute_on_cursor(self, query: str, val=None, table_name=''):
        '''
        Method execute SQL statment on database. First process SQL statment, next use method execute on cursor. 

        Arguments:
        - self (MySQLConnector or SQLiteConnector)
        - query (str) - SQL sentence
        - val (tuple) - special value used in SQL sentence
        - table_name (str) - name of table to SQL statment
        '''
        if val is None:
            val = []
        if type(self.connection) == sqlite3.Connection:
            query = query.replace("%s", "?")
        query = query.replace('table_name', table_name)
        self.mycursor.execute(query, val)
        if val != []:
            self.connection.commit()
        return self.mycursor.fetchall()


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

    def drop_database(self, query: str, val: str):
        query = query + val
        self.mycursor.execute(query)

    
    @classmethod
    def create_database(cls, query: str, host: str, user: str, password: str):
        connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password)
        mycursor = connection.cursor()
        mycursor.execute(query)


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


@dataclass
class Expense:
    """
    Class Expense represents single expense.

    Atributes:
    - id (None | int)
    - amount (float): amount can't be negative number
    - description (str): description can't be empty string

    Methods:
    - __repr__()
    - save_to_db(cls, db, amount, description) 
    """
    id: None
    amount: float
    description: str

    def __post_init__(self):
        if self.amount <= 0:
            raise ValueError
        if self.description == '':
            raise ValueError
    
    def __repr__(self) -> str:
        return f"Expense(id={self.id}, amount={self.amount}, description={self.description!r})"
    
    @classmethod
    def save_to_db(cls, db: Connector, amount: float, description: str):
        """
        Method create Expense object and save its to database.

        Arguments:
        - db (Connector): it's connector with database
        - amount (float)
        - description (str)
        """
        expense = cls(None, float(amount), description)
        db.execute_on_cursor(QUERY_INSERT, (expense.amount, expense.description))


def init_db_connection(choice_db: str) -> Connector:
    """
    Function returns object class MySQLConnector or object class SQLiteConnector. If database not exist, function create database and table.

    Arguments:
        choice_db (str): user starts program decide which database use (mysql or sqlite)

    Return: 
        db = MySQLConnector or SQLiteConnector
    """
    if 'sqlite' == choice_db:
        db = SQLiteConnector(FILENAME)
        db.execute_on_cursor(QUERY_CREATE_TABLE_SQLITE, table_name=TABLE_NAME)
    else:
        try: 
            db = MySQLConnector(HOST, USER, PASSWORD, DATABASE)
        except mysql.connector.errors.ProgrammingError:
            MySQLConnector.create_database(QUERY_CREATE_DB, HOST, USER, PASSWORD)
            db = MySQLConnector(HOST, USER, PASSWORD, DATABASE)
            db.execute_on_cursor(QUERY_CREATE_TABLE_MYSQL, table_name=TABLE_NAME)
    return db


def read_db(db: Connector) -> list[Expense]:
    """
    Function connect with database, select all records and return list with expenses.

    Arguments:
        db (MySQLConnector | SQLiteConnector)

    Return:
        current_expenses (list[Expense])
    """
    contents_db = db.execute_on_cursor(QUERY_SELECT)
    current_expenses = [Expense(element[0], element[1], element[2]) for element in contents_db]
    return current_expenses


def print_report(current_expenses: list[Expense]) -> None:
    """
    The function displays a report with all current expenses and total sum.
    
    Arguments:
    - currrent_expenses (list[Expense])
    """
    total = 0
    print(f'-ID--AMOUNT--BIG?--------DESCRIPTION-------')
    for expense in current_expenses:
        if expense.amount > 1000:
            big = "(!)"
        else:
            big = ' - '
        print(f'{expense.id:3} {expense.amount:7} {big:>4}     {expense.description}')
        total += expense.amount
    print(f"TOTAL = {total}")


def import_data_from_csv(db: Connector, csv_file: str) -> None:
    """
    Function read file CSV with expenses and save each expense to database.
    File CSV must be two column: AMOUNT, DESCRIPTION.

    Arguments:
    - db (MySQLConnector | SQLiteConnector)
    - csv_file (str): file name with extension
    """
    if os.path.exists(csv_file):
        with open(csv_file) as stream:
            reader = csv.DictReader(stream)
            for row in reader:
                try:
                    Expense.save_to_db(db, row['amount'], row['description'])
                except ValueError:
                    print(f"Don't correct or misscing amount or description: {row['amount']} and {row['description']}.")
    else:
        print('File is not exist.')
        raise FileNotFoundError


def print_list(current_expenses: list[Expense]) -> None:
    """
    Function print list with current expenses.

    Arguments:
    - currrent_expenses (list[Expense])
    """
    expenses_object_list = [expense.__repr__() for expense in current_expenses]
    print(expenses_object_list)


@click.group()
def cli():
    pass

@cli.command() #add
@click.argument('db_type')
@click.argument('amount', type=float)
@click.argument('description')

def add(db_type, amount, description):
    db = init_db_connection(db_type)
    try:
        Expense.save_to_db(db, amount, description)
    except ValueError:
        print("Don't correct or misscing amount or description.")
        sys.exit(1)


@cli.command() #delete
@click.argument('db_type')
@click.argument('id', type=int)

def delete(db_type, id):
    db = init_db_connection(db_type)
    db.execute_on_cursor(QUERY_DELETE, [int(id)])
    print(f'The record with id {id} has been deleted.')

@cli.command() #report
@click.argument('db_type')
def report(db_type):
    db = init_db_connection(db_type)
    current_expenses = read_db(db)
    print_report(current_expenses)


@cli.command() #python_export
@click.argument('db_type')
def python_export(db_type):
    db = init_db_connection(db_type)
    current_expenses = read_db(db)
    print_list(current_expenses)


@cli.command() #import csv
@click.argument('db_type')
@click.argument('csv_file')

def import_csv(db_type, csv_file):
    db = init_db_connection(db_type)
    try:
        import_data_from_csv(db, csv_file)
    except FileNotFoundError:
        print('File is not exist.')
        sys.exit(1)
    

@cli.command() #drop_database
@click.argument('db_type')

def drop_database(db_type):
    db = init_db_connection(db_type)
    if type(db) == MySQLConnector:
        val = os.environ.get("database")
        db.drop_database(QUERY_DROP_DATABASE_MYSQL, val)
    else:
        db.connection.close()
        os.remove(FILENAME)


if __name__ == "__main__":
    cli()
