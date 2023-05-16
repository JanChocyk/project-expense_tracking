# Poprawki:
# 1. Korekta metody execute_on_cursor ----------------------------------------------------- GIT
# 2. Pierwsze uruchomienie to konfiguracja bazy danych (wybór i stworzenie). -------------- GIT
# 3. Lepsze rozegranie init_db_connection. ------------------------------------------------ GIT
# 4. Inaczej usuwać bazę danych sqlite. --------------------------------------------------- GIT
# 4.5 Rozbić projekt na dwa pliki --------------------------------------------------------- GIT
# 4.6 Poprawić testy. --------------------------------------------------------------------- GIT
# 5. Korekta docstringów.
# 6. Poprawić README ---------------------------------------------------------------------- GIT



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
# python expense_tracking.py configuration
# python expense_tracking.py add 1001 "test"
# python expense_tracking.py report
# python expense_tracking.py import-csv "expenses.csv" 
# python expense_tracking.py python-export
# python expense_tracking.py delete 1
# python expense_tracking.py drop-database
"""

import csv
from dataclasses import dataclass
import os
import sys

import click

from expense_tracking.config_db import *

HOST = os.environ.get('HOST')
USER = os.environ.get('USER')
PASSWORD = os.environ.get('PASSWORD_TO_DB')
DATABASE = os.environ.get('DATABASE')
FILENAME = os.environ.get('NAME_DB')


@dataclass
class Expense:
    """
    Class Expense represents single expense.

    Atributes:
    - id (None | int)
    - amount (float): amount can't be negative number
    - description (str): description can't be empty string
    """
    id: None
    amount: float
    description: str

    def __post_init__(self):
        if self.amount <= 0:
            raise ValueError
        if self.description == '':
            raise ValueError
    

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


def init_db_connection(chosen_db) -> Connector:
    """
    Function check configuration database and returns object class MySQLConnector or object class SQLiteConnector. If database not exist, function create database and table.

    Arguments:
        choice_db (str): user starts program decide which database use (mysql or sqlite)

    Return: 
        db (Connector)
    """

    if chosen_db == 'unknown':
        raise ValueError('Missing configuration. Set configuration command: python expens_tracking.py configuration.')
    elif chosen_db == 'mysql':
        db = MySQLConnector(HOST, USER, PASSWORD, DATABASE)
    elif chosen_db == 'sqlite':
        db = SQLiteConnector(FILENAME)
    return db


def read_db(db: Connector) -> list[Expense]:
    """
    Function connect with database, select all records and return list with expenses.

    Arguments:
        db - it is connect to database

    Return:
        current_expenses (list[Expense]) - list all expenses from database
    """
    contents_db = db.execute_on_cursor(QUERY_SELECT)
    current_expenses = [Expense(element[0], element[1], element[2]) for element in contents_db]
    return current_expenses


def print_report(current_expenses: list[Expense]) -> None:
    """
    The function displays a report with all current expenses and total sum.
    
    Arguments:
    - currrent_expenses - list all expenses from database
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
    - db - it is connect to database
    - csv_file - file name with extension CSV
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

    Arguments:
    - currrent_expenses - list all expenses from database
    """
    expenses_object_list = [expense.__repr__() for expense in current_expenses]
    print(expenses_object_list)


@click.group()
def cli():
    pass

@cli.command() #configuration

def configuration():
    choice_db = input('Which database to choose: MySQL or SQLite? Type "--m" or "--s": ')
    if check_db_config() == 'mysql' or check_db_config() == 'sqlite':
        print('Database already chosen. First drop current database, next set new configuration.')
        sys.exit(1)
    if choice_db == '--m':
        MySQLConnector.prepare_database(HOST, USER, PASSWORD, DATABASE)
        set_choice_db('mysql')
        print('Configuration is completed. Database created.')
    elif choice_db == '--s':
        SQLiteConnector.prepare_database(FILENAME)
        set_choice_db('sqlite')
        print('Configuration is completed. Database created.')
    else:
        print('Incorrect data has been entered.')


@cli.command() #add
@click.argument('amount', type=float)
@click.argument('description')

def add(amount, description):
    try: 
        db = init_db_connection(check_db_config())
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
        db = init_db_connection(check_db_config())
    except ValueError:
        print('Missing configuration. Set configuration command: python expens_tracking.py configuration.')
        sys.exit(1)
    db.execute_on_cursor(QUERY_DELETE, [int(id)])
    print(f'The record with id {id} has been deleted.')

@cli.command() #report
def report():
    try: 
        db = init_db_connection(check_db_config())
    except ValueError:
        print('Missing configuration. Set configuration command: python expens_tracking.py configuration.')
        sys.exit(1)
    current_expenses = read_db(db)
    print_report(current_expenses)


@cli.command() #python_export
def python_export():
    try: 
        db = init_db_connection(check_db_config())
    except ValueError:
        print('Missing configuration. Set configuration command: python expens_tracking.py configuration.')
        sys.exit(1)
    current_expenses = read_db(db)
    print_list(current_expenses)


@cli.command() #import csv
@click.argument('csv_file')

def import_csv(csv_file):
    try: 
        db = init_db_connection(check_db_config())
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
        db = init_db_connection(check_db_config())
    except ValueError:
        print('Missing configuration. Set configuration command: python expens_tracking.py configuration.')
        sys.exit(1)
    decision = input('Are you shure that you want drop database? Yes/No: ')
    if decision.lower() == 'yes':
        db.drop_database()
        set_choice_db('unknown')

if __name__ == "__main__":
    cli()
