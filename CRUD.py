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
                                            "pro_rut, " \
                                                "pro_email, " \
                                                "pro_cargo, " \
                                                "pro_password, " \
                                                    "lvl_curso," \
                                                        "pro_state, pro_nacimiento) " \
                                                            "VALUES(?,?,?,?,?,?,?,?,?,?,?,?);"
                cursor.execute(sql_add, datos_profesor)
                cnxn.commit()
                return True  # Retorna True si la operación fue exitosa
    except pyodbc.Error as ex:
        print(f"Error de conexión o consulta: {ex.args[0]}")
        return False  # Retorna False si ocurrió un error

def profesorREAD(pro_nameID: int | None = None, pro_rut: str | None = None, pro_password: str | None = None, pro_email: str | None = None, lvl_curso: int | None = None):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                if pro_nameID is not None:
                    # Corregido: Usar la tabla 'Curso' y las columnas 'cur_nameID', 'cur_nombre'
                    sql_info = "SELECT p.*, c.cur_nombre FROM Profesores p LEFT JOIN Curso c ON p.lvl_curso = c.cur_nameID WHERE p.pro_nameID = ?"
                    cursor.execute(sql_info, pro_nameID)
                    return cursor.fetchone()
                elif pro_rut is not None and pro_password is not None:
                    sql_info = "SELECT p.*, c.cur_nombre FROM Profesores p LEFT JOIN Curso c ON p.lvl_curso = c.cur_nameID WHERE p.pro_rut = ? AND pro_password = ?"
                    cursor.execute(sql_info, pro_rut, pro_password)
                    return cursor.fetchone()
                elif pro_rut is not None:
                    sql_info = "SELECT p.*, c.cur_nombre FROM Profesores p LEFT JOIN Curso c ON p.lvl_curso = c.cur_nameID WHERE p.pro_rut = ?"
                    cursor.execute(sql_info, pro_rut)
                    return cursor.fetchone()
                elif pro_email is not None:
                    sql_info = "SELECT p.*, c.cur_nombre FROM Profesores p LEFT JOIN Curso c ON p.lvl_curso = c.cur_nameID WHERE p.pro_email = ?"
                    cursor.execute(sql_info, pro_email)
                    return cursor.fetchone()
                elif lvl_curso is not None:
                    sql_info = "SELECT p.*, c.cur_nombre FROM Profesores p LEFT JOIN Curso c ON p.lvl_curso = c.cur_nameID WHERE p.lvl_curso = ?"
                    cursor.execute(sql_info, lvl_curso)
                    return cursor.fetchall()
                else:
                    # Corregido: Usar la tabla 'Curso' y las columnas 'cur_nameID', 'cur_nombre'
                    sql_info = "SELECT p.*, c.cur_nombre FROM Profesores p LEFT JOIN Curso c ON p.lvl_curso = c.cur_nameID"
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
                cursor.execute(sql_update, params)
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

def cursoREAD_all():
    """Lee todos los cursos de la base de datos."""
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                # Selecciona solo los cursos habilitados (cur_state = 1)
                sql_info = "SELECT cur_nameID, cur_nombre FROM Curso WHERE cur_state = 1 ORDER BY cur_nombre"
                cursor.execute(sql_info)
                return cursor.fetchall()  # Retorna una lista de tuplas (id, nombre)
    except pyodbc.Error as ex:
        print(f"Error de conexión o consulta de cursos: {ex.args[0]}")
        return []
    

def estudiantesREAD(es_nameID: int | None = None, es_rut: str | None = None):
    """Lee todos los estudiantes de la base de datos."""
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                if es_nameID is not None:
                    sql_info = "SELECT e.*, c.cur_nombre, p.pro_nombre_1, p.pro_apellido_pat FROM Estudiantes e LEFT JOIN Curso c ON e.lvl_curso = c.cur_nameID LEFT JOIN Profesores p ON e.Pro_nameID = p.pro_nameID WHERE e.es_nameID = ?"
                    cursor.execute(sql_info, es_nameID)
                    return cursor.fetchone()
                else:
                    sql_info = "SELECT e.*, c.cur_nombre, p.pro_nombre_1, p.pro_apellido_pat FROM Estudiantes e LEFT JOIN Curso c ON e.lvl_curso = c.cur_nameID LEFT JOIN Profesores p ON e.Pro_nameID = p.pro_nameID"
                    cursor.execute(sql_info)
                    return cursor.fetchall()
    except pyodbc.Error as ex:
        print(f"Error de conexión o consulta de estudiantes: {ex.args[0]}")
        return None if es_nameID is not None else []

def testCREATE(test_data: tuple):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                sql_add = "INSERT INTO Test (es_ID, pro_ID) OUTPUT INSERTED.test_ID VALUES(?,?); "
                cursor.execute(sql_add, test_data)      
                test_id = cursor.fetchone()[0]
                cnxn.commit()
                return test_id
    except pyodbc.Error as ex:
        print(f"Error de conexión o consulta: {ex.args[0]}")
        return None
    
def testREAD(test_ID: int):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                sql_info = "SELECT * FROM Test WHERE test_id = ?"
                cursor.execute(sql_info, test_ID)
                return cursor.fetchone()
    except pyodbc.Error as ex:
        print(f"Error de conexión o consulta: {ex.args[0]}")
        return None if test_ID is not None else []
def preguntaCREATE(pregunta_data: tuple):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                sql_add = "INSERT INTO Preguntas (pre_texto, pre_respuesta, pre_tipo, ID_test) VALUES(?,?,?,?)"
                cursor.execute(sql_add, pregunta_data)
                cnxn.commit()
                return True  # Retorna True si la operación fue exitosa
    except pyodbc.Error as ex:
        print(f"Error de conexión o consulta: {ex.args[0]}")
        return False 