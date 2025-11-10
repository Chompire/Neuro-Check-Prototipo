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
            self.view.info_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("No se pudieron cargar los datos.", text_align=ft.TextAlign.CENTER)),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                ])
            )
            return

        # Crear y añadir la fila con los datos del docente
        row = ft.DataRow(cells=[
            ft.DataCell(ft.Text(f"{doc_info.pro_nombre_1} {doc_info.pro_nombre_2 or ''}".strip())),
            ft.DataCell(ft.Text(f"{doc_info.pro_apellido_pat} {doc_info.pro_apellido_mat}")),
            ft.DataCell(ft.Text(doc_info.pro_rut)),
            ft.DataCell(ft.Text("Profesional PIE" if doc_info.pro_cargo == 1 else "Profesor Docente")),
            ft.DataCell(ft.Text("N/A")),
        ])
        self.view.info_table.rows.append(row)

        if doc_info.pro_cargo == 1:
            self.cargar_cursos_pie(doc_info.pro_nameID)
        else:
            self.view.cursos_designados_table.rows.clear() # Limpiar la tabla si no es PIE


    def cargar_cursos_pie(self, pro_id):
        self.view.cursos_designados_table.rows.clear()
        resultados_detallados_profesional = self.model.leer_resultados_detallados(pro_ID=pro_id)
        conteo_por_curso = {}
        for resultado in resultados_detallados_profesional:
            curso = resultado.lvl_curso
            if curso:
                conteo_por_curso[curso] = conteo_por_curso.get(curso, 0) + 1

        # 3. Obtener todos los cursos de la BD para buscar sus detalles.
        todos_los_cursos = self.model.leer_cursos()
        cursos_map = {c.cur_nombre: c for c in todos_los_cursos}

        # 4. Llenar la tabla con los cursos y sus conteos, comparando con la tabla Curso.
        for nombre_curso, conteo in conteo_por_curso.items():
            curso_obj = cursos_map.get(nombre_curso)
            año_curso = str(curso_obj.cur_año) if curso_obj else "N/A"
            estado_curso = "Habilitado" if curso_obj and curso_obj.cur_state else "Inhabilitado"

            self.view.cursos_designados_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(nombre_curso)),
                    ft.DataCell(ft.Text(año_curso)),
                    ft.DataCell(ft.Text(str(conteo))),
                    ft.DataCell(ft.Text(estado_curso)),
                ])
            )
        self.page.update()