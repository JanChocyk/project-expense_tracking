# project-expense_tracking

Expense tracker

A program that allows the user to control their expenses.
Functionalities:
- adding an expense (size and description) - the program will save the expense to the database
- report preview - the program will display a list of expenses from the database
- delete expense - the program will remove the indicated expense from the database
- deleting the database - the program will delete the entire database
- import of data from a CSV file - the program will import expenses saved in a CSV file to the database
- python list export - the program will export the paython list

technical details:
- the program supports SQLite and MySQL databases
- used SQL statements
- the program uses Object-Relational Mapping
- the program has a text interface
- object-oriented programming was used

Example runner:
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
