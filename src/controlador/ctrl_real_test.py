from flet_mvc import FletController
import flet as ft
import crud as db
from datetime import datetime

class RealizarTestController(FletController):
    def __init__(self, page, model):
        super().__init__(page, model)
        self.selected_student = None
        self.numpage_incomplete = 10
        self.numpage_estudiantes = 10
        self.current_page_est = 0
        self.current_page_tests = 0
        self.total_pages_est = 1
        self.total_pages_tests = 1
        if hasattr(self.model, 'datos_profesor') and self.model.datos_profesor:
            self.id_profesor = self.model.datos_profesor.pro_nameID
        else:
            self.id_profesor = None
        self.estudiante_data = self.model.leer_estudiantes()
        self.test_data = self.model.leer_test(pro_ID=self.id_profesor, test_status=0)
        self.selected_test_id = None
        
    def cargar_estudiantes(self, estudiantes_a_mostrar=None):
        self.view.next_button.visible = False
        new_rows = []
        self.selected_es_id = None

        # Obtener los cursos asignados al profesor
        cursos_asignados_ids = set()
        if self.id_profesor:
            cursos_asignados_str = self.model.leer_cursos_pie(self.id_profesor)
            if cursos_asignados_str and cursos_asignados_str.cursos_a_cargo:
                cursos_asignados_ids = {int(cid) for cid in cursos_asignados_str.cursos_a_cargo.split(',') if cid.isdigit()}

        # Filtrar estudiantes por cursos asignados y estado del curso
        todos_los_estudiantes = self.model.leer_estudiantes()
        self.estudiante_data = [
            est for est in todos_los_estudiantes 
            if est.cur_state == 1 and est.lvl_curso in cursos_asignados_ids
        ]
        if estudiantes_a_mostrar is None:
            estudiantes_a_mostrar = self.estudiante_data

        total_items = len(estudiantes_a_mostrar)
        total_pages_est = (total_items + self.numpage_estudiantes - 1) // self.numpage_estudiantes
        if total_pages_est == 0: total_pages_est = 1
        start_index = self.current_page_est * self.numpage_estudiantes
        end_index = start_index + self.numpage_estudiantes
        estudiantes_pagina_actual = estudiantes_a_mostrar[start_index:end_index]
        self.view.page_label_est.value = f"Página {self.current_page_est + 1} de {total_pages_est}"
        self.view.prev_button_est.disabled = self.current_page_est == 0
        self.view.next_button_est.disabled = self.current_page_est >= total_pages_est - 1
        
        for estudiante in estudiantes_pagina_actual:
            new_rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(estudiante.es_nombre_1, selectable=True)),
                    ft.DataCell(ft.Text(estudiante.es_apellido_pat, selectable=True)),
                    ft.DataCell(ft.Text(estudiante.es_nacimiento.strftime('%Y-%m-%d'), selectable=True)),
                    ft.DataCell(ft.Text(estudiante.es_rut, selectable=True)),
                    ft.DataCell(ft.Text(estudiante.cur_nombre, selectable=True)),
                ],
                data=estudiante,
                on_select_changed=self.es_row_select,
            )
            )
        self.view.estudiante_table.rows = new_rows
        self.page.update()

    def es_row_select(self, e):
        selected_es= e.control.data
        is_currently_selected = e.control.selected

        for row in self.view.estudiante_table.rows:
            row.selected = False

        if not is_currently_selected:
            e.control.selected = True
            self.view.next_button.visible = True
            self.selected_es_id = selected_es[0]
        else:
            self.selected_es_id = None
            self.view.next_button.visible = False
        self.page.update()
    
    def test_row_select(self, e):
        selected_test= e.control.data
        is_currently_selected = e.control.selected

        for row in self.view.test_incompletos.rows:
            row.selected = False

        if not is_currently_selected:
            e.control.selected = True
            self.view.upload_button.visible = True            
            self.view.eliminar_button.visible = True
            self.selected_test_id = selected_test.test_ID
            print(self.selected_test_id)
        else:
            self.selected_test_id = None
            self.view.upload_button.visible = False
            self.view.eliminar_button.visible = False
        self.page.update()

    def cargar_test_incompletos(self, test_a_mostrar=None):
        test_a_mostrar = db.testREAD(test_status=0)
        self.view.upload_button.visible = False
        new_rows = []
        self.selected_test_id = None
       
        total_items = len(test_a_mostrar)
        total_pages = (total_items + self.numpage_incomplete - 1) // self.numpage_incomplete
        start_index = self.current_page_tests * self.numpage_incomplete
        end_index = start_index + self.numpage_incomplete
        test_pagina_actual = test_a_mostrar[start_index:end_index]
        self.view.page_label_test.value = f"Página {self.current_page_tests + 1} de {total_pages}"
        self.view.prev_button_test.disabled = self.current_page_tests == 0
        self.view.next_button_test.disabled = self.current_page_tests >= total_pages - 1
        if test_a_mostrar:
            for test in test_pagina_actual:
                new_rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(test.es_nombre_1, selectable=True)),
                        ft.DataCell(ft.Text(test.es_apellido_pat, selectable=True)),
                        ft.DataCell(ft.Text(test.es_rut, selectable=True)),
                        ft.DataCell(ft.Text(test.cur_nombre, selectable=True)),
                        ft.DataCell(ft.Text(f"{test.pro_nombre_1} {test.pro_apellido_pat}", selectable=True)),
                        ft.DataCell(ft.Text(test.test_fecha_inicio.strftime('%Y-%m-%d'), selectable=True)),
                        ft.DataCell(ft.Text("Incompleto", selectable=True)),
                    ],
                    data=test,
                    on_select_changed=self.test_row_select,)
                )
        self.view.test_incompletos.rows = new_rows
        self.page.update()
    
    def next_page_test(self, e):
        total_items = len(self.test_data)
        total_pages = (total_items + self.numpage_incomplete - 1) // self.numpage_incomplete
        if self.current_page_tests < total_pages - 1:
            self.current_page_tests += 1
            self.test_search()

    def next_page_est(self, e):
        total_items = len(self.estudiante_data)
        total_pages = (total_items + self.numpage_estudiantes - 1) // self.numpage_estudiantes
        if self.current_page_est < total_pages - 1:
            self.current_page_est += 1
            self.est_search()


    def prev_page_test(self, e):
        if self.current_page_tests > 0:
            self.current_page_tests -= 1
            self.test_search()

    def prev_page_est(self, e):
            if self.current_page_est > 0:
                self.current_page_est -= 1
                self.est_search()

    def est_search(self, reset_page=False):
        if reset_page:
            self.current_page_est = 0

        search_text = self.view.estudiante_search.value.lower() if self.view.estudiante_search.value else ""
        
        if not search_text:
            self.cargar_estudiantes()
        else:
            estudiantes_filtrados = []
            for estudiante in self.estudiante_data:
                nombre_completo = f"{estudiante.es_nombre_1} {estudiante.es_apellido_pat}".lower()
                rut = estudiante.es_rut.lower()
                curso = estudiante.cur_nombre.lower()
                if search_text in nombre_completo or search_text in rut or search_text in curso:
                    estudiantes_filtrados.append(estudiante)
            self.cargar_estudiantes(estudiantes_filtrados)

    def test_search(self, reset_page=False):
        if reset_page:
            self.current_page_tests = 0
        search_text = self.view.test_search.value.lower() if self.view.test_search.value else ""
        if not search_text:
            self.cargar_test_incompletos()
        else:
            test_filtrados = []
            for test in self.test_data:
                nombre_completo = f"{test.es_nombre_1} {test.es_apellido_pat}".lower()
                rut = test.es_rut.lower()
                curso = test.cur_nombre.lower()
                if search_text in nombre_completo or search_text in rut or search_text in curso:
                    test_filtrados.append(test)
            self.cargar_test_incompletos(test_filtrados)


    def on_iniciar_test_click(self, e):
        fecha_inicio = datetime.now()
        pro_id = self.model.datos_profesor.pro_nameID if hasattr(self.model, 'datos_profesor') and self.model.datos_profesor else None
        test_data = (self.selected_es_id, pro_id, fecha_inicio, None)
        test_id = self.model.crear_test(*test_data)
        print(test_id)
        self.selected_test_id = test_id
        
        if self.selected_test_id is not None:
            self.model.crear_respuesta(None, "Atención", self.selected_test_id)
            self.model.crear_respuesta(None, "Memoria", self.selected_test_id)
            self.model.crear_respuesta(None, "Social", self.selected_test_id)
            self.model.crear_respuesta(None, "Emocional", self.selected_test_id)
            self.page.go(f"/test/{self.selected_test_id}")

    def on_reanudar_test_click(self, e):
        if self.selected_test_id is not None:
            print(f"Reanudando el test con ID: {self.selected_test_id}")
            self.page.go(f"/test/{self.selected_test_id}")
        else:
            self.view.feedback_snackbar.content = ft.Text("Por favor, selecciona un test para reanudar.")
            self.view.feedback_snackbar.bgcolor = ft.Colors.RED_700
            self.view.feedback_snackbar.open = True
            self.page.update()
    def eliminar_test(self, e):
        if self.selected_test_id is not None:
            self.model.eliminar_test(self.selected_test_id)
            self.view.feedback_snackbar.content = ft.Text("Test eliminado correctamente.")
            self.view.feedback_snackbar.bgcolor = ft.Colors.GREEN
            self.view.feedback_snackbar.open = True
            self.page.update()
            self.cargar_test_incompletos()
        else:
            self.view.feedback_snackbar.content = ft.Text("Por favor, selecciona un test para eliminar.")
            self.view.feedback_snackbar.bgcolor = ft.Colors.RED_700
            self.view.feedback_snackbar.open = True
            self.page.update()