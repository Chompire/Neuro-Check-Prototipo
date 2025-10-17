import flet as ft
import pyodbc
from DB import CONNECTION_STRING

def profesorCREATE(datos_profesor: tuple):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                sql_add = "INSERT INTO Profesores (" \
                    "pro_nombre_1, " \
                        "pro_nombre_2, " \
                            "pro_nombre_3, " \
                                "pro_apellido_pat, " \
                                    "pro_apellido_mat, " \
                                        "pro_nacimiento, " \
                                            "pro_rut, " \
                                                "pro_email, " \
                                                "pro_cargo, " \
                                                "pro_password, " \
                                                    "lvl_curso," \
                                                        "pro_state) " \
                                                            "VALUES(?,?,?,?,?,?,?,?,?,?,?,?);"
                cursor.execute(sql_add, datos_profesor)
                cnxn.commit()
    except pyodbc.Error as ex:
        print(f"Error de conexión o consulta: {ex.args[0]}")
        return None

def profesorREAD(pro_nameID: int | None = None, pro_rut: str | None = None, pro_password: str | None = None, pro_email: str | None = None):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                if pro_nameID is not None:
                    # Obtener un solo profesor por ID
                    sql_info = "SELECT * FROM Profesores WHERE pro_nameID = ?"
                    cursor.execute(sql_info, pro_nameID)
                    return cursor.fetchone()
                elif pro_rut is not None and pro_password is not None:
                    sql_info = "SELECT * FROM Profesores WHERE pro_email = ? AND pro_password = ?"
                    cursor.execute(sql_info, pro_rut, pro_password)
                    return cursor.fetchone()
                elif pro_rut is not None:
                    sql_info = "SELECT * FROM Profesores WHERE pro_rut = ?"
                    cursor.execute(sql_info, pro_rut)
                    return cursor.fetchone()
                else:
                    # Obtener todos los profesores
                    sql_info = "SELECT * FROM Profesores"
                    cursor.execute(sql_info)
                    return cursor.fetchall()
    except pyodbc.Error as ex:
        print(f"Error de conexión o consulta: {ex.args[0]}")
        return [] if pro_nameID is None and pro_rut is None else None
    
def profesorUPDATE(pro_nameID: int, datos_profesor: dict):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                # Asume que datos_profesor es un diccionario con {columna: valor}
                set_clause = ", ".join([f"{key} = ?" for key in datos_profesor.keys()])
                sql_update = f"UPDATE Profesores SET {set_clause} WHERE pro_nameID = ?"
                params = list(datos_profesor.values()) + [pro_nameID]
                cursor.execute(sql_update, *params)
                cnxn.commit()
    except pyodbc.Error as ex:
        print(f"Error de conexión o consulta: {ex.args[0]}")
    
def profesorDELETE(pro_nameID: int):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                sql_delete = "DELETE FROM Profesores WHERE pro_nameID = ?"
                cursor.execute(sql_delete, pro_nameID)
                cnxn.commit()
    except pyodbc.Error as ex:
        print(f"Error de conexión o consulta: {ex.args[0]}")