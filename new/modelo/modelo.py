import flet as ft
from flet_mvc import FletModel
import crud as db
from collections import namedtuple

# Define un namedtuple para contener los detalles combinados del test para un acceso más fácil
TestDetails = namedtuple('TestDetails', [
    'es_nombre_1', 'es_apellido_pat', 'cur_nombre',
    'pro_nombre_1', 'pro_apellido_pat'
])

class AppModel(FletModel):
    def cargar_profesor(self, rut: str, password: str):
        datos = db.profesorREAD(pro_rut=rut, pro_password=password)
        if datos:
            self.datos_profesor = datos
            return True
        else:
            return False
    def cargar_profesor_id(self, pro_nameID: int | None = None):
        prof_id = db.profesorREAD(pro_nameID=pro_nameID)
        if prof_id:
            self.datos_profesor_id = prof_id
            return prof_id
        else:
            return False
        
    def cargar_estudiantes(self, es_nameID: int | None = None):
        datos = db.estudiantesREAD(es_nameID=es_nameID)
        if datos:
            self.datos_estudiantes = datos
            return True
        else:
            return False
    def cargar_test_incompletos(self, test_status: int | None = None):
        datos = db.testREAD(test_status=test_status)
        if datos:
            self.datos_test_incompletos = datos
            return True
        else:
            return False
    
    def leer_estudiantes(self):
        return db.estudiantesREAD()

    def crear_test(self, es_ID: int, pro_ID: int, test_fecha_inicio, test_fecha_termino):
        test_data = (es_ID, pro_ID, test_fecha_inicio, test_fecha_termino)
        test_id = db.testCREATE(test_data)
        return test_id

    def actualizar_test(self, test_ID: int, test_data: dict):
        db.testUPDATE(test_ID, test_data)
        
    def leer_test(self, test_ID: int | None = None, test_status: int | None = None, pro_ID: int | None = None):
        return db.testREAD(test_ID=test_ID, test_status=test_status, pro_ID=pro_ID)

    def eliminar_test(self, test_ID: int):
        db.testDELETE(test_ID=test_ID)

    def leer_preguntas(self, pre_id: int | None = None, pre_cat: str | None = None):
        if pre_cat:
            return db.preguntasREAD(pre_cat=pre_cat)
        elif pre_id:
            return db.preguntasREAD(pre_id=pre_id)

    def crear_respuesta(self, res_respuesta: str, res_tipo: int, ID_test: int):
        respuesta_data = (res_respuesta, res_tipo, ID_test)
        res_id = db.respuestaCREATE(respuesta_data)
        return res_id

    def leer_respuestas(self, ID_test: int):
        return db.respuestaREAD(ID_test)

    def actualizar_respuesta(self, ID_respuesta: int, respuesta_data: dict):
        db.respuestaUPDATE(ID_respuesta, respuesta_data)

    def eliminar_respuestas_por_test(self, ID_test: int):
        db.respuestaDELETE(ID_test=ID_test)
    def leer_cursos(self):
        return db.cursoREAD()


    def crear_resultado_detallado(self, det_nameES, det_apellidoES, lvl_curso, det_namePRO, det_apellidoPRO, det_porcentaje, det_porcentaje_atencion, det_porcentaje_memoria, det_porcentaje_social, det_porcentaje_emocional, det_puntaje, det_fecha, id_test):
        detalles_data = (det_nameES, det_apellidoES, lvl_curso, det_namePRO, det_apellidoPRO, det_porcentaje,det_porcentaje_atencion,det_porcentaje_memoria,det_porcentaje_social,det_porcentaje_emocional,det_puntaje, det_fecha, id_test)
        det_id = db.resultados_detalladosCREATE(detalles_data)
        return det_id
    
    def leer_resultados_detallados(self, ID_test: int):
        return db.resultados_detalladosREAD(ID_test)

    def leer_resultados_detallados_by_det_id(self, det_id: int, pro_id: int):
        return db.resultados_detalladosREAD(det_ID=det_id, pro_ID=pro_id)
    
    def leer_info_test(self, test_id: int) -> TestDetails | None:
        test_record = db.testREAD(test_ID=test_id)
        if not test_record:
            return None
        es_id = test_record[1] # es_ID del test
        pro_id = test_record[2] # pro_ID del test
        student_record = db.estudiantesREAD(es_nameID=es_id)
        profesor_record = db.profesorREAD(pro_nameID=pro_id)
        
        if student_record and profesor_record:
            return TestDetails(
                es_nombre_1=student_record.es_nombre_1,
                es_apellido_pat=student_record.es_apellido_pat,
                cur_nombre=student_record.cur_nombre,
                pro_nombre_1=profesor_record.pro_nombre_1,
                pro_apellido_pat=profesor_record.pro_apellido_pat
            )
        return None
    
    # --- Métodos para gestión de docentes ---
    def leer_profesores(self):
        return db.profesorREAD()

    def leer_profesor_por_rut(self, rut):
        return db.profesorREAD(pro_rut=rut)

    def crear_profesor(self, datos):
        return db.profesorCREATE(datos)

    def actualizar_profesor(self, prof_id, datos):
        db.profesorUPDATE(prof_id, datos)

    def eliminar_profesor(self, prof_id):
        db.profesorDELETE(prof_id)
