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

import csv

import pytest
from expense_tracking import *


@pytest.fixture
def db():
    db = SQLiteConnector(':memory:')
    db.execute_on_cursor(QUERY_CREATE_TABLE_SQLITE, table_name=TABLE_NAME)
    return db


@pytest.fixture
def csv_file(tmp_path):
    csv_path = tmp_path / "test.csv"
    with csv_path.open(mode="w") as f:
        writer = csv.writer(f)
        writer.writerow(["amount", "description"])
        writer.writerow([40, "test"])    
    return csv_path


@pytest.fixture
def list():
    current_list = [Expense(1, 40, "test"), Expense(2, 1001, "test")]
    return current_list


#  test of correct addition of the expense to database, test funcji read_db z poleceniem SELECT
def test_save_to_db1(db):
    Expense.save_to_db(db, 1000, 'description')
    got = read_db(db)
    expected = [Expense(1, 1000, 'description')]
    assert got == expected


# test raise ValueError by method save_to_db
def test_save_to_db2(db):
    with pytest.raises(ValueError):
        Expense.save_to_db(db, -1000, 'description')
        

# test check 'if' in function init_db_connection
def test_init_db_connection1():
    choice_db = 'sqlite'
    db = init_db_connection(choice_db)
    got = type(db)
    expected = SQLiteConnector
    assert got == expected


# test check 'if' in function init_db_connection
def test_init_db_connection2():
    choice_db = 'mysql'
    db = init_db_connection(choice_db)
    got = type(db)
    expected = MySQLConnector
    assert got == expected


# test metody execute_on_cursor i wykonania usunięcia rekordu z bazy danych
def test_execute_on_cursor1(db):
    Expense.save_to_db(db, 1000, 'description')
    db.execute_on_cursor(QUERY_DELETE, [1])
    got = read_db(db)
    expected = []
    assert got == expected


# testowanie funkcji import_data_from_csv: odczyt z pliku i zapis do bazy danych
def test_import_data_from_csv1(db, csv_file):
    import_data_from_csv(db, csv_file)
    got = read_db(db)
    expected = [Expense(1, 40, "test")]
    assert got == expected


# testowanie funkcji import_data_from_csv: rzucanie wyjątku FileNotFoundError
def test_import_data_from_csv2(db):
    with pytest.raises(FileNotFoundError):
        import_data_from_csv(db, 'test.csv')


# test funkcji prnt_raport
def test_print(capsys, list):
    print_report(list)
    captured = capsys.readouterr()
    expected = """-ID--AMOUNT--BIG?--------DESCRIPTION-------\n  1      40   -      test\n  2    1001  (!)     test\nTOTAL = 1041\n"""
    assert captured.out == expected


# test funkcji print_list
def test_print_list(capsys, list):
    print_list(list)
    captured = capsys.readouterr()
    expected = """["Expense(id=1, amount=40, description='test')", "Expense(id=2, amount=1001, description='test')"]\n"""
    assert captured.out == expected
