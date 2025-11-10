from flet_mvc import FletController
import flet as ft

class MisTestsController(FletController):
    def __init__(self, page, model):
        super().__init__(page, model)
        self.selected_test_id = None
        self.res_det_id = None

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

    def cargar_test_profesores(self):
        # Solo ejecutar si la tabla existe (es decir, si el usuario es PIE)
        if self.view.test_profesores_table is None:
            return # Si la tabla no existe en la vista, no hacer nada.

        self.view.test_profesores_table.rows.clear()
        
        # Obtener todos los tests completados (status=1)
        test_dat = self.model.leer_test(test_status=1)
        
        # Obtener los cursos a cargo del profesional PIE actual
        current_pro_id = self.model.datos_profesor.pro_nameID
        curso_dat = self.model.leer_cursos_pie(self.model.datos_profesor.pro_nameID)
        print(curso_dat)

        # Convertir la cadena de IDs de cursos (ej: "1,5,8") en una lista de enteros [1, 5, 8]
        cursos_pie_ids = [int(cid) for cid in curso_dat[0].split(',') if cid.isdigit()]

        # Filtrar y mostrar los tests
        for test in test_dat:
            # Condición: El test es de OTRO profesor Y el curso del estudiante está en la lista de cursos del PIE.
            if test.pro_ID != current_pro_id and test.cur_nameID in cursos_pie_ids:
                self.view.test_profesores_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(test.es_nombre_1)),
                            ft.DataCell(ft.Text(test.es_apellido_pat)),
                            ft.DataCell(ft.Text(test.es_rut)),
                            ft.DataCell(ft.Text(test.cur_nombre)),
                            ft.DataCell(ft.Text(test.test_fecha_inicio.strftime('%Y-%m-%d') if test.test_fecha_inicio else "N/A")),
                            ft.DataCell(ft.Text(test.test_fecha_termino.strftime('%Y-%m-%d') if test.test_fecha_termino else "N/A")),
                            ft.DataCell(ft.Text(f"{test.det_porcentaje or 0}%")),
                        ],
                        data=test,
                        on_select_changed=self.test_profesores_row_select,
                    )
                )

    def test_profesores_row_select(self, e):
        selected_test = e.control.data
        for row in self.view.test_profesores_table.rows:
            row.selected = False

        if selected_test:
            e.control.selected = True
            self.selected_test_id = selected_test.test_ID
            print(self.selected_test_id)
            self.res_det_id = self.model.leer_resultados_detallados(self.selected_test_id) # This returns a list of detailed results for a test_ID
          
            self.page.go(f"/resultados_detallados/{self.res_det_id[0][0]}")
        

        self.page.update()
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