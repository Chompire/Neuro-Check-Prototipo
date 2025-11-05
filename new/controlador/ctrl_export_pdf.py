from flet_mvc import FletController
import flet as ft

class ExportPDFController(FletController):
    def __init__(self, page, model):
        self.selected_est_id = None
        self.res_det_id = None
        super().__init__(page, model)
    def cargar_alumno(self, res_det_id: int):
        self.res_det_id = res_det_id

        # Leer los resultados detallados usando el ID
        resultados = self.model.leer_resultados_detallados_by_det_id(det_id=res_det_id)

        if resultados:
            resultado = resultados[0]
            test_id = resultado.id_test
            test_full = self.model.leer_test(test_id)
            estudiante_id = test_full[1]
            estudiante = self.model.leer_estudiante_por_id(estudiante_id)
            if estudiante.es_nombre_3 is None:
                nombre_completo = f"{estudiante.es_nombre_1} {estudiante.es_nombre_2} {estudiante.es_apellido_pat} {estudiante.es_apellido_mat}"
            else:
                nombre_completo = f"{estudiante.es_nombre_1} {estudiante.es_nombre_2} {estudiante.es_nombre_3} {estudiante.es_apellido_pat} {estudiante.es_apellido_mat}"

            self.view.nombre_completo_es.value = nombre_completo
            self.view.rut_es.value = estudiante.es_rut
            self.view.sexo_es.value = "Masculino" if estudiante.es_sexo == 1 else "Femenino"
            self.view.curso_es.value = resultado.lvl_curso
            self.page.update()