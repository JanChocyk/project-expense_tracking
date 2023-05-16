import csv

import pytest
import os
import sys
expense_tracking_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
print(expense_tracking_path)
sys.path.insert(0, expense_tracking_path)

from expense_tracking import config_db
from expense_tracking import expense_tracking_main




@pytest.fixture
def db():
    return config_db.SQLiteConnector.prepare_database(':memory:')

# @pytest.fixture
# def dg_mysql():
#     connection = mysql.connector.connect(
#         host=HOST,
#         user=USER,
#         password=PASSWORD,
#         database='',
#         port=3307,
#     )
#     cur = connection.cursor()
#     cur.execute(QUERY_CREATE_DB)
#     cur.execute(QUERY_CREATE_TABLE_MYSQL)
#     connection.commit()


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
    current_list = [expense_tracking_main.Expense(1, 40, "test"), expense_tracking_main.Expense(2, 1001, "test")]
    return current_list


#  test of correct addition of the expense to database, test funcji read_db z poleceniem SELECT
def test_save_to_db1(db):
    expense_tracking_main.Expense.save_to_db(db, 1000, 'description')
    got = expense_tracking_main.read_db(db)
    expected = [expense_tracking_main.Expense(1, 1000, 'description')]
    assert got == expected


# test raise ValueError by method save_to_db
def test_save_to_db2(db):
    with pytest.raises(ValueError):
        expense_tracking_main.Expense.save_to_db(db, -1000, 'description')
        

# # # test check 'if' in function init_db_connection
# def test_init_db_connection1():
#     chosen_db = 'sqlite'
#     db = init_db_connection(chosen_db)
#     got = type(db)
#     expected = SQLiteConnector
#     assert got == expected


# # # test check 'if' in function init_db_connection
# def test_init_db_connection2():
#     chosen_db = 'mysql'
#     db = init_db_connection(chosen_db)
#     got = type(db)
#     expected = MySQLConnector
#     assert got == expected


# test check 'if' in function init_db_connection
def test_init_db_connection():
    chosen_db = 'unknown'
    with pytest.raises(ValueError):
        expense_tracking_main.init_db_connection(chosen_db)

# test metody execute_on_cursor i wykonania usunięcia rekordu z bazy danych
def test_execute_on_cursor1(db):
    expense_tracking_main.Expense.save_to_db(db, 1000, 'description')
    db.execute_on_cursor(config_db.QUERY_DELETE, [1])
    got = expense_tracking_main.read_db(db)
    expected = []
    assert got == expected


# testowanie funkcji import_data_from_csv: odczyt z pliku i zapis do bazy danych
def test_import_data_from_csv1(db, csv_file):
    expense_tracking_main.import_data_from_csv(db, csv_file)
    got = expense_tracking_main.read_db(db)
    expected = [expense_tracking_main.Expense(1, 40, "test")]
    assert got == expected


# testowanie funkcji import_data_from_csv: rzucanie wyjątku FileNotFoundError
def test_import_data_from_csv2(db):
    with pytest.raises(FileNotFoundError):
        expense_tracking_main.import_data_from_csv(db, 'test.csv')


# test funkcji prnt_raport
def test_print(capsys, list):
    expense_tracking_main.print_report(list)
    captured = capsys.readouterr()
    expected = """-ID--AMOUNT--BIG?--------DESCRIPTION-------\n  1      40   -      test\n  2    1001  (!)     test\nTOTAL = 1041\n"""
    assert captured.out == expected


# test funkcji print_list
def test_print_list(capsys, list):
    expense_tracking_main.print_list(list)
    captured = capsys.readouterr()
    expected = """["Expense(id=1, amount=40, description='test')", "Expense(id=2, amount=1001, description='test')"]\n"""
    assert captured.out == expected
