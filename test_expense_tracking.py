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

# SCENARIUSZ TESTÓW:
# 
# 1. test init_db_connection(choice_db: str)
# Sprawdzenie czy działa if, który decyduje, czy dostejemy obiekt db= MySQLConnection() czy db=SQLConnection()
# 
# 2. test read_db(Connector)
# Sprawdzenie czy działa SELECT i czy jest zwracana lista obiektów Expense.
# 
# 3. test metody save_to_db(db, amoutn, description)
# Sprawdzenie, czy poprawnie zadziałał INSERT
# 
# 4. Test inita klasy Expense
# - utworzenie poprawnego obiektu
# - sprawdzenie czy jest rzucany ValueError
# 
# 5. Test metody execute_on_cursor(query, val)
# -select
# -insert
# -delete

from unittest.mock import MagicMock

import pytest
from expense_tracking import *

# @pytest.fixture
# def setUp(self):
#     # Wykonaj kod, który zostanie uruchomiony przed każdym testem
#     self.connection = sqlite3.connect(":memory:")
#     self.cursor = self.connection.cursor()
        
#     # Stwórz tabelę testową
#     self.cursor.execute("""
#         CREATE TABLE test (
#             id INTEGER PRIMARY KEY,
#             name TEXT NOT NULL,
#             age INTEGER
#             );
#         """)
        
#     # Dodaj testowe dane
#     self.cursor.execute("""
#         INSERT INTO test (id, name, age)
#         VALUES
#             (1, 'John', 25),
#             (2, 'Jane', 30),
#             (3, 'Bob', NULL);
#     """)


def test_print_raport():
    ...


def test_print_list():
    ...

