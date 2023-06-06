"""
Usage:
    python expense_tracking_main.py <command> <command_parametrs...>

Commands and parameters:
    configuration
    add <amount:float> <description: str>
    import-csv <filename: str>
    report
    delete <number_record_ID: int>
    drop-database
    python-export

Enviromental variables:
    Make sure you have the following environment variables created:
    HOST='hostname' (e.g. 'localhost')
    USER='username' (e.g. 'root')
    DATABASE='database_name' (e.g. 'expenses')
    PASSWORD='password'
    FILENAME='filename' (only for SQLite)

"""

import csv
from dataclasses import dataclass
import os
import sys

import click

from config_db import *

HOST = os.environ.get('HOST')
USER = os.environ.get('USER')
PASSWORD = os.environ.get('PASSWORD_TO_DB')
DATABASE = os.environ.get('DATABASE')
FILENAME = os.environ.get('NAME_DB')


@dataclass
class Expense:
    """
    Class Expense represents single expense.
    """
    id: None
    amount: float
    description: str


    def __post_init__(self):
        if self.amount <= 0:
            raise ValueError('Amount must be greater than zero.')
        if self.description == '':
            raise ValueError('Description can not be empty string.')
    

    @classmethod
    def save_to_db(cls, db: Connector, amount: float, description: str):
        """
        Method create Expense object and save its to database. 
        """
        expense = cls(None, float(amount), description)
        db.execute_on_cursor(QUERY_INSERT, (expense.amount, expense.description))


def init_db_connection(chosen_db: str) -> Connector:
    """
    Function check configuration database and returns object class MySQLConnector or object class SQLiteConnector. If database not exist, function create database and table.
    """
    if chosen_db == 'mysql':
        db = MySQLConnector(HOST, USER, PASSWORD, DATABASE)
    elif chosen_db == 'sqlite':
        db = SQLiteConnector(os.environ.get('NAME_DB'))    
    else:
        raise ValueError('Missing configuration. Set configuration command: python expens_tracking.py configuration.')
    return db


def read_db(db: Connector) -> list[Expense]:
    """
    Function connect with database, select all records and return list with expenses.
    """
    contents_db = db.execute_on_cursor(QUERY_SELECT)
    current_expenses = [Expense(element[0], element[1], element[2]) for element in contents_db]
    return current_expenses


def print_report(current_expenses: list[Expense]) -> None:
    """
    The function displays a report with all current expenses and total sum.
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
    File CSV must be two column: AMOUNT, DESCRIPTION.
    """
    with open(csv_file) as stream:
        reader = csv.DictReader(stream)
        for row in reader:
            try:
                Expense.save_to_db(db, row['amount'], row['description'])
            except ValueError:
                print(f"Don't correct or misscing amount or description: {row['amount']} and {row['description']}.")


def print_list(current_expenses: list[Expense]) -> None:
    """
    Function print list with current expenses.
    """
    expenses_object_list = [expense.__repr__() for expense in current_expenses]
    print(expenses_object_list)


@click.group()
def cli():
    pass

@cli.command() #configuration

def configuration():
    choice_db = input('Which database to choose: MySQL or SQLite? Type "--m" or "--s": ')
    if choice_db == '--m':
        MySQLConnector.prepare_database(HOST, USER, PASSWORD, DATABASE)
        print("Database created. You need to create the 'CHOSEN_DB' environment variable with the value 'mysql'.")
    elif choice_db == '--s':
        SQLiteConnector.prepare_database(FILENAME)
        print("Database created. You need to create the 'CHOSEN_DB' environment variable with the value 'sqlite'.")
    else:
        print('Incorrect data has been entered.')


@cli.command() #add
@click.argument('amount', type=float)
@click.argument('description')

def add(amount, description):
    try: 
        db = init_db_connection(os.environ.get('CHOSEN_DB'))
    except ValueError:
        print('Missing configuration. Set configuration command: python expens_tracking.py configuration.')
        sys.exit(1)
    try:
        Expense.save_to_db(db, amount, description)
    except ValueError:
        print("Don't correct or misscing amount or description.")
        sys.exit(1)


@cli.command() #delete
@click.argument('id', type=int)

def delete(id):
    try: 
        db = init_db_connection(os.environ.get('CHOSEN_DB'))
    except ValueError:
        print('Missing configuration. Set configuration command: python expens_tracking.py configuration.')
        sys.exit(1)
    db.execute_on_cursor(QUERY_DELETE, [int(id)])
    print(f'The record with id {id} has been deleted.')

@cli.command() #report
def report():
    try: 
        db = init_db_connection(os.environ.get('CHOSEN_DB'))
    except ValueError:
        print('Missing configuration. Set configuration command: python expens_tracking.py configuration.')
        sys.exit(1)
    current_expenses = read_db(db)
    print_report(current_expenses)


@cli.command() #python_export
def python_export():
    try: 
        db = init_db_connection(os.environ.get('CHOSEN_DB'))
    except ValueError:
        print('Missing configuration. Set configuration command: python expens_tracking.py configuration.')
        sys.exit(1)
    current_expenses = read_db(db)
    print_list(current_expenses)


@cli.command() #import csv
@click.argument('csv_file')

def import_csv(csv_file):
    try: 
        db = init_db_connection(os.environ.get('CHOSEN_DB'))
    except ValueError:
        print('Missing configuration. Set configuration command: python expens_tracking.py configuration.')
        sys.exit(1)
    try:
        import_data_from_csv(db, csv_file)
    except FileNotFoundError:
        print('File is not exist.')
        sys.exit(1)
    

@cli.command() #drop_database

def drop_database():
    try: 
        db = init_db_connection(os.environ.get('CHOSEN_DB'))
    except ValueError:
        print('Missing configuration. Set configuration command: python expens_tracking.py configuration.')
        sys.exit(1)
    decision = input('Are you shure that you want drop database? Yes/No: ')
    if decision.lower() == 'yes':
        db.drop_database()
        set_choice_db('unknown')

if __name__ == "__main__":
    cli()
