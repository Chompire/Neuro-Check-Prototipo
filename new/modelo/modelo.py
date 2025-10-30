import flet as ft
from flet_mvc import FletModel
import crud as db

class LoginAppModel(FletModel):
    def cargar_profesor(self, rut: str, password: str):
        datos = db.profesorREAD(pro_rut=rut, pro_password=password)
        if datos:
            self.datos_profesor = datos
            return True
        else:
            # Fracaso: El CRUD no encontró al usuario.
            return False
        
class EstudiantesAppModel(FletModel):
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
    def profesor_ident(self, pro_nameID: int | None = None):
        prof_id = db.profesorREAD(pro_nameID=pro_nameID)
        if prof_id:
            self.datos_profesor = prof_id
            return True
        else:
            return False



class TestAppModel(FletModel):
    def crear_test(self, es_ID: int, pro_ID: int, test_fecha_inicio, test_fecha_termino):
        test_data = (es_ID, pro_ID, test_fecha_inicio, test_fecha_termino)
        test_id = db.testCREATE(test_data)
        return test_id

    def actualizar_test(self, test_ID: int, test_data: dict):
        db.testUPDATE(test_ID, test_data)

    def crear_pregunta(self, pre_respuesta: str, pre_tipo: int, ID_test: int):
        pregunta_data = (pre_respuesta, pre_tipo, ID_test)
        pre_id = db.preguntaCREATE(pregunta_data)
        return pre_id

    def leer_preguntas(self, ID_test: int):
        return db.preguntaREAD(ID_test)

    def actualizar_pregunta(self, ID_pregunta: int, pregunta_data: dict):
        db.preguntaUPDATE(ID_pregunta, pregunta_data)

    def eliminar_preguntas_por_test(self, ID_test: int):
        db.preguntaDELETE(ID_test=ID_test)

    def crear_resultado_detallado(self, det_nameES, det_apellidoES, lvl_curso, det_namePRO, det_apellidoPRO, det_porcentaje, det_puntaje, det_fecha, id_test):
        detalles_data = (det_nameES, det_apellidoES, lvl_curso, det_namePRO, det_apellidoPRO, det_porcentaje, det_puntaje, det_fecha, id_test)
        det_id = db.resultados_detalladosCREATE(detalles_data)
        return det_id



