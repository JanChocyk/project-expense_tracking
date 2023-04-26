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

import pytest
from expense_tracking import *
