import pyodbc
cnxn = None
cursor = None
CONNECTION_STRING = (
    'Driver={ODBC Driver 17 for SQL Server};'
    'Server=LAPTOP-CBFBA03P\SQLEXPRESS;'
    'Database=NeuroCheckDB;'
    'Trusted_Connection=yes;'
)

try:
    cnxn = pyodbc.connect(CONNECTION_STRING)
    cursor = cnxn.cursor()
    print("Conexión exitosa a SQL Server.")

except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print(f"Error de conexión: {sqlstate}")

