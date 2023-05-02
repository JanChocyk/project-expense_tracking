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
QUERY_SELECT = 'SELECT * FROM list_expenses'
QUERY_INSERT = 'INSERT INTO list_expenses (amount, description) VALUES (%s, %s)'
QUERY_DELETE = 'DELETE FROM list_expenses WHERE id = %s'
QUERY_CREATE_DB = 'CREATE DATABASE expenses'
QUERY_CREATE_TABLE_MYSQL = 'CREATE TABLE list_expenses (id INT AUTO_INCREMENT, amount DECIMAL(10,2), description VARCHAR(200), PRIMARY KEY (id))'
QUERY_CREATE_TABLE_SQLITE = 'CREATE TABLE IF NOT EXISTS list_expenses (id INTEGER PRIMARY KEY , amount REAL, description TEXT)'
QUERY_DROP_DATABASE_MYSQL = 'DROP DATABASE '


class Connector:
    def execute_on_cursor(self, query, val=None):
        if val is None:
            val = []
        if type(self.connection) == sqlite3.Connection:
            query = query.replace("%s", "?")
        self.mycursor.execute(query, val)
        if val != []:
            self.connection.commit()
        return self.mycursor.fetchall()


class MySQLConnector(Connector):
    """
    A class represent connection with database.
    ...
    Atributes
    -------------
    connection = mysql.connector.connection.MySQLConnection
        Create connection with database.
    mycursor = mysql.connector.cursor.MySQLCursor
        Create cursor object.
    """
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
        self.mycursor = self.connection.cursor()

    def drop_database(self, query, val):
        query = query + val
        self.mycursor.execute(query)

    @classmethod
    def create_table(cls, query):
        db = cls(HOST, USER, PASSWORD, DATABASE)
        db.mycursor.execute(query)
        return db
    
    @classmethod
    def create_database(cls, query, host, user, password):
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
    def __init__(self):
        self.connection = sqlite3.connect(FILENAME)
        self.mycursor = self.connection.cursor()


@dataclass
class Expense:
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
    def save_to_db(cls, db, amount, description):
        expense = cls(None, float(amount), description)
        return db.execute_on_cursor(QUERY_INSERT, (expense.amount, expense.description))


def init_db_connection(choice_db: str) -> Connector:
    """
    Returns object class MySQLConnector or object class SQLiteConnector.

    Parameters:
        choice_db = str
    Return: 
        db = MySQLConnector or SQLiteConnector
    """
    if 'sqlite' == choice_db:
        db = SQLiteConnector()
        db.execute_on_cursor(QUERY_CREATE_TABLE_SQLITE)
    else:
        try: 
            db = MySQLConnector(HOST, USER, PASSWORD, DATABASE)
        except mysql.connector.errors.ProgrammingError:
            MySQLConnector.create_database(QUERY_CREATE_DB, HOST, USER, PASSWORD)
            MySQLConnector.create_table(QUERY_CREATE_TABLE_MYSQL)
            db = MySQLConnector(HOST, USER, PASSWORD, DATABASE)
    return db


def read_db(db: Connector) -> list[Expense]:
    """
    Return list with expenses from database.
    Parametres:
        db = MySQLConnector or SQLiteConnector
        query = str
        It is SQL statment.
    Return:
        current_expenses = list[Expense]
    """
    contents_db = db.execute_on_cursor(QUERY_SELECT)
    current_expenses = [Expense(element[0], element[1], element[2]) for element in contents_db]
    return current_expenses


def print_raport(current_expenses: list[Expense]) -> None:
    """The function displays a report with all current expenses and total sum."""
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


# czy taka adnotacja typów z or może być?
def import_data_from_csv(db: Connector, csv_file: str) -> None:
    """Function read file CSV with expenses and save each expense to database.
       File CSV must be two column: AMOUNT, DESCRIPTION.
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
    """Function print list with current expenses."""
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

@cli.command() #raport
@click.argument('db_type')
def raport(db_type):
    db = init_db_connection(db_type)
    current_expenses = read_db(db)
    print_raport(current_expenses)


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
    import_data_from_csv(db, csv_file)
    

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
