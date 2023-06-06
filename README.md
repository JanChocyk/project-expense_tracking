Expenses Management Program
This program allows users to effectively control their expenses. It provides various functionalities to add, preview, and manage expenses, as well as import/export data. The program supports both SQLite and MySQL databases, utilizes SQL statements, and incorporates Object-Relational Mapping (ORM). It features a text-based interface and employs object-oriented programming principles.

Functionalities
Add Expense: Users can add expenses to the program by specifying the amount and description. The program will save the expense to the connected database.

Preview Reports: Users can preview a list of expenses stored in the database. This functionality allows users to gain an overview of their spending.

Delete Expense: Users have the option to remove a specific expense from the database. This feature enables easy management and organization of expenses.

Delete Database: Users can choose to delete the entire database. This functionality ensures flexibility in starting afresh or clearing data.

Import from CSV: The program allows users to import expenses saved in a CSV file into the database. This feature simplifies the process of transferring data from external sources.

Python List Export: Users can export the expenses as a Python list. This functionality facilitates further analysis or integration with other Python programs.

Technical Details
Database Support: The program supports two popular database management systems: SQLite and MySQL. It provides connectors and functionalities for seamless interaction with these databases. Additionally, you have the flexibility to extend the program by incorporating connectors for other database systems.

SQL Statements: SQL (Structured Query Language) statements are used to interact with the databases. The program handles essential operations such as creating tables, inserting records, querying data, and deleting entries.

Object-Relational Mapping (ORM): The program employs Object-Relational Mapping techniques to bridge the gap between the relational database and object-oriented programming. This approach simplifies data manipulation and allows for a more intuitive programming experience.

Text Interface: The program offers a text-based interface, enabling users to interact with it through a command-line environment. This interface provides a straightforward and efficient means of managing expenses.

Object-Oriented Programming: The program is developed using object-oriented programming principles. This approach enhances code organization, reusability, and maintainability.

Getting Started
To get started with the Expenses Management Program, follow these steps:

Ensure you have Python installed on your system.

Clone the project repository: git clone <repository_url>.

Install the necessary dependencies by running the following command:

Copy code
pip install -r requirements.txt
Set up the database connection by providing the required details (such as database type, credentials, etc.) in the configuration file.

Run the program:

Copy code
python expenses_management.py
You can now start utilizing the program's functionalities through the text interface.

Contributing
Contributions to the Expenses Management Program are welcome. If you have any ideas, improvements, or bug fixes, feel free to submit a pull request. Additionally, please ensure that you adhere to the established coding conventions and maintain appropriate documentation.

License
This project is licensed under the MIT License.

Contact
For any inquiries or suggestions regarding the Expenses Management Program, please reach out to Your Name.

Thank you for using our Expenses Management Program! We hope it helps you effectively control your expenses.

# project-expense_tracking

Expense tracker - introduction

Functionalitys

In this project, I wanted to present the customer segmentation in a way that is understandable for non-technical people

Project Status: [Completet]
Project Objective

Methods Used

Technologies

Used Machine Learning Algorithms

Model Building Steps

Getting Started

Please feel free to reach me through my LinkedIn


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
