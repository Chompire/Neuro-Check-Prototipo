from flet_mvc import FletController
import flet as ft
import crud as db

class PerfilDocenteController(FletController):
    def __init__(self, page, model):
        super().__init__(page, model)
        
    def cargar_datos_docente(self):
        """Carga los datos del profesor logueado en la tabla de la vista."""
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
                ft.DataCell(ft.Text(doc_info.cur_nombre or "N/A")),
            ])
        )

    def cargar_tests_completados(self):
        """Carga los tests completados por el profesor logueado."""
        self.view.test_completos_table.rows.clear()
        
        pro_id = self.model.datos_profesor.pro_nameID
        tests = self.model.leer_test(pro_ID=pro_id, test_status=1)

        if not tests:
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
            for test in tests:
                self.view.test_completos_table.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(test.es_nombre_1)),
                        ft.DataCell(ft.Text(test.es_apellido_pat)),
                        ft.DataCell(ft.Text(test.es_rut)),
                        ft.DataCell(ft.Text(test.cur_nombre)),
                        ft.DataCell(ft.Text(test.test_fecha_inicio.strftime('%Y-%m-%d') if test.test_fecha_inicio else "N/A")),
                        ft.DataCell(ft.Text(test.test_fecha_termino.strftime('%Y-%m-%d') if test.test_fecha_termino else "N/A")),
                        ft.DataCell(ft.Text(f"{test.det_porcentaje or 0}%")),
                    ])
                )
        self.page.update()