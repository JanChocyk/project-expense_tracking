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
