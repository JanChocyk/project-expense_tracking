# Expenses Management Program

This program allows users to effectively control their expenses. It provides various functionalities to add, preview, and manage expenses, as well as import/export data. The program supports both SQLite and MySQL databases, utilizes SQL statements, and incorporates Object-Relational Mapping (ORM). It features a text-based interface and employs object-oriented programming principles.

## Functionalities

1. Add Expense: Users can add expenses to the program by specifying the amount and description. The program will save the expense to the connected database.
2. Preview Reports: Users can preview a list of expenses stored in the database. This functionality allows users to gain an overview of their spending.
3. Delete Expense: Users have the option to remove a specific expense from the database. This feature enables easy management and organization of expenses.
4. Delete Database: Users can choose to delete the entire database. This functionality ensures flexibility in starting afresh or clearing data.
5. Import from CSV: The program allows users to import expenses saved in a CSV file into the database. This feature simplifies the process of transferring data from external sources.
6. Python List Export: Users can export the expenses as a Python list. This functionality facilitates further analysis or integration with other Python programs.

## Technical Details

* Database Support: The program supports two popular database management systems: SQLite and MySQL. It provides connectors and functionalities for seamless interaction with these databases. Additionally, you have the flexibility to extend the program by incorporating connectors for other database systems.
* SQL Statements: SQL (Structured Query Language) statements are used to interact with the databases. The program handles essential operations such as creating tables, inserting records, querying data, and deleting entries.
* Object-Relational Mapping (ORM): The program employs Object-Relational Mapping techniques to bridge the gap between the relational database and object-oriented programming. This approach simplifies data manipulation and allows for a more intuitive programming experience.
* Text Interface: The program offers a text-based interface, enabling users to interact with it through a command-line environment. This interface provides a straightforward and efficient means of managing expenses.
* Object-Oriented Programming: The program is developed using object-oriented programming principles. This approach enhances code organization, reusability, and maintainability.
* Development: the program can be extended with new connectors for other database management systems, e.g. PostgreSQL.

## Getting Started

To get started with the Expenses Management Program, follow these steps:
1. Ensure you have Python installed on your system.
2. Clone the project repository: git clone <repository_url>.
3. Install the necessary dependencies by running the following command:
```pip install -r requirements.txt```
4. Set up the database connection.

MySQL:
- install MySQL
- set up environment variables: HOST - name host, USER - name MySQL user, PASSWORD - your password to MySQL, DATABASE - name new database

SQLite:
- set up environment variables: FILENAME - name new database

5. Run the program in setup mode:
```python expense_tracking_main.py configuration```
6. Run the program:
```python expense_tracking_main.py <comand>```
7. You can now start utilizing the program's functionalities through the text interface.

## Contact
For any inquiries or suggestions regarding the Expenses Management Program, please reach out to *janischocyk@gmail.com*.


Thank you for using our Expenses Management Program! We hope it helps you effectively control your expenses.
