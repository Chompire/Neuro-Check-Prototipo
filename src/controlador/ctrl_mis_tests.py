from flet_mvc import FletController
import flet as ft

class MisTestsController(FletController):
    def __init__(self, page, model):
        super().__init__(page, model)
        self.selected_test_id = None
        self.res_det_id = None
        self.numpage_completos = 10
        self.current_page_completos = 0
        self.total_pages_completos = 1
        self.numpage_otros = 10
        self.current_page_otros = 0
        self.total_pages_otros = 1

    def cargar_tests_completados(self):
        new_rows = []
        pro_id = self.model.datos_profesor.pro_nameID
        test_dat = self.model.leer_test(pro_ID=pro_id, test_status=1)
        total_items = len(test_dat)

        if not test_dat:
            new_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("No hay tests completados para mostrar.", text_align=ft.TextAlign.CENTER)),
                        *[ft.DataCell(ft.Text("")) for _ in range(6)] # Añadir 6 celdas vacías
                    ]
                )
            )
        else:
            total_pages = (total_items + self.numpage_completos - 1) // self.numpage_completos
            if total_pages == 0: total_pages = 1
            self.total_pages_completos = total_pages
            start_index = self.current_page_completos * self.numpage_completos
            end_index = start_index + self.numpage_completos
            tests_pagina_actual = test_dat[start_index:end_index]

            self.view.page_label_completos.value = f"Página {self.current_page_completos + 1} de {total_pages}"
            self.view.prev_button_completos.visible = self.current_page_completos > 0
            self.view.next_button_completos.visible = self.current_page_completos < total_pages - 1
            for test in tests_pagina_actual:
                new_rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(test.es_nombre_1)),
                        ft.DataCell(ft.Text(test.es_apellido_pat)),
                        ft.DataCell(ft.Text(test.es_rut)),
                        ft.DataCell(ft.Text(test.cur_nombre)),
                        ft.DataCell(ft.Text(test.test_fecha_inicio.strftime('%Y-%m-%d') if test.test_fecha_inicio else "N/A")),
                        ft.DataCell(ft.Text(test.test_fecha_termino.strftime('%Y-%m-%d') if test.test_fecha_termino else "N/A")),
                        ft.DataCell(ft.Text(f"{test.det_porcentaje or 0}%", color=ft.Colors.GREEN if (test.det_porcentaje or 0) <= 39 else ft.Colors.YELLOW if (test.det_porcentaje or 0) <= 69 else ft.Colors.RED)),
                        
                    ],
                    data = test,
                    on_select_changed=self.test_completos_row_select,
                    )
                )
        self.view.test_completos_table.rows = new_rows
        self.page.update()

    def cargar_test_profesores(self):
        if self.view.test_profesores_table is None:
            return

        new_rows = []
        test_dat = self.model.leer_test(test_status=1)
        current_pro_id = self.model.datos_profesor.pro_nameID
        curso_dat = self.model.leer_cursos_pie(self.model.datos_profesor.pro_nameID)
        
        if not curso_dat or not curso_dat[0]:
            return
        
        cursos_pie_ids = {int(cid) for cid in curso_dat[0].split(',') if cid.isdigit()}

        tests_filtrados = []
        for test in test_dat:
            if test.pro_ID != current_pro_id and test.cur_nameID in cursos_pie_ids:
                tests_filtrados.append(test)
        
        total_items = len(tests_filtrados)
        if total_items > 0:
            total_pages = (total_items + self.numpage_otros - 1) // self.numpage_otros
            self.total_pages_otros = total_pages
            start_index = self.current_page_otros * self.numpage_otros
            end_index = start_index + self.numpage_otros
            tests_pagina_actual = tests_filtrados[start_index:end_index]

            for test in tests_pagina_actual:                
                new_rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(test.es_nombre_1)),
                            ft.DataCell(ft.Text(test.es_apellido_pat)),
                            ft.DataCell(ft.Text(test.es_rut)),
                            ft.DataCell(ft.Text(test.cur_nombre)),
                            ft.DataCell(ft.Text(test.test_fecha_inicio.strftime('%Y-%m-%d') if test.test_fecha_inicio else "N/A")),
                            ft.DataCell(ft.Text(test.test_fecha_termino.strftime('%Y-%m-%d') if test.test_fecha_termino else "N/A")),
                            ft.DataCell(ft.Text(f"{test.pro_nombre_1} {test.pro_apellido_pat}")),
                            ft.DataCell(ft.Text(f"{test.det_porcentaje or 0}%", color=ft.Colors.GREEN if (test.det_porcentaje or 0) <= 39 else ft.Colors.YELLOW if (test.det_porcentaje or 0) <= 69 else ft.Colors.RED)),
                        ],
                        data=test,
                        on_select_changed=self.test_profesores_row_select,
                    )
                )
        else:
            new_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("No hay tests de otros profesores para mostrar.", text_align=ft.TextAlign.CENTER)),
                        *[ft.DataCell(ft.Text("")) for _ in range(7)] # Añadir 7 celdas vacías
                    ]
                )
            )

        self.view.test_profesores_table.rows = new_rows
        self.page.update()

    def next_page_completos(self, e):
        if self.current_page_completos < self.total_pages_completos - 1:
            self.current_page_completos += 1
            self.cargar_tests_completados()

    def prev_page_completos(self, e):
        if self.current_page_completos > 0:
            self.current_page_completos -= 1
            self.cargar_tests_completados()

    def next_page_otros(self, e):
        if self.current_page_otros < self.total_pages_otros - 1:
            self.current_page_otros += 1
            self.cargar_test_profesores()

    def prev_page_otros(self, e):
        if self.current_page_otros > 0:
            self.current_page_otros -= 1
            self.cargar_test_profesores()


    def test_profesores_row_select(self, e):
        selected_test = e.control.data
        for row in self.view.test_profesores_table.rows:
            row.selected = False

        if selected_test:
            e.control.selected = True
            self.selected_test_id = selected_test.test_ID
            print(self.selected_test_id)
            self.res_det_id = self.model.leer_resultados_detallados(self.selected_test_id)
            
            if self.res_det_id:
                self.page.go(f"/resultados_detallados/{self.res_det_id[0][0]}")
            else:
                print(f"Error: No se encontraron resultados detallados para el test ID {self.selected_test_id}")
                # Opcional: Mostrar un mensaje al usuario en la UI
        self.page.update()
    def test_completos_row_select(self, e):
        selected_test = e.control.data
        for row in self.view.test_completos_table.rows:
            row.selected = False

        if selected_test:
            e.control.selected = True
            self.selected_test_id = selected_test.test_ID
            self.res_det_id = self.model.leer_resultados_detallados(self.selected_test_id)
            
            if self.res_det_id:
                self.page.go(f"/resultados_detallados/{self.res_det_id[0][0]}")
            else:
                print(f"Error: No se encontraron resultados detallados para el test ID {self.selected_test_id}")
                # Opcional: Mostrar un mensaje al usuario en la UI
        self.page.update()