import flet as ft
import pyodbc
from DB import CONNECTION_STRING
#-------------------profesorCRUD
def profesorCREATE(datos_profesor: tuple):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                sql_add = """INSERT INTO Profesores(
                pro_nombre_1,pro_nombre_2, pro_nombre_3,
                pro_apellido_pat, pro_apellido_mat,
                pro_rut, pro_email,pro_cargo,pro_password, 
                lvl_curso,pro_state, pro_nacimiento)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?);"""
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

def cursoREAD():
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
                    sql_info = """
                    SELECT e.*,
                    c.cur_nombre,
                    p.pro_nombre_1, p.pro_apellido_pat
                    FROM Estudiantes e
                    LEFT JOIN Curso c ON e.lvl_curso = c.cur_nameID
                    LEFT JOIN Profesores p ON e.Pro_nameID = p.pro_nameID WHERE e.es_nameID = ?"""
                    cursor.execute(sql_info, es_nameID)
                    return cursor.fetchone()
                else:
                    sql_info = """
                    SELECT e.*,
                    c.cur_nombre,
                    p.pro_nombre_1, p.pro_apellido_pat
                    FROM Estudiantes e
                    LEFT JOIN Curso c ON e.lvl_curso = c.cur_nameID
                    LEFT JOIN Profesores p ON e.Pro_nameID = p.pro_nameID"""
                    cursor.execute(sql_info)
                    return cursor.fetchall()
    except pyodbc.Error as ex:
        print(f"Error de conexión o consulta de estudiantes: {ex.args[0]}")
        return None if es_nameID is not None else []

#-------------------testCRUD

def testCREATE(test_data: tuple):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                sql_add = "INSERT INTO Test (es_ID, pro_ID, test_status, test_fecha_inicio, test_fecha_termino) OUTPUT INSERTED.test_ID VALUES(?,?,0,?,?)"
                cursor.execute(sql_add, test_data)      
                test_id = cursor.fetchone()[0]
                cnxn.commit()
                return test_id
    except pyodbc.Error as ex:
        print(f"Error de conexión o consulta: {ex.args[0]}")
        return None
    
def testREAD(test_ID: int | None = None , test_status: int | None = None):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                if test_ID is not None:
                    sql_info = "SELECT * FROM Test WHERE test_id = ?"
                    cursor.execute(sql_info, test_ID)
                    return cursor.fetchone()
                elif test_status is not None:
                    sql_info = """
                        SELECT
                            t.test_status, t.test_ID, test_fecha_inicio, test_fecha_termino,
                            e.es_nombre_1, e.es_apellido_pat, e.es_rut, c.cur_nombre,
                            p.pro_nombre_1, p.pro_apellido_pat, p.pro_rut
                            FROM Test t
                            LEFT JOIN Estudiantes e ON t.es_ID = e.es_nameID
                            LEFT JOIN Profesores p ON t.pro_ID = p.pro_nameID
                            LEFT JOIN Curso c ON e.lvl_curso = c.cur_nameID
                            WHERE t.test_status = ?"""
                    cursor.execute(sql_info, test_status)
                    return cursor.fetchall()
    except pyodbc.Error as ex:
        print(f"Error de conexión o consulta: {ex.args[0]}")
        return None if test_ID is not None else []
    
def testUPDATE(test_ID: int, test_data: dict):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                set_clause = ", ".join([f"{key} = ?" for key in test_data.keys()])
                sql_update = f"UPDATE Test SET {set_clause} WHERE test_ID = ?"
                params = list(test_data.values()) + [test_ID]
                cursor.execute(sql_update, params)
                cnxn.commit()
    except pyodbc.Error as ex:
        print(f"Error de conexión o consulta: {ex.args[0]}")

#-------------------resultados_detalladosCRUD

def resultados_detalladosCREATE(detalles_data: tuple):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                sql_add = """INSERT INTO Resultados_detallados
                            (det_nameES, det_apellidoES,lvl_curso, det_namePRO, det_apellidoPRO, 
                             det_porcentaje, det_puntaje, det_fecha, id_test) OUTPUT INSERTED.det_ID
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
                cursor.execute(sql_add, detalles_data)
                det_id = cursor.fetchone()[0]
                cnxn.commit()
                return det_id
    except pyodbc.Error as ex:
        print(f"Error al crear resultado detallado: {ex.args[0]}")
        return None

def resultados_detalladosREAD(test_ID: int | None = None, det_ID: int | None = None):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                if test_ID is not None:
                    sql_info = "SELECT * FROM Resultados_detallados WHERE id_test = ?"
                    cursor.execute(sql_info, test_ID)
                elif det_ID is not None:
                    sql_info = "SELECT * FROM Resultados_detallados WHERE det_id = ?"
                    cursor.execute(sql_info, det_ID)
                else:
                    return [] # No se proporcionó ID, devolver lista vacía
                return cursor.fetchall()
    except pyodbc.Error as ex:
        print(f"Error al leer resultados detallados: {ex.args[0]}")
        return []
    
#-------------------preguntaCRUD

def preguntaCREATE(pregunta_data: tuple):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                sql_add = "INSERT INTO Preguntas (pre_respuesta, pre_tipo, ID_test) OUTPUT INSERTED.pre_ID VALUES(?,?,?)"
                cursor.execute(sql_add, pregunta_data)
                pre_id= cursor.fetchone()[0]
                cnxn.commit()
                return pre_id
    except pyodbc.Error as ex:
        print(f"Error de conexión o consulta: {ex.args[0]}")
        return False 

def preguntaREAD(ID_test: int | None = None):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                if ID_test is not None:
                    # Devolvemos el ID para poder usarlo en las actualizaciones
                    sql_info = "SELECT pre_ID, pre_respuesta, pre_tipo FROM Preguntas WHERE ID_test = ?"
                    cursor.execute(sql_info, ID_test)
                    return cursor.fetchall()
    except pyodbc.Error as ex:
        return [] # Devolver lista vacía en caso de error
def preguntaUPDATE(ID_pregunta: int, pregunta_data: dict):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                set_clause = ", ".join([f"{key} = ?" for key in pregunta_data.keys()])
                sql_update = f"UPDATE Preguntas SET {set_clause} WHERE pre_ID = ?"
                params = list(pregunta_data.values()) + [ID_pregunta]
                cursor.execute(sql_update, params)
                cnxn.commit()
    except pyodbc.Error as ex:
        print(f"Error de conexión o consulta: {ex.args[0]}")