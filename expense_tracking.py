import csv
from dataclasses import dataclass
import os
import sys

import click
import mysql.connector


@dataclass
class Expenses:
    id: int
    amount: float
    description: str

    def __post_init__(self):
        if self.amount <= 0:
            raise ValueError
    
    def __repr__(self) -> str:
        return f"Expense(id={self.id}, amount={self.amount}, description={self.description!r})"


def connect_to_db() -> None:
    """Function open connect to database Expenses, there are all expenses."""
    try:
        mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Delfin_2023",
                database="expenses"
            )
    except mysql.connector.errors.ProgrammingError:
        print('Database not exist.')
        sys.exit(1)
    return mydb


def create_new_db() -> None:
    """Function create new databese Expenses with table list_expenses, they will be stored expenses. MySQL on the computer is required."""
    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Delfin_2023",
        )
    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE expenses")
    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Delfin_2023",
            database="expenses"
        )
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE list_expenses (id INT PRIMARY KEY, amount DECIMAL(10,2), description VARCHAR(200))")


def search_next_id() -> int:
    """Function use current expensive, check ID and return the next free ID."""
    current_expenses = read_db()
    ids = {expense.id for expense in current_expenses}
    new_id = 1
    while True:
        if new_id in ids:
            new_id += 1
        else:
            break
    return new_id


def save_to_db(new_expense: Expenses) -> None:
    '''Function save to database new object Expenses with new expense.'''
    try:
        mydb = connect_to_db()
    except mysql.connector.errors.ProgrammingError:
        create_new_db()
        mydb = connect_to_db()

    mycursor = mydb.cursor()
    sql = "INSERT INTO list_expenses (id, amount, description) VALUES (%s, %s, %s)"
    val = (new_expense.id, new_expense.amount, new_expense.description)
    mycursor.execute(sql, val)
    mydb.commit()


def read_db() -> list[Expenses]:
    """Function return list with expenses from database."""
    try:
        mydb = connect_to_db()
    except mysql.connector.errors.ProgrammingError:
        create_new_db()
        mydb = connect_to_db()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM list_expenses")
    my_result = mycursor.fetchall()
    current_expenses = [Expenses(element[0], element[1], element[2]) for element in my_result]
    return current_expenses


def create_new_expense(amount: float, description: str) -> Expenses:
    """Function create list with expensive objects. First do Expense object from amount and description. Next function use function read_db to acess current expensive and assigne new object to list. 
       Arguments: amount, description.
    """
    try:
        new_expense = Expenses(search_next_id(), float(amount), description)
    except ValueError:
        print(r"The amount exept's must be larger than 0")
        sys.exit(1)
    return new_expense


def delete_expense(id: int) -> None:
    """Function delete record in database with given ID."""
    try:
        mydb = connect_to_db()
    except mysql.connector.errors.ProgrammingError:
        create_new_db()
        mydb = connect_to_db()
    mycursor = mydb.cursor()
    sql = "DELETE FROM list_expenses WHERE id = %s"
    id_ = (int(id), )
    mycursor.execute(sql, id_)
    mydb.commit()


def print_raport() -> None:
    """The function displays a report with all current expenses and total sum."""
    current_expenses = read_db()
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


def import_data_from_csv(csv_file: str) -> None:
    """Function read file CSV with expenses and save each expense to database.
       File CSV must be two column: AMOUNT, DESCRIPTION.
    """
    if os.path.exists(csv_file):
        with open(csv_file) as stream:
            reader = csv.DictReader(stream)
            for row in reader:
                save_to_db(create_new_expense(row['amount'], row['description']))
    else:
        print('File is not exist.')
        sys.exit(1)


def print_list() -> None:
    """Function print list with current expenses."""
    current_expenses = read_db()
    expenses_object_list = [expense.__repr__() for expense in current_expenses]
    print(expenses_object_list)


@click.group()
def cli():
    pass

@cli.command() #add
@click.argument('amount', type=float)
@click.argument('description')

def add(amount, description):
    if float(amount) <= 0 or description == '':
        print('Given amount or description are not correct format.')
        sys.exit(1)
    save_to_db(create_new_expense(amount, description))


@cli.command()
@click.argument('id', type=int)

def delete(id):
    delete_expense(id) 


@cli.command() #raport
def raport():
    print_raport()


@cli.command() #python_export
def python_export():
    print_list()


@cli.command() #import csv
@click.argument('csv_file')

def import_csv(csv_file):
    import_data_from_csv(csv_file)


if __name__ == "__main__":
    cli()
