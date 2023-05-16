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

Technical details:
- the program supports SQLite and MySQL databases
- used SQL statements
- the program uses Object-Relational Mapping
- the program has a text interface
- object-oriented programming was used
The program uses two database management systems: MySQL and SQLite. However, you can extend the program yourself with your own connectors using other systems.

Exemplary program launches:
- python expense_tracking_main.py configuration
- python expense_tracking_main.py add 1001 "test"
- python expense_tracking_main.py report
- python expense_tracking_main.py import-csv "expenses.csv" 
- python expense_tracking_main.py python-export
- python expense_tracking_main.py delete 1
- python expense_tracking_main.py drop-database
