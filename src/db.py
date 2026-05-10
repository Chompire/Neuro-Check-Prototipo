import pyodbc
CONNECTION_STRING = (
    'Driver={ODBC Driver 17 for SQL Server};'
    # r'Server=UBNTCONTROLLER\SQLEXPRESS;' 
    r'Server=localhost\SQLEXPRESS;' 
    'Database=NeuroCheckDB;'
    'Trusted_Connection=yes;'
)
