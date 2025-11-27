import flet as ft
from flet_mvc import FletModel
import crud as db
from collections import namedtuple

TestDetails = namedtuple('TestDetails', [
    'es_nombre_1', 'es_apellido_pat', 'cur_nombre',
    'pro_nombre_1', 'pro_apellido_pat'
])


CursoDetails = namedtuple('CursoDetails', ['cur_nameID', 'cur_nombre', 'cur_año', 'cur_state'])

class AppModel(FletModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.datos_profesor = None

    def cargar_profesor(self, rut: str, password: str):
        datos = db.profesorREAD(pro_rut=rut, pro_password=password)
        if datos:
            self.datos_profesor = datos
            return True
        else:
            return False
    def cargar_profesor_por_id(self, pro_id: int):
        """Carga los datos de un profesor en el modelo usando solo su ID."""
        profesor_data = db.profesorREAD(pro_nameID=pro_id)
        if profesor_data:
            self.datos_profesor = profesor_data
            return True
        else:
            return False
        
    def leer_profesor_por_id(self, pro_id: int):
        """Lee los datos de un profesor desde la BD usando su ID y lo retorna."""
        return db.profesorREAD(pro_nameID=pro_id)

    def cargar_estudiantes(self, es_nameID: int | None = None):
        datos = db.estudiantesREAD(es_nameID=es_nameID)
        if datos:
            self.datos_estudiantes = datos
            return True
        else:
            return False
    def leer_estudiante_por_id(self, es_nameID: int | None = None):
        datos = db.estudiantesREAD(es_nameID=es_nameID)
        if datos:
            self.datos_estudiante = datos
            return datos
        else:
            return False
    def leer_estudiantes_por_curso(self, lvl_curso: int):
        datos = db.estudiantesREAD(lvl_curso=lvl_curso)
        if datos:
            return datos
        else:
            return []

    def estudiante_existe_por_rut(self, es_rut: str) -> bool:
        return db.estudiante_existe_por_rut(es_rut)

    def crear_estudiante(self, datos: tuple) -> bool:
        return db.estudianteCREATE(datos)

    def actualizar_estudiante(self, es_nameID: int, datos: dict):
        return db.estudianteUPDATE(es_nameID, datos)

    def eliminar_estudiante(self, es_nameID: int):
        return db.estudianteDELETE(es_nameID)


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
    def leer_cursos_pie(self, prof_id: int):
        return db.prof_pie_READ(prof_id)
    
    def actualizar_respuesta(self, ID_respuesta: int, respuesta_data: dict):
        db.respuestaUPDATE(ID_respuesta, respuesta_data)

    def eliminar_respuestas_por_test(self, ID_test: int):
        db.respuestaDELETE(ID_test=ID_test)

    def leer_curso_by_id(self, curso_id: int):
        """Lee un curso específico por su ID."""
        curso_data = db.cursoREAD(curso_id=curso_id)
        if curso_data:
            return CursoDetails(
                cur_nameID=curso_data[0],
                cur_nombre=curso_data[1],
                cur_año=curso_data[2],
                cur_state=curso_data[3]
            )
        return None
    def leer_cursos(self):
        return db.cursoREAD()

    def crear_curso(self, nombre, año):
        return db.cursoCREATE(nombre, año)

    def actualizar_curso(self, curso_id, datos):
        db.cursoUPDATE(curso_id, datos)

    def crear_resultado_detallado(self, det_nameES, det_apellidoES, lvl_curso, det_namePRO, det_apellidoPRO, det_porcentaje, det_porcentaje_atencion, det_porcentaje_memoria, det_porcentaje_social, det_porcentaje_emocional, det_puntaje, det_fecha, id_test):
        detalles_data = (det_nameES, det_apellidoES, lvl_curso, det_namePRO, det_apellidoPRO, det_porcentaje,det_porcentaje_atencion,det_porcentaje_memoria,det_porcentaje_social,det_porcentaje_emocional,det_puntaje, det_fecha, id_test)
        det_id = db.resultados_detalladosCREATE(detalles_data)
        return det_id
    
    def leer_resultados_detallados(self, ID_test: int | None = None, pro_ID: int | None = None, lvl_curso: str | None = None, det_porcentaje: int | None = None, cur_año: int | None = None, det_nameES: str | None = None):
        kwargs = {}
        if ID_test is not None:
            kwargs['test_ID'] = ID_test
        if pro_ID is not None:
            kwargs['pro_ID'] = pro_ID
        if cur_año is not None:
            kwargs['cur_año'] = cur_año
        if lvl_curso is not None:
            kwargs['lvl_curso'] = lvl_curso
        if det_nameES is not None:
            kwargs['det_nameES'] = det_nameES
        return db.resultados_detalladosREAD(**kwargs)

    def leer_resultados_detallados_by_det_id(self, det_id: int | None = None, pro_id: int| None = None, det_fecha: str | None =None):
        if pro_id is None:
            return db.resultados_detalladosREAD(det_ID=det_id)
        elif det_id is None:
            return db.resultados_detalladosREAD(pro_ID=pro_id)
        elif det_fecha is not None:
            return db.resultados_detalladosREAD(det_fecha=det_fecha)
        else:
            return db.resultados_detalladosREAD(det_ID=det_id, pro_ID=pro_id)
    
    def leer_info_test(self, test_id: int) -> TestDetails | None:
        test_record = db.testREAD(test_ID=test_id)
        if not test_record:
            return None
        es_id = test_record[1]
        pro_id = test_record[2]
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
    
    def crear_documento_pdf(self, nombre, extension, contenido):
        return db.documentoPDFCREATE(nombre, extension, contenido)

    def actualizar_documento_pdf(self, pdf_id: int, contenido: bytes):
        return db.documentoPDFUPDATE(pdf_id, contenido)

    def leer_lista_documentos_pdf(self):
        return db.documentoPDF_READ(include_content=False)

    def leer_contenido_documento_pdf(self, pdf_id: int):
        return db.documentoPDF_READ(pdf_id=pdf_id, include_content=True)

    def leer_documento_por_nombre(self, nombre_archivo: str):
        return db.documentoPDF_READ(pdf_nombre=nombre_archivo, include_content=True)
    
    def leer_profesores(self):
        return db.profesorREAD()

    def leer_profesor_por_rut(self, rut):
        return db.profesorREAD(pro_rut=rut)
    def leer_profesor_por_rut_contra_estado(self, rut, password):
        return db.profesorREAD(pro_rut=rut, pro_password=password)

    def crear_profesor(self, datos):
        return db.profesorCREATE(datos)

    def actualizar_profesor(self, prof_id, datos):
        db.profesorUPDATE(prof_id, datos)

    def eliminar_profesor(self, prof_id):
        db.profesorDELETE(prof_id)

    def crear_asignacion_pie(self, prof_id, cursos_str):
        db.prof_pie_CREATE(prof_id, cursos_str)

    def actualizar_asignacion_pie(self, prof_id, cursos_str):
        db.prof_pie_UPDATE(prof_id, cursos_str)

    def eliminar_asignacion_pie(self, prof_id):
        db.prof_pie_DELETE(prof_id)

    def obtener_pie_por_curso(self, curso_id: int):
        return db.obtener_pie_por_curso(curso_id)

    def crear_notificacion(self, prof_id_destino, mensaje, test_id):
        return db.notificacionCREATE(prof_id_destino, mensaje, test_id)

    def leer_notificaciones(self, prof_id: int, solo_no_leidas=False):
        return db.notificacionesREAD(prof_id=prof_id, solo_no_leidas=solo_no_leidas)

    def marcar_notificacion_leida(self, not_id):
        db.notificacionUPDATE_leida(not_id, leida=True)

    def eliminar_notificaciones(self, prof_id: int | None = None, not_status: int | None = None, noti_ID: int | None = None):
        return db.notificacionesDELETE(prof_id=prof_id, not_status=not_status, noti_ID=noti_ID)

    def crear_notificacion_a_pie(self, estudiante_id: int, id_resultado_detallado: int):
        
        try:
            estudiante_data = self.leer_estudiante_por_id(es_nameID=estudiante_id)
            if not estudiante_data:
                print(f"Error: No se encontró el estudiante con ID {estudiante_id}")
                return

            curso_id = estudiante_data.lvl_curso
            nombre_estudiante = f"{estudiante_data.es_nombre_1} {estudiante_data.es_apellido_pat}"
            profesor_pie_id = db.obtener_pie_por_curso(curso_id)

            if not profesor_pie_id:
                print(f"Advertencia: No se encontró un profesor PIE para el curso ID {curso_id}. No se creará la notificación.")
                return
            mensaje = f"Se ha realizado un test para el estudiante'{nombre_estudiante}' de nivel {estudiante_data.lvl_curso}"
            self.crear_notificacion(profesor_pie_id, mensaje, id_resultado_detallado)

        except Exception as e:
            print(f"Error en la base de datos al crear notificación: {e}")
            raise
