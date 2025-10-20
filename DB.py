import pyodbc
cnxn = None
cursor = None
CONNECTION_STRING = (
    'Driver={ODBC Driver 17 for SQL Server};'
    r'Server=CHOMPIRE\SQLEXPRESS;'
    'Database=NeuroCheckDB;'
    'Trusted_Connection=yes;'
)
