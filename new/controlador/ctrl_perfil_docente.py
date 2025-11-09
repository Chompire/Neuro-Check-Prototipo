from flet_mvc import FletController
import flet as ft
import crud as db

class PerfilDocenteController(FletController):
    def __init__(self, page, model):
        super().__init__(page, model)
        self.selected_test_id = None
        self.res_det_id = None
        self.pro_id = None
        
        
        
    def cargar_datos_docente(self):
        self.view.info_table.rows.clear()
        
        doc_info = self.model.datos_profesor
        if not doc_info:
            # Manejar el caso en que no hay datos de profesor
            self.view.info_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("No se pudieron cargar los datos.", text_align=ft.TextAlign.CENTER)),
                    ft.DataCell(ft.Text("")), # Celda vacía para la columna 2
                    ft.DataCell(ft.Text("")), # Celda vacía para la columna 3
                    ft.DataCell(ft.Text("")), # Celda vacía para la columna 4
                    ft.DataCell(ft.Text("")), # Celda vacía para la columna 5
                ])
            )
            return

        self.view.info_table.rows.append(
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(f"{doc_info.pro_nombre_1} {doc_info.pro_nombre_2 or ''}".strip())),
                ft.DataCell(ft.Text(f"{doc_info.pro_apellido_pat} {doc_info.pro_apellido_mat}")),
                ft.DataCell(ft.Text(doc_info.pro_rut)),
                ft.DataCell(ft.Text("Profesional PIE" if doc_info.pro_cargo == 1 else "Profesor Docente")),
                ft.DataCell(ft.Text("N/A")), # Celda faltante para la columna "Curso"
            ])
        )

        # Si el profesor es PIE, cargar los cursos designados
        self.cargar_conteo_encuestas_por_curso(doc_info.pro_nameID)


    def cargar_tests_completados(self):
        self.view.test_completos_table.rows.clear()
        pro_id = self.model.datos_profesor.pro_nameID
        test_dat = self.model.leer_test(pro_ID=pro_id, test_status=1)

        if not test_dat:
            self.view.test_completos_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("No hay tests completados para mostrar.", text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text("")), # Celda vacía para la columna 2
                        ft.DataCell(ft.Text("")), # Celda vacía para la columna 3
                        ft.DataCell(ft.Text("")), # Celda vacía para la columna 4
                        ft.DataCell(ft.Text("")), # Celda vacía para la columna 5
                        ft.DataCell(ft.Text("")), # Celda vacía para la columna 6
                        ft.DataCell(ft.Text("")), # Celda vacía para la columna 7
                    ]
                )
            )
        else:
            for test in test_dat:
                self.view.test_completos_table.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(test.es_nombre_1)),
                        ft.DataCell(ft.Text(test.es_apellido_pat)),
                        ft.DataCell(ft.Text(test.es_rut)),
                        ft.DataCell(ft.Text(test.cur_nombre)),
                        ft.DataCell(ft.Text(test.test_fecha_inicio.strftime('%Y-%m-%d') if test.test_fecha_inicio else "N/A")),
                        ft.DataCell(ft.Text(test.test_fecha_termino.strftime('%Y-%m-%d') if test.test_fecha_termino else "N/A")),
                        ft.DataCell(ft.Text(f"{test.det_porcentaje or 0}%")),
                        
                    ],
                    data = test,
                    on_select_changed=self.test_completos_row_select,
                    )
                )
    def test_completos_row_select(self, e):
        selected_test = e.control.data
        for row in self.view.test_completos_table.rows:
            row.selected = False

        if selected_test:
            e.control.selected = True
            self.selected_test_id = selected_test.test_ID
            self.res_det_id = self.model.leer_resultados_detallados(self.selected_test_id) # This returns a list of detailed results for a test_ID
          
            self.page.go(f"/resultados_detallados/{self.res_det_id[0][0]}")
        

        self.page.update()

    def cargar_conteo_encuestas_por_curso(self, pro_id):
        """Cuenta los resultados detallados por curso para un profesor específico."""
        self.view.cursos_designados_table.rows.clear()
        all_results = self.model.leer_resultados_detallados_by_det_id(pro_id=pro_id)
        conteo = {}
        if all_results:
            for resultado in all_results:
                curso = resultado.lvl_curso
                año = resultado.cur_año
                state = resultado.cur_state
                print(f"Curso: {curso}")    
                conteo[curso] = conteo.get(curso, 0) + 1
        
        for curso, num_encuestas in conteo.items():
            self.view.cursos_designados_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(curso)),
                    ft.DataCell(ft.Text(año)),
                    ft.DataCell(ft.Text(str(num_encuestas))),
                    ft.DataCell(ft.Text("Habilitado" if state == 1 else "Deshabilitado")),
                ])
            )