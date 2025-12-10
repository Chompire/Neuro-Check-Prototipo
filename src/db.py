import pyodbc
CONNECTION_STRING = (
    'Driver={ODBC Driver 17 for SQL Server};'
    # r'Server=UBNTCONTROLLER\SQLEXPRESS;' # Original server name
    r'Server=localhost\SQLEXPRESS;' # Use this if the database is on the same machine
    'Database=NeuroCheckDB;'
    'Trusted_Connection=yes;'
)
