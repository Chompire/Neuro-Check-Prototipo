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
            self.id_profesor = None # Manejar el caso si los datos del profesor no están cargados
        self.estudiante_data = self.model.leer_estudiantes() # Ahora este método existe
        self.test_data = self.model.leer_test(pro_ID=self.id_profesor, test_status=0) # Cargar tests incompletos del profesor
        self.selected_test_id = None
        
    def cargar_estudiantes(self, estudiantes_a_mostrar=None):
        self.view.estudiante_table.rows.clear()
        self.view.next_button.visible = False
        self.selected_es_id = None
        
        # Leer estudiantes y filtrar por cursos habilitados (cur_state == 1)
        self.estudiante_data = [est for est in self.model.leer_estudiantes() if est.cur_state == 1]
        if estudiantes_a_mostrar is None:
            estudiantes_a_mostrar = self.estudiante_data

        total_items = len(estudiantes_a_mostrar)
        total_pages_est = (total_items + self.numpage_estudiantes - 1) // self.numpage_estudiantes
        if total_pages_est == 0: total_pages_est = 1 # Evitar página 0 de 0
        start_index = self.current_page_est * self.numpage_estudiantes
        end_index = start_index + self.numpage_estudiantes
        estudiantes_pagina_actual = estudiantes_a_mostrar[start_index:end_index]
        self.view.page_label_est.value = f"Página {self.current_page_est + 1} de {total_pages_est}"
        self.view.prev_button_est.disabled = self.current_page_est == 0
        self.view.next_button_est.disabled = self.current_page_est >= total_pages_est - 1
        self.page.update()
        
        for estudiante in estudiantes_pagina_actual:
            self.view.estudiante_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(estudiante.es_nombre_1)),
                    ft.DataCell(ft.Text(estudiante.es_apellido_pat)),
                    ft.DataCell(ft.Text(estudiante.es_nacimiento.strftime('%Y-%m-%d'))), # Formatear fecha
                    ft.DataCell(ft.Text(estudiante.es_rut)),
                    ft.DataCell(ft.Text(estudiante.cur_nombre)),
                ],
                data=estudiante,
                on_select_changed=self.es_row_select,
            )
            )
        self.page.update()

    def es_row_select(self, e):
        selected_es_id = None
        selected_es= e.control.data
        is_currently_selected = e.control.selected
        for row in self.view.estudiante_table.rows:
            row.selected = False
        if not is_currently_selected:
            e.control.selected = True
            self.view.next_button.visible = True
            self.selected_es_id = selected_es[0]
        else:
            for row in self.view.estudiante_table.rows:
                row.selected = False
                if selected_es_id is not None:
                    self.view.next_button.visible = False
                for row in self.view.estudiante_table.rows:
                    row.selected = False
                    self.view.next_button.visible = False
        self.page.update()
    
    def test_row_select(self, e):
        selected_test_id = None
        selected_test= e.control.data
        is_currently_selected = e.control.selected
        for row in self.view.test_incompletos.rows:
            row.selected = False
        if not is_currently_selected:
            e.control.selected = True
            self.view.upload_button.visible = True
            self.selected_test_id = selected_test.test_ID
            print(self.selected_test_id)
        else:
            for row in self.view.test_incompletos.rows:
                row.selected = False
                if selected_test_id  is not None:
                    self.view.upload_button.visible = False
                for row in self.view.test_incompletos.rows:
                    row.selected = False
                    self.view.upload_button.visible = False
        self.page.update()

    def cargar_test_incompletos(self, test_a_mostrar=None):
        test_a_mostrar = db.testREAD(test_status=0)
        self.view.test_incompletos.rows.clear()
        self.view.upload_button.visible = False
        self.selected_test_id = None
       
        total_items = len(test_a_mostrar)
        total_pages = (total_items + self.numpage_incomplete - 1) // self.numpage_incomplete
        start_index = self.current_page_tests * self.numpage_incomplete
        end_index = start_index + self.numpage_incomplete
        test_pagina_actual = test_a_mostrar[start_index:end_index]
        self.view.page_label_test.value = f"Página {self.current_page_tests + 1} de {total_pages}"
        self.view.prev_button_test.disabled = self.current_page_tests == 0
        self.view.next_button_test.disabled = self.current_page_tests >= total_pages - 1
        self.page.update()
        if test_a_mostrar:
            for test in test_pagina_actual:
                self.view.test_incompletos.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(test.es_nombre_1)),
                        ft.DataCell(ft.Text(test.es_apellido_pat)),
                        ft.DataCell(ft.Text(test.es_rut)),
                        ft.DataCell(ft.Text(test.cur_nombre)),
                        ft.DataCell(ft.Text(f"{test.pro_nombre_1} {test.pro_apellido_pat}")),
                        ft.DataCell(ft.Text(test.test_fecha_inicio.strftime('%Y-%m-%d'))),
                        ft.DataCell(ft.Text("Incompleto")), # El estado es 0 (Incompleto)
                    ],
                    data=test,
                    on_select_changed=self.test_row_select,)
                )
                self.page.update()

    
    def next_page_test(self, e):
        lista_test_incompletos = db.testREAD(test_status=0)
        total_items = len(lista_test_incompletos)
        total_pages = (total_items + self.numpage_incomplete - 1) // self.numpage_incomplete
        if self.current_page_tests < total_pages - 1:
            self.current_page_tests += 1
            self.cargar_test_incompletos()

    def next_page_est(self, e):
        lista_estudiantes = db.estudiantesREAD()
        total_items = len(lista_estudiantes)
        total_pages = (total_items + self.numpage_estudiantes - 1) // self.numpage_estudiantes
        if self.current_page_est < total_pages - 1:
            self.current_page_est += 1
            self.cargar_estudiantes()


    def prev_page_test(self, e):
        if self.current_page_tests > 0:
            self.current_page_tests -= 1
            self.cargar_test_incompletos()

    def prev_page_est(self, e):
            if self.current_page_est > 0:
                self.current_page_est -= 1
                self.cargar_estudiantes()

    def est_search(self, reset_page=False):
        if reset_page:
            self.current_page_est = 0 # Reiniciar a la primera página en una nueva búsqueda

        search_text = self.view.estudiante_search.value.lower() if self.view.estudiante_search.value else ""
        
        if not search_text:
            # Si no hay búsqueda, cargar todos los estudiantes
            self.cargar_estudiantes()
        else:
            # Filtrar la lista de estudiantes
            estudiantes_filtrados = []
            for estudiante in self.estudiante_data:
                nombre_completo = f"{estudiante.es_nombre_1} {estudiante.es_apellido_pat}".lower()
                rut = estudiante.es_rut.lower()
                curso = estudiante.cur_nombre.lower()
                if search_text in nombre_completo or search_text in rut or search_text in curso:
                    estudiantes_filtrados.append(estudiante)
            # Llamar a cargar_estudiantes con la lista filtrada
            self.cargar_estudiantes(estudiantes_filtrados)

    def test_search(self, reset_page=False):
        if reset_page:
            self.current_page_tests = 0 # Reiniciar a la primera página en una nueva búsqueda
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