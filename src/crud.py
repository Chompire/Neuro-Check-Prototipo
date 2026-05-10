import flet as ft
import pyodbc
import pandas as pd
from db import CONNECTION_STRING    
def profesorCREATE(datos_profesor: tuple):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                sql_add = """INSERT INTO Profesores (
                pro_nombre_1, pro_nombre_2, pro_nombre_3,
                pro_apellido_pat, pro_apellido_mat,
                pro_rut, pro_cargo, pro_password,
                pro_state, pro_online_state)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0);"""
                cursor.execute(sql_add, datos_profesor)
                cnxn.commit()
                return True 
    except pyodbc.Error as ex:
        print(f"profesorCREATE Error de conexión o consulta: {ex.args[0]}")
        return False

def profesorREAD(pro_nameID: int | None = None, pro_rut: str | None = None, pro_password: str | None = None, lvl_curso: int | None = None):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                base_sql = """
                    SELECT p.*, ISNULL(t_count.num_encuestas, 0) as num_encuestas
                    FROM Profesores p
                    LEFT JOIN (
                        SELECT pro_ID, COUNT(test_ID) as num_encuestas
                        FROM Test
                        WHERE test_status = 1
                        GROUP BY pro_ID
                    ) t_count ON p.pro_nameID = t_count.pro_ID
                """

                if pro_nameID is not None:
                    sql_info = f"{base_sql} WHERE p.pro_nameID = ?"
                    cursor.execute(sql_info, pro_nameID)
                    return cursor.fetchone()
                elif pro_rut is not None and pro_password is not None:
                    sql_info = f"{base_sql} WHERE p.pro_rut = ? AND p.pro_password = ?"
                    cursor.execute(sql_info, pro_rut, pro_password)
                    return cursor.fetchone()
                elif pro_rut is not None:
                    sql_info = f"{base_sql} WHERE p.pro_rut = ?"
                    cursor.execute(sql_info, pro_rut)
                    return cursor.fetchone()
                elif lvl_curso is not None:
                    
                    print("profesorREAD: La búsqueda por lvl_curso ya no está soportada directamente en Profesores.")
                    return []
                else:
                    cursor.execute(base_sql)
                    return cursor.fetchall()
    except pyodbc.Error as ex:
        print(f"profesorREAD Error de conexión o consulta: {ex.args[0]}")
        return [] if pro_nameID is None and pro_rut is None else None
    
def profesorUPDATE(pro_nameID: int, datos_profesor: dict):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                
                set_clause = ", ".join([f"{key} = ?" for key in datos_profesor.keys()])
                sql_update = f"UPDATE Profesores SET {set_clause} WHERE pro_nameID = ?"
                params = list(datos_profesor.values()) + [pro_nameID]
                cursor.execute(sql_update, params)
                cnxn.commit()
    except pyodbc.Error as ex:
        print(f"profesorUPDATE Error de conexión o consulta: {ex.args[0]}")
    
def profesorDELETE(pro_nameID: int):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                sql_delete = "DELETE FROM Profesores WHERE pro_nameID = ?"
                cursor.execute(sql_delete, pro_nameID)
                cnxn.commit()
    except pyodbc.Error as ex:
        print(f"profesorDELETE Error de conexión o consulta: {ex.args[0]}")

def prof_pie_CREATE(prof_id: int, cursos_a_cargo: str):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn: 
            with cnxn.cursor() as cursor:
                sql_add = "INSERT INTO Prof_PIE (prof_ID, cursos_a_cargo) VALUES (?, ?)"
                cursor.execute(sql_add, prof_id, cursos_a_cargo)
                cnxn.commit()
    except pyodbc.Error as ex:
        print(f"prof_pie_CREATE Error: {ex.args[0]}")

def prof_pie_UPDATE(prof_id: int, cursos_a_cargo: str):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn: 
            with cnxn.cursor() as cursor:
                
                sql_update = "UPDATE Prof_PIE SET cursos_a_cargo = ? WHERE prof_ID = ?"
                cursor.execute(sql_update, cursos_a_cargo, prof_id)
                if cursor.rowcount == 0:
                    sql_insert = "INSERT INTO Prof_PIE (prof_ID, cursos_a_cargo) VALUES (?, ?)"
                    cursor.execute(sql_insert, prof_id, cursos_a_cargo)
                cnxn.commit()
    except pyodbc.Error as ex:
        print(f"prof_pie_UPDATE Error: {ex.args[0]}")

def prof_pie_DELETE(prof_id: int):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                sql_delete = "DELETE FROM Prof_PIE WHERE prof_ID = ?"
                cursor.execute(sql_delete, prof_id)
                cnxn.commit()
    except pyodbc.Error as ex:
        print(f"prof_pie_DELETE Error: {ex.args[0]}")

def prof_pie_READ(prof_ID: int):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                sql_info = "SELECT cursos_a_cargo FROM Prof_PIE WHERE prof_ID = ?"
                cursor.execute(sql_info, prof_ID)
                return cursor.fetchone()
    except pyodbc.Error as ex:
        print(f"prof_pie_READ Error de conexión o consulta: {ex.args[0]}")
        return None

def cursoREAD(curso_id: int | None = None):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                if curso_id is not None:
                    sql_info = "SELECT cur_nameID, cur_nombre, cur_año, cur_state FROM Curso WHERE cur_nameID = ?"
                    cursor.execute(sql_info, curso_id)
                    return cursor.fetchone()
                else:
                    sql_info = "SELECT cur_nameID, cur_nombre, cur_año, cur_state FROM Curso ORDER BY cur_nombre"
                    cursor.execute(sql_info)
                    return cursor.fetchall()
    except pyodbc.Error as ex:
        print(f"cursoREAD Error de conexión o consulta: {ex.args[0]}")
        return None if curso_id is not None else []

def cursoCREATE(nombre: str, año: int):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                sql_add = "INSERT INTO Curso (cur_nombre, cur_año, cur_state) VALUES (?, ?, 1)"
                cursor.execute(sql_add, nombre, año)
                cnxn.commit()
                return True
    except pyodbc.Error as ex:
        print(f"cursoCREATE Error de conexión o consulta: {ex.args[0]}")
        return False

def cursoUPDATE(curso_id: int, datos_curso: dict):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                set_clause = ", ".join([f"{key} = ?" for key in datos_curso.keys()])
                sql_update = f"UPDATE Curso SET {set_clause} WHERE cur_nameID = ?"
                params = list(datos_curso.values()) + [curso_id]
                cursor.execute(sql_update, params)
                cnxn.commit()
    except pyodbc.Error as ex:
        print(f"cursoUPDATE Error de conexión o consulta: {ex.args[0]}")
    

def estudianteCREATE(datos_estudiante: tuple):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                sql_add = """INSERT INTO Estudiantes(es_nombre_1,
                                es_apellido_pat, es_apellido_mat,
                                es_rut, es_nacimiento, es_sexo,
                                lvl_curso, es_establecimiento)
                                VALUES(?,?,?,?,?,?,?,?);"""
                cursor.execute(sql_add, datos_estudiante)
                cnxn.commit()
                return True
    except pyodbc.Error as ex:
        print(f"estudianteCREATE Error de conexión o consulta: {ex.args[0]}")
        return False

def estudiante_existe_por_rut(es_rut: str) -> bool:
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                sql_check = "SELECT 1 FROM Estudiantes WHERE es_rut = ?"
                cursor.execute(sql_check, es_rut)
                return cursor.fetchone() is not None
    except pyodbc.Error as ex:
        print(f"estudiante_existe_por_rut Error: {ex.args[0]}")
        return True

def estudianteUPDATE(es_nameID: int, datos_estudiante: dict):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                set_clause = ", ".join([f"{key} = ?" for key in datos_estudiante.keys()])
                sql_update = f"UPDATE Estudiantes SET {set_clause} WHERE es_nameID = ?"
                params = list(datos_estudiante.values()) + [es_nameID]
                cursor.execute(sql_update, params)
                cnxn.commit()
                return True
    except pyodbc.Error as ex:
        print(f"estudianteUPDATE Error de conexión o consulta: {ex.args[0]}")
        return False

def estudianteDELETE(es_nameID: int):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                cursor.execute("SELECT test_ID FROM Test WHERE es_ID = ?", es_nameID)
                test_ids = [row.test_ID for row in cursor.fetchall()]
                if test_ids:
                    placeholders = ','.join('?' for _ in test_ids)
                    cursor.execute(f"DELETE FROM Respuestas WHERE ID_test IN ({placeholders})", *test_ids)
                    cursor.execute(f"DELETE FROM Test WHERE es_ID = ?", es_nameID)
                cursor.execute("DELETE FROM Estudiantes WHERE es_nameID = ?", es_nameID)
                cnxn.commit()
                return True
    except pyodbc.Error as ex:
        print(f"estudianteDELETE Error de conexión o consulta: {ex.args[0]}")
        return False

def estudiantesREAD(es_nameID: int | None = None, es_rut: str | None = None, pro_nameID: int | None = None, lvl_curso: int | None = None):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                if es_nameID is not None:
                    sql_info = """SELECT e.*, c.cur_nombre, c.cur_state, e.es_establecimiento
                    FROM Estudiantes e
                    LEFT JOIN Curso c ON e.lvl_curso = c.cur_nameID WHERE e.es_nameID = ?"""
                    cursor.execute(sql_info, es_nameID)
                    return cursor.fetchone()
                elif es_rut is not None:
                    sql_info = """SELECT e.*, c.cur_nombre, c.cur_state, e.es_establecimiento
                    FROM Estudiantes e
                    LEFT JOIN Curso c ON e.lvl_curso = c.cur_nameID WHERE e.es_rut = ?"""
                    cursor.execute(sql_info, (es_rut,))
                    return cursor.fetchone()
                elif pro_nameID is not None:
                    print("estudiantesREAD: La búsqueda por pro_nameID ya no está soportada en Estudiantes.")
                    return []
                elif lvl_curso is not None:
                    sql_info = """SELECT e.*, c.cur_nombre, c.cur_state, e.es_establecimiento
                    FROM Estudiantes e
                    LEFT JOIN Curso c ON e.lvl_curso = c.cur_nameID WHERE e.lvl_curso = ?"""
                    cursor.execute(sql_info, lvl_curso)
                    return cursor.fetchall()
                else:
                    sql_info = """SELECT e.*, c.cur_nombre, c.cur_state, e.es_establecimiento
                    FROM Estudiantes e
                    LEFT JOIN Curso c ON e.lvl_curso = c.cur_nameID
                    """
                    cursor.execute(sql_info)
                    return cursor.fetchall()
    except pyodbc.Error as ex:
        print(f"estudiantesREAD Error de conexión o consulta de estudiantes: {ex.args[0]}")
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
        print(f"testCREATE Error de conexión o consulta: {ex.args[0]}")
        return None
    
def testREAD(test_ID: int | None = None , test_status: int | None = None, pro_ID: int | None = None):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                if test_ID is not None:
                    sql_info = "SELECT * FROM Test WHERE test_id = ?"
                    cursor.execute(sql_info, test_ID)
                    return cursor.fetchone()
                elif pro_ID is not None and test_status is not None:
                    sql_info = """
                        SELECT
                            t.test_status, t.test_ID, test_fecha_inicio, test_fecha_termino,
                            t.test_status, t.test_ID, t.pro_ID, c.cur_nameID, test_fecha_inicio, test_fecha_termino,
                            e.es_nombre_1, e.es_apellido_pat, e.es_rut, c.cur_nombre,
                            p.pro_nombre_1, p.pro_apellido_pat, p.pro_rut,
                            rd.det_porcentaje
                            FROM Test t
                            LEFT JOIN Estudiantes e ON t.es_ID = e.es_nameID
                            LEFT JOIN Profesores p ON t.pro_ID = p.pro_nameID
                            LEFT JOIN Curso c ON e.lvl_curso = c.cur_nameID
                            LEFT JOIN Resultados_detallados rd ON t.test_ID = rd.id_test
                            WHERE t.pro_ID = ? AND t.test_status = ?"""
                    cursor.execute(sql_info, pro_ID, test_status)
                    return cursor.fetchall()
                elif test_status is not None:
                    sql_info = """
                        SELECT
                            t.test_status, t.test_ID, test_fecha_inicio, test_fecha_termino,
                            t.test_status, t.test_ID, t.pro_ID, c.cur_nameID, test_fecha_inicio, test_fecha_termino,
                            e.es_nombre_1, e.es_apellido_pat, e.es_rut, c.cur_nombre,
                            p.pro_nombre_1, p.pro_apellido_pat, p.pro_rut,
                            rd.det_porcentaje
                            FROM Test t
                            LEFT JOIN Estudiantes e ON t.es_ID = e.es_nameID
                            LEFT JOIN Profesores p ON t.pro_ID = p.pro_nameID
                            LEFT JOIN Curso c ON e.lvl_curso = c.cur_nameID
                            LEFT JOIN Resultados_detallados rd ON t.test_ID = rd.id_test
                            WHERE t.test_status = ?"""
                    cursor.execute(sql_info, test_status)
                    return cursor.fetchall()
                elif pro_ID is not None:
                    sql_info = """
                        SELECT
                            t.test_status, t.test_ID, test_fecha_inicio, test_fecha_termino,
                            t.test_status, t.test_ID, t.pro_ID, c.cur_nameID, test_fecha_inicio, test_fecha_termino,
                            e.es_nombre_1, e.es_apellido_pat, e.es_rut, c.cur_nombre,
                            p.pro_nombre_1, p.pro_apellido_pat, p.pro_rut,
                            rd.det_porcentaje
                            FROM Test t
                            LEFT JOIN Estudiantes e ON t.es_ID = e.es_nameID
                            LEFT JOIN Profesores p ON t.pro_ID = p.pro_nameID
                            LEFT JOIN Curso c ON e.lvl_curso = c.cur_nameID
                            LEFT JOIN Resultados_detallados rd ON t.test_ID = rd.id_test
                            WHERE t.pro_ID = ? AND t.test_status = 1""" 
                    cursor.execute(sql_info, pro_ID)
                    return cursor.fetchall()
    except pyodbc.Error as ex:
        print(f"testREAD Error de conexión o consulta: {ex.args[0]}")
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
        print(f"testUPDATE Error de conexión o consulta: {ex.args[0]}")

def testDELETE(test_ID: int| None = None):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                if test_ID is not None:
                    sql_delete = "DELETE FROM Test WHERE test_ID = ?"
                    cursor.execute(sql_delete, test_ID)
                    cnxn.commit()
    except pyodbc.Error as ex:
        print(f"testDELETE Error de conexión o consulta: {ex.args[0]}")

#-------------------resultados_detalladosCRUD

def resultados_detalladosCREATE(detalles_data: tuple):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                sql_add = """INSERT INTO Resultados_detallados
                            (det_nameES, det_apellidoES, lvl_curso, det_namePRO, det_apellidoPRO, 
                             det_porcentaje, det_porcentaje_atencion, det_porcentaje_memoria, 
                             det_porcentaje_social, det_porcentaje_emocional,
                             det_puntaje, det_fecha, id_test) OUTPUT INSERTED.det_ID
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
                cursor.execute(sql_add, detalles_data)
                det_id = cursor.fetchone()[0]
                cnxn.commit()
                return det_id
    except pyodbc.Error as ex:
        print(f"resultados_detalladosCREATE Error al crear resultado detallado: {ex.args[0]}")
        return None

def resultados_detalladosREAD(test_ID: int | None = None, det_ID: int | None = None, pro_ID: int | None = None, lvl_curso: str | None = None, det_fecha: str | None = None, cur_año: int | None = None):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                if det_ID is not None and pro_ID is not None:
                    sql_info = """
                        SELECT rd.* FROM Resultados_detallados rd
                        JOIN Test t ON rd.id_test = t.test_ID
                        WHERE rd.det_id = ? AND t.pro_ID = ?
                    """
                    cursor.execute(sql_info, det_ID, pro_ID)
                    return cursor.fetchall()
                elif test_ID is not None:
                    sql_info = "SELECT * FROM Resultados_detallados WHERE id_test = ?"
                    cursor.execute(sql_info, test_ID)
                    return cursor.fetchall()
                elif det_ID is not None:
                    sql_info = "SELECT * FROM Resultados_detallados WHERE det_id = ?"
                    cursor.execute(sql_info, det_ID)
                    return cursor.fetchall()
                elif pro_ID is not None:                    
                    sql_info = """
                        SELECT rd.*, c.cur_año, c.cur_state, t.pro_ID FROM Resultados_detallados rd
                        JOIN Test t ON rd.id_test = t.test_ID
                        LEFT JOIN Curso c ON rd.lvl_curso = c.cur_nombre
                        WHERE t.pro_ID = ? 
                    """
                    params = [pro_ID]
                    if cur_año is not None:
                        sql_info += " AND c.cur_año = ?"
                        params.append(cur_año)
                    
                    cursor.execute(sql_info, params)
                    return cursor.fetchall()
                elif det_fecha is not None:
                    sql_info = "SELECT * FROM Resultados_detallados WHERE det_fecha = ?"
                    cursor.execute(sql_info, det_fecha)
                    return cursor.fetchall()
                elif lvl_curso is not None:
                    sql_info = """
                        SELECT rd.*, c.cur_año, t.pro_ID FROM Resultados_detallados rd
                        JOIN Test t ON rd.id_test = t.test_ID
                        LEFT JOIN Curso c ON rd.lvl_curso = c.cur_nombre
                        WHERE rd.lvl_curso = ?
                    """
                    params = [lvl_curso]
                    if cur_año is not None:
                        sql_info += " AND c.cur_año = ?"
                        params.append(cur_año)
                    cursor.execute(sql_info, params)
                    return cursor.fetchall()
                else:
                    sql_info = "SELECT * FROM Resultados_detallados"
                    cursor.execute(sql_info)
                    return cursor.fetchall()
    except pyodbc.Error as ex:
        print(f"resultados_detalladosREAD Error al leer resultados detallados: {ex.args[0]}")
        return []

def preguntasREAD(pre_id: int | None = None, pre_cat: str | None = None):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                if pre_id is not None:
                    sql_info = "SELECT pre_id, pre_text, pre_plus FROM Preguntas WHERE pre_id = ?"
                    cursor.execute(sql_info, pre_id)
                elif pre_cat is not None:
                    sql_info = "SELECT pre_id, pre_text, pre_plus FROM Preguntas WHERE pre_cat = ? ORDER BY pre_id"
                    cursor.execute(sql_info, pre_cat)
                return cursor.fetchall()
    except pyodbc.Error as ex:
        print(f"preguntasREAD Error de conexión o consulta: {ex.args[0]}")
        return []

        
#-------------------respuestaCRUD

def respuestaCREATE(respuesta_data: tuple):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                sql_add = "INSERT INTO Respuestas (res_respuesta, res_tipo, ID_test) OUTPUT INSERTED.res_ID VALUES(?,?,?)"
                cursor.execute(sql_add, respuesta_data)
                res_id= cursor.fetchone()[0]
                cnxn.commit()
                return res_id
    except pyodbc.Error as ex:
        print(f"respuestaCREATE Error de conexión o consulta: {ex.args[0]}")
        return False 

def respuestaREAD(ID_test: int | None = None):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                if ID_test is not None:
                    
                    sql_info = "SELECT res_ID, res_respuesta, res_tipo FROM Respuestas WHERE ID_test = ?"
                    cursor.execute(sql_info, ID_test)
                    return cursor.fetchall()
    except pyodbc.Error as ex:
        return [] 
def respuestaUPDATE(ID_respuesta: int, respuesta_data: dict):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                set_clause = ", ".join([f"{key} = ?" for key in respuesta_data.keys()])
                sql_update = f"UPDATE Respuestas SET {set_clause} WHERE res_ID = ?"
                params = list(respuesta_data.values()) + [ID_respuesta]
                cursor.execute(sql_update, params)
                cnxn.commit()
    except pyodbc.Error as ex:
        print(f"respuestaUPDATE Error de conexión o consulta: {ex.args[0]}")

def respuestaDELETE(ID_respuesta: int| None = None, ID_test: int | None = None):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                if ID_respuesta is not None:
                    sql_delete = "DELETE FROM Respuestas WHERE res_ID = ?"
                    cursor.execute(sql_delete, ID_respuesta)
                    cnxn.commit()
                elif ID_test is not None:
                    sql_delete = "DELETE FROM Respuestas WHERE ID_test = ?"
                    cursor.execute(sql_delete, ID_test)
                    cnxn.commit()
    except pyodbc.Error as ex:
        print(f"respuestaDELETE Error de conexión o consulta: {ex.args[0]}")

#-------------------documentosPDFCRUD

def documentoPDFCREATE(nombre: str, extension: str, contenido: bytes):

    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                sql_add = "INSERT INTO DocumentosPDF (pdf_nombre, pdf_extension, pdf_contenido) OUTPUT INSERTED.pdf_id VALUES (?, ?, ?)"
                cursor.execute(sql_add, nombre, extension, contenido)
                pdf_id = cursor.fetchone()[0]
                cnxn.commit()
                return pdf_id
    except pyodbc.Error as ex:
        print(f"documentoPDFCREATE Error de conexión o consulta: {ex.args[0]}")
        return None

def documentoPDFUPDATE(pdf_id: int, contenido: bytes):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                sql_update = "UPDATE DocumentosPDF SET pdf_contenido = ?, pdf_fecha = GETDATE() WHERE pdf_id = ?"
                cursor.execute(sql_update, contenido, pdf_id)
                cnxn.commit()
                return True
    except pyodbc.Error as ex:
        print(f"documentoPDFUPDATE Error de conexión o consulta: {ex.args[0]}")
        return False

def documentoPDF_READ(pdf_id: int | None = None, pdf_nombre: str | None = None, include_content: bool = False):
  
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                select_clause = "SELECT pdf_id, pdf_nombre, pdf_extension, pdf_fecha"
                if include_content:
                    select_clause += ", pdf_contenido"

                if pdf_id is not None:
                    sql_info = f"{select_clause} FROM DocumentosPDF WHERE pdf_id = ?"
                    cursor.execute(sql_info, pdf_id)
                    return cursor.fetchone()
                elif pdf_nombre is not None:
                    sql_info = f"{select_clause} FROM DocumentosPDF WHERE pdf_nombre = ?"
                    cursor.execute(sql_info, pdf_nombre)
                    return cursor.fetchone()
                else: 
                    sql_info = f"{select_clause} FROM DocumentosPDF ORDER BY pdf_fecha DESC"
                    cursor.execute(sql_info)
                    return cursor.fetchall()
    except pyodbc.Error as ex:
        print(f"documentoPDF_READ Error de conexión o consulta: {ex.args[0]}")
        return None if pdf_id is not None or pdf_nombre is not None else []

#-------------------notificacionesCRUD

def notificacionCREATE(prof_id_destino: int, mensaje: str, id_resultados_detallados: int):

    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                
                sql_add = "INSERT INTO Notificaciones (id_profesor_pie, not_mensaje, not_status, id_resultados_detallados, noti_fecha_creacion) VALUES (?, ?, 0, ?, GETDATE())"
                cursor.execute(sql_add, prof_id_destino, mensaje, id_resultados_detallados)
                cnxn.commit()
                return True
    except pyodbc.Error as ex:
        print(f"notificacionCREATE Error: {ex.args[0]}")
        return False

def notificacionesREAD(prof_id: int, solo_no_leidas: bool = False):

    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                
                sql_info = "SELECT noti_ID, not_mensaje, not_status, id_resultados_detallados, noti_fecha_creacion FROM Notificaciones WHERE id_profesor_pie = ?"
                params = [prof_id]
                if solo_no_leidas:
                    sql_info += " AND not_status = 0"
                sql_info += " ORDER BY noti_fecha_creacion DESC"
                cursor.execute(sql_info, params)
                return cursor.fetchall()
    except pyodbc.Error as ex:
        print(f"notificacionesREAD Error: {ex.args[0]}")
        return []

def notificacionUPDATE_leida(noti_ID: int, leida: bool = True):

    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                sql_update = "UPDATE Notificaciones SET not_status = ? WHERE noti_ID = ?"
                cursor.execute(sql_update, 1 if leida else 0, noti_ID)
                cnxn.commit()
    except pyodbc.Error as ex:
        print(f"notificacionUPDATE_leida Error: {ex.args[0]}")

def notificacionesDELETE(prof_id: int | None = None, not_status: int | None = None, noti_ID: int | None = None):

    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                sql_delete = "DELETE FROM Notificaciones WHERE 1=1"
                params = []
                if prof_id is not None:
                    sql_delete += " AND id_profesor_pie = ?"
                    params.append(prof_id)
                if not_status is not None:
                    sql_delete += " AND not_status = ?"
                    params.append(not_status)
                if noti_ID is not None:
                    sql_delete += " AND noti_ID = ?"
                    params.append(noti_ID)
                
                cursor.execute(sql_delete, params)
                cnxn.commit()
                return True
    except pyodbc.Error as ex:
        print(f"notificacionesDELETE Error: {ex.args[0]}")
        return False

def obtener_pie_por_curso(curso_id: int):
   
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                curso_id_str = str(curso_id)
                sql_query = """
                    SELECT P.pro_nameID
                    FROM Profesores P
                    JOIN Prof_PIE PP ON P.pro_nameID = PP.prof_ID
                    WHERE P.pro_cargo = 1 -- Cargo 1 es para PIE
                      AND CHARINDEX(CONCAT(',', ?, ','), CONCAT(',', PP.cursos_a_cargo, ',')) > 0
                """
                cursor.execute(sql_query, curso_id_str)
                result = cursor.fetchone()
                if result:
                    return result.pro_nameID
                return None
    except pyodbc.Error as ex:
        print(f"obtener_pie_por_curso Error: {ex.args[0]}")
        return None